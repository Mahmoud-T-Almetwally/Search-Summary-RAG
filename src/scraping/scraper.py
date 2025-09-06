from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.article_crawler.spiders.content_spider import ContentSpider
from crawler.article_crawler.items import ArticleCrawlerItem

import logging
from typing import Dict, List


logger = logging.Logger(__name__)

CRAWLER_RESULTS = []


class ItemCollectorPipeline:
    """A Scrapy pipeline that collects items into a list."""
    def __init__(self):
        self.items = []

    def open_spider(self, spider):
        CRAWLER_RESULTS.clear()

    def close_spider(self, spider):
        global CRAWLER_RESULTS
        CRAWLER_RESULTS = self.items

    def process_item(self, item, spider):
        self.items.append(dict(item))
        return item
    

def scrape_urls(urls: List[str]) -> Dict[str, str]:
    """
    Runs the Scrapy content_spider for the given URLs and returns the cleaned text.
    The function signature remains the same, so the rest of the application is unaffected.

    args:
        urls: a list of url strings to be scraped.

    returns:
        a dictionary of urls to scraped text.

    example usage:
        >>> items = scrape_urls(['https://example.com'])
        >>> items
            {'https://example.com' : "example cleaned text"}
    """

    if not urls:
        return {}
    
    logger.info(msg=f"Initializing Scrapy crawler for {len(urls)} URLs...")

    settings = get_project_settings()
    settings.set("ITEM_PIPELINES", {**settings.get("ITEM_PIPELINES", {}), ItemCollectorPipeline: 1})

    process = CrawlerProcess(settings=settings)
    process.crawl(ContentSpider, urls=urls)

    process.start()

    scraped_content = {item['url']: item['cleaned_text'] for item in CRAWLER_RESULTS if item.get('cleaned_text')}
    
    logger.info(msg=f"Scraping complete. Successfully extracted content from {len(scraped_content)} URLs.")
    
    return scraped_content
