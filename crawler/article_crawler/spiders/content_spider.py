import scrapy
from bs4 import BeautifulSoup
from crawler.article_crawler.items import ArticleCrawlerItem

import logging


logger = logging.getLogger(__name__)


class ContentSpider(scrapy.Spider):
    name = "content_spider"

    async def start(self):
        
        urls = getattr(self, "urls", [])

        for url in urls:
            yield scrapy.Request(url, callback=self.parse, errback=self.handle_error, meta={"playwright" : True})

    def handle_error(self, failure):
        """
        Catches and logs request failures.
        """
        
        request_url = failure.request.url
        error_type = failure.value.__class__.__name__
        
        logger.error(
            f"Request failed for URL: {request_url}. Error: {error_type}"
        )

    
    def parse(self, response):
        """
        This method is only called for SUCCESSFUL requests.
        """

        logger.info(f"Successfully fetched and parsing URL: {response.url}")

        soup = BeautifulSoup(response.body, "html.parser")

        for tag in soup(['nav', 'footer', 'header', 'script', 'style', 'aside', 'form']):
            tag.decompose()

        cleaned_text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""

        item = ArticleCrawlerItem()
        item['url'] = response.url
        item['cleaned_text'] = cleaned_text

        yield item

