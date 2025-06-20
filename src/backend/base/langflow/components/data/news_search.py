from urllib.parse import quote_plus

import pandas as pd
import requests
from bs4 import BeautifulSoup

from langflow.custom import Component
from langflow.io import IntInput, MessageTextInput, Output
from langflow.schema import DataFrame


class NewsSearchComponent(Component):
    display_name = "News Search"
    display_name_zh = "新闻搜索"
    description = "Searches Google News via RSS. Returns clean article data."
    description_zh = "通过RSS搜索Google新闻。返回文章数据。"
    icon = "newspaper"
    name = "NewsSearch"

    inputs = [
        MessageTextInput(
            name="query",
            display_name="搜索查询",
            info="搜索关键词以获取新闻文章。",
            tool_mode=True,
            required=True,
        ),
        MessageTextInput(
            name="hl",
            display_name="语言 (hl)",
            info="语言代码, e.g. en-US, fr, de. 默认: en-US.",
            tool_mode=False,
            input_types=[],
            required=False,
            advanced=True,
        ),
        MessageTextInput(
            name="gl",
            display_name="国家 (gl)",
            info="国家代码, e.g. US, FR, DE. 默认: US.",
            tool_mode=False,
            input_types=[],
            required=False,
            advanced=True,
        ),
        MessageTextInput(
            name="ceid",
            display_name="国家:语言 (ceid)",
            info="e.g. US:en, FR:fr. 默认: US:en.",
            tool_mode=False,
            value="US:en",
            input_types=[],
            required=False,
            advanced=True,
        ),
        MessageTextInput(
            name="topic",
            display_name="主题",
            info="只填写一个: WORLD, NATION, BUSINESS, TECHNOLOGY, ENTERTAINMENT, SCIENCE, SPORTS, HEALTH.",
            tool_mode=False,
            input_types=[],
            required=False,
            advanced=True,
        ),
        MessageTextInput(
            name="location",
            display_name="位置 (Geo)",
            info="城市、州或国家用于位置相关新闻。留空用于关键词搜索。",
            tool_mode=False,
            input_types=[],
            required=False,
            advanced=True,
        ),
        IntInput(
            name="timeout",
            display_name="超时",
            info="请求的超时时间（秒）。",
            value=5,
            required=False,
            advanced=True,
        ),
    ]

    outputs = [Output(name="articles", display_name="新闻文章", method="search_news")]

    def search_news(self) -> DataFrame:
        # Defaults
        hl = getattr(self, "hl", None) or "en-US"
        gl = getattr(self, "gl", None) or "US"
        ceid = getattr(self, "ceid", None) or f"{gl}:{hl.split('-')[0]}"
        topic = getattr(self, "topic", None)
        location = getattr(self, "location", None)
        query = getattr(self, "query", None)

        # Build base URL
        if topic:
            # Topic-based feed
            base_url = f"https://news.google.com/rss/headlines/section/topic/{quote_plus(topic.upper())}"
            params = f"?hl={hl}&gl={gl}&ceid={ceid}"
            rss_url = base_url + params
        elif location:
            # Location-based feed
            base_url = f"https://news.google.com/rss/headlines/section/geo/{quote_plus(location)}"
            params = f"?hl={hl}&gl={gl}&ceid={ceid}"
            rss_url = base_url + params
        elif query:
            # Keyword search feed
            base_url = "https://news.google.com/rss/search?q="
            query_parts = [query]
            query_encoded = quote_plus(" ".join(query_parts))
            params = f"&hl={hl}&gl={gl}&ceid={ceid}"
            rss_url = f"{base_url}{query_encoded}{params}"
        else:
            self.status = "No search query, topic, or location provided."
            self.log(self.status)
            return DataFrame(
                pd.DataFrame(
                    [
                        {
                            "title": "Error",
                            "link": "",
                            "published": "",
                            "summary": "No search query, topic, or location provided.",
                        }
                    ]
                )
            )

        try:
            response = requests.get(rss_url, timeout=self.timeout)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "xml")
            items = soup.find_all("item")
        except requests.RequestException as e:
            self.status = f"Failed to fetch news: {e}"
            self.log(self.status)
            return DataFrame(pd.DataFrame([{"title": "Error", "link": "", "published": "", "summary": str(e)}]))
        except (AttributeError, ValueError, TypeError) as e:
            self.status = f"Unexpected error: {e!s}"
            self.log(self.status)
            return DataFrame(pd.DataFrame([{"title": "Error", "link": "", "published": "", "summary": str(e)}]))

        if not items:
            self.status = "No news articles found."
            self.log(self.status)
            return DataFrame(pd.DataFrame([{"title": "No articles found", "link": "", "published": "", "summary": ""}]))

        articles = []
        for item in items:
            try:
                title = self.clean_html(item.title.text if item.title else "")
                link = item.link.text if item.link else ""
                published = item.pubDate.text if item.pubDate else ""
                summary = self.clean_html(item.description.text if item.description else "")
                articles.append({"title": title, "link": link, "published": published, "summary": summary})
            except (AttributeError, ValueError, TypeError) as e:
                self.log(f"Error parsing article: {e!s}")
                continue

        df_articles = pd.DataFrame(articles)
        self.log(f"Found {len(df_articles)} articles.")
        return DataFrame(df_articles)

    def clean_html(self, html_string: str) -> str:
        return BeautifulSoup(html_string, "html.parser").get_text(separator=" ", strip=True)
