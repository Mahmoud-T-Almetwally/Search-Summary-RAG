# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleCrawlerItem(scrapy.Item):
    url = scrapy.Field()
    cleaned_text = scrapy.Field()
