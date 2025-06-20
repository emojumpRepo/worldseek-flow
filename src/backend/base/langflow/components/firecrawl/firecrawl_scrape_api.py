from langflow.custom.custom_component.component import Component
from langflow.io import (
    DataInput,
    IntInput,
    MultilineInput,
    Output,
    SecretStrInput,
)
from langflow.schema.data import Data


class FirecrawlScrapeApi(Component):
    display_name: str = "FirecrawlScrapeApi"
    description: str = "Firecrawl Scrape API."
    name = "FirecrawlScrapeApi"

    documentation: str = "https://docs.firecrawl.dev/api-reference/endpoint/scrape"

    inputs = [
        SecretStrInput(
            name="api_key",
            display_name="API密钥",
            required=True,
            password=True,
            info="The API key to use Firecrawl API.",
        ),
        MultilineInput(
            name="url",
            display_name="网址",
            required=True,
            info="The 网址 to scrape.",
            tool_mode=True,
        ),
        IntInput(
            name="timeout",
            display_name="超时",
            info="超时 in milliseconds for the request.",
        ),
        DataInput(
            name="scrapeOptions",
            display_name="Scrape Options",
            info="The page options to send with the request.",
        ),
        DataInput(
            name="extractorOptions",
            display_name="Extractor Options",
            info="The extractor options to send with the request.",
        ),
    ]

    outputs = [
        Output(display_name="数据", name="data", method="scrape"),
    ]

    def scrape(self) -> Data:
        try:
            from firecrawl import FirecrawlApp
        except ImportError as e:
            msg = "Could not import firecrawl integration package. Please install it with `pip install firecrawl-py`."
            raise ImportError(msg) from e

        params = self.scrapeOptions.__dict__.get("data", {}) if self.scrapeOptions else {}
        extractor_options_dict = self.extractorOptions.__dict__.get("data", {}) if self.extractorOptions else {}
        if extractor_options_dict:
            params["extract"] = extractor_options_dict

        # Set default values for parameters
        params.setdefault("formats", ["markdown"])  # Default output format
        params.setdefault("onlyMainContent", True)  # Default to only main content

        app = FirecrawlApp(api_key=self.api_key)
        results = app.scrape_url(self.url, params=params)
        return Data(data=results)
