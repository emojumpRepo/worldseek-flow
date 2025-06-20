import re
from urllib.parse import parse_qs, unquote, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

from langflow.custom import Component
from langflow.io import IntInput, MessageTextInput, Output
from langflow.schema import DataFrame
from langflow.services.deps import get_settings_service


class WebSearchComponent(Component):
    display_name = "Web Search"
    display_name_zh = "网页搜索"
    description = "Performs a basic DuckDuckGo search (HTML scraping). May be subject to rate limits."
    description_zh = "执行基本的DuckDuckGo搜索（HTML抓取）。可能受到速率限制。"
    icon = "search"
    name = "WebSearchNoAPI"

    inputs = [
        MessageTextInput(
            name="query",
            display_name="搜索查询",
            info="要搜索的关键词。",
            tool_mode=True,
            required=True,
        ),
        IntInput(
            name="timeout",
            display_name="超时",
            info="请求的超时时间（秒）。",
            value=5,
            advanced=True,
        ),
    ]

    outputs = [Output(name="results", display_name="搜索结果", method="perform_search")]

    def validate_url(self, string: str) -> bool:
        url_regex = re.compile(
            r"^(https?:\/\/)?" r"(www\.)?" r"([a-zA-Z0-9.-]+)" r"(\.[a-zA-Z]{2,})?" r"(:\d+)?" r"(\/[^\s]*)?$",
            re.IGNORECASE,
        )
        return bool(url_regex.match(string))

    def ensure_url(self, url: str) -> str:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
        if not self.validate_url(url):
            msg = f"Invalid URL: {url}"
            raise ValueError(msg)
        return url

    def _sanitize_query(self, query: str) -> str:
        """Sanitize search query."""
        # Remove potentially dangerous characters
        return re.sub(r'[<>"\']', "", query.strip())

    def perform_search(self) -> DataFrame:
        query = self._sanitize_query(self.query)
        if not query:
            msg = "Empty search query"
            raise ValueError(msg)
        headers = {"User-Agent": get_settings_service().settings.user_agent}
        params = {"q": query, "kl": "us-en"}
        url = "https://html.duckduckgo.com/html/"

        try:
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
        except requests.RequestException as e:
            self.status = f"Failed request: {e!s}"
            return DataFrame(pd.DataFrame([{"title": "Error", "link": "", "snippet": str(e), "content": ""}]))

        if not response.text or "text/html" not in response.headers.get("content-type", "").lower():
            self.status = "No results found"
            return DataFrame(
                pd.DataFrame([{"title": "Error", "link": "", "snippet": "No results found", "content": ""}])
            )
        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.select("div.result"):
            title_tag = result.select_one("a.result__a")
            snippet_tag = result.select_one("a.result__snippet")
            if title_tag:
                raw_link = title_tag.get("href", "")
                parsed = urlparse(raw_link)
                uddg = parse_qs(parsed.query).get("uddg", [""])[0]
                decoded_link = unquote(uddg) if uddg else raw_link

                try:
                    final_url = self.ensure_url(decoded_link)
                    page = requests.get(final_url, headers=headers, timeout=self.timeout)
                    page.raise_for_status()
                    content = BeautifulSoup(page.text, "lxml").get_text(separator=" ", strip=True)
                except requests.RequestException as e:
                    final_url = decoded_link
                    content = f"(Failed to fetch: {e!s}"

                results.append(
                    {
                        "title": title_tag.get_text(strip=True),
                        "link": final_url,
                        "snippet": snippet_tag.get_text(strip=True) if snippet_tag else "",
                        "content": content,
                    }
                )

        df_results = pd.DataFrame(results)
        return DataFrame(df_results)
