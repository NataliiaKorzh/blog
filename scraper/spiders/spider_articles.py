import scrapy
from scrapy.http import Response


class ArticlesSpider(scrapy.Spider):
    """
    Spider for scraping articles from Hacker News.

    This spider crawls Hacker News and extracts article titles and URLs.

    Attributes:
        name (str): The name of the spider.
        allowed_domains (list): The list of allowed domains to crawl.
        start_urls (list): The list of URLs to start crawling from.
    """
    name = "articles"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com"]

    def parse(self, response: Response, **kwargs) -> None:
        """
        Parse the response and extract article links.

        Args:
            response (Response): The response object containing the page source.
        """
        try:
            articles = response.css(".titleline a::attr(href)").getall()
            for article in articles:
                yield response.follow(article, callback=self._parse_article)
        except Exception as e:
            self.logger.error(f"Error parsing page: {e}")

        next_page = response.css("a.morelink::attr(href)").get()
        if next_page is not None:
            next_page_with_param = response.urljoin(next_page)
            yield response.follow(next_page_with_param, callback=self.parse)

    @staticmethod
    def _parse_article(response: Response) -> None:
        """
        Parse the article page and extract title and URL.

        Args:
            response (Response): The response object containing the article page source.
        """
        title = response.css(".titleline a::text").get()
        url = response.css(".titleline a::attr(href)").get()

        yield {
            "title": title,
            "url": url,
        }
