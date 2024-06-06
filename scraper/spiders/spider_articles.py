import scrapy
from scrapy.http import Response


class ArticlesSpider(scrapy.Spider):
    name = "articles"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com"]

    def parse(self, response: Response, **kwargs) -> None:

        try:
            articles = response.css(".titleline a::attr(href)").getall()
            for article in articles:
                yield response.follow(article, callback=self._parse_article)
        except Exception as e:
            self.logger.error(f"Error parsing page: {e}")

        next_page = response.css(
            "a.morelink::attr(href)"
        ).get()
        if next_page is not None:
            next_page_with_param = response.urljoin(f"{self.start_urls} + '/' + {next_page}")
            yield response.follow(next_page_with_param, callback=self.parse)

    @staticmethod
    def _parse_article(response: Response) -> None:

        title = response.css(".titleline a::text").get()
        url = response.css(".titleline a::attr(href)").get()

        yield {
            "title": title,
            "url": url,
        }
