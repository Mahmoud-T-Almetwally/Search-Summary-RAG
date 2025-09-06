import pytest
from src.scraping import scraper # Import the module we are testing

def test_scrape_urls_with_mocked_crawler(mocker):
    """
    Tests the scrape_urls orchestrator function.
    It mocks the Scrapy CrawlerProcess to avoid running a real crawl,
    and checks if the function correctly processes the simulated results.
    """
    
    test_urls = ["http://test.com/page1", "http://test.com/page2"]
    
    mock_results = [
        {'url': 'http://test.com/page1', 'cleaned_text': 'This is page one.'},
        {'url': 'http://test.com/page2', 'cleaned_text': 'This is page two.'}
    ]

    mock_crawler_process = mocker.patch('src.scraping.scraper.CrawlerProcess')

    mock_crawler_process.return_value.start.return_value = None

    mocker.patch('src.scraping.scraper.CRAWLER_RESULTS', mock_results)

    final_dict = scraper.scrape_urls(test_urls)

    mock_crawler_process.assert_called_once()
    
    assert isinstance(final_dict, dict)
    assert len(final_dict) == 2
    assert final_dict['http://test.com/page1'] == 'This is page one.'
    assert final_dict['http://test.com/page2'] == 'This is page two.'

def test_scrape_urls_with_no_urls():
    """
    Tests the edge case where an empty list of URLs is provided.
    """
    result = scraper.scrape_urls([])
    assert result == {}
