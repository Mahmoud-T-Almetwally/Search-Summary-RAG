import pytest
from pathlib import Path
from scrapy.http import HtmlResponse, Request
from crawler.article_crawler.spiders.content_spider import ContentSpider


TEST_DATA_DIR = Path(__file__).parent.parent / "test_data"

def test_spider_parsing_logic():
    """
    Tests the spider's parse() method to ensure it correctly extracts
    and cleans text from a local HTML file.
    """

    html_file_path = TEST_DATA_DIR / "sample_article.html"
    html_content = html_file_path.read_text(encoding="utf-8")
    
    fake_url = "http://example.com/article.html"
    request = Request(url=fake_url)
    response = HtmlResponse(
        url=fake_url,
        request=request,
        body=html_content,
        encoding='utf-8'
    )

    spider = ContentSpider()

    results = list(spider.parse(response))

    assert len(results) == 1
    
    item = results[0]
    
    assert item['url'] == fake_url
    
    cleaned_text = item['cleaned_text']
    assert cleaned_text is not None
    assert len(cleaned_text) > 100 
    
    assert '<nav>' not in cleaned_text
    assert '<footer>' not in cleaned_text
    assert 'script' not in cleaned_text.lower()