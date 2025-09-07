import pytest
from src.processing.text_processor import process_scraped_data, Document
from src.scraping.scraper import scrape_urls

MOCK_SEARCH_URLS = ["http://example.com/page1", "http://example.com/page2"]
MOCK_SCRAPED_CONTENT = {
    "http://example.com/page1": "This is the full text content of the first page. It is long enough to be chunked into multiple pieces.",
    "http://example.com/page2": "This is the content of the second page."
}


def test_data_ingestion_pipeline_integration(mocker):
    """
    Tests the integration of scraping and text processing.
    It verifies that the output of the scraper is correctly handled by the processor.
    """

    mock_scrape_urls = mocker.patch('src.main.scrape_urls')

    mock_scrape_urls.return_value = MOCK_SCRAPED_CONTENT

    scraped_content = mock_scrape_urls(MOCK_SEARCH_URLS)

    documents = process_scraped_data(scraped_content)

    assert len(documents) > 1
    assert all(isinstance(doc, Document) for doc in documents)

    found_url1 = False
    found_url2 = False
    for doc in documents:
        if doc.metadata['source_url'] == "http://example.com/page1":
            found_url1 = True
        if doc.metadata['source_url'] == "http://example.com/page2":
            found_url2 = True
    
    assert found_url1 and found_url2
    
    assert "content of the first page" in documents[0].page_content