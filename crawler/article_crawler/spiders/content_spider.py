import scrapy
from bs4 import BeautifulSoup
from article_crawler.items import ArticleCrawlerItem


class ContentSpider(scrapy.Spider):
    name = "content_spider"

    def start_requests(self):
        
        urls = getattr(self, "urls", [])

        for url in urls:
            yield scrapy.Request(url, callback=self.parse, meta={"playwright" : True})

    
    def parse(self, response):

        soup = BeautifulSoup(response.body, "html.parser")

        for tag in soup(['nav', 'footer', 'header', 'script', 'style', 'aside', 'form']):
            tag.decompose()

        cleaned_text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""

        item = ArticleCrawlerItem()
        item['url'] = response.url
        item['cleaned_text'] = cleaned_text

        yield item

