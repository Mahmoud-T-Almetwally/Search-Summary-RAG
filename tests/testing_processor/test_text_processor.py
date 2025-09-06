import pytest
from src.processing.text_processor import process_scraped_data, Document
from src import config

MOCK_TEXT_LONG = "This is the first sentence. " * 50 + "This is the second sentence. " * 50 + "This is the third sentence. " * 50

MOCK_TEXT_SHORT = "This is a single short document."

MOCK_SCRAPED_CONTENT = {
    "http://example.com/long_article": MOCK_TEXT_LONG,
    "http://example.com/short_article": MOCK_TEXT_SHORT,
    "http://example.com/empty_article": "",
}

def test_process_scraped_data_happy_path():
    """
    Tests the standard functionality: chunking long text and creating Document objects.
    """

    documents = process_scraped_data(MOCK_SCRAPED_CONTENT)

    assert isinstance(documents, list)
    assert len(documents) > 1  
    assert all(isinstance(doc, Document) for doc in documents)

    for doc in documents:
        assert len(doc.page_content) <= config.CHUNK_SIZE
        assert isinstance(doc.page_content, str)
        assert len(doc.page_content) > 0

def test_metadata_integrity():
    """
    CRITICAL TEST: Ensures that metadata (source URL and chunk index) is correct.
    """

    documents = process_scraped_data(MOCK_SCRAPED_CONTENT)

    long_article_chunks = [d for d in documents if d.metadata['source_url'] == "http://example.com/long_article"]
    short_article_chunks = [d for d in documents if d.metadata['source_url'] == "http://example.com/short_article"]

    assert len(long_article_chunks) > 1
    
    expected_indices = list(range(len(long_article_chunks)))
    actual_indices = sorted([d.metadata['chunk_index'] for d in long_article_chunks])
    assert actual_indices == expected_indices

    assert len(short_article_chunks) == 1
    assert short_article_chunks[0].metadata['chunk_index'] == 0

def test_short_text_handling():
    """
    Tests that text shorter than the chunk size results in a single document.
    """

    short_content = {"http://example.com/short": MOCK_TEXT_SHORT}
    documents = process_scraped_data(short_content)

    assert len(documents) == 1
    assert documents[0].page_content == MOCK_TEXT_SHORT

def test_edge_case_empty_and_invalid_input():
    """
    Tests that the function handles empty inputs gracefully.
    """
    
    assert process_scraped_data({}) == []

    content_with_empty = {
        "http://example.com/real": "Some text.",
        "http://example.com/empty": ""
    }

    documents = process_scraped_data(content_with_empty)

    assert len(documents) == 1
    assert documents[0].metadata['source_url'] == "http://example.com/real"

def test_respects_config_values(mocker):
    """
    Tests if the text splitter correctly uses CHUNK_SIZE from the config.
    We use pytest-mocker to temporarily change the config value for this test.
    """

    mocker.patch('src.processing.text_processor.config.CHUNK_SIZE', 50)
    mocker.patch('src.processing.text_processor.config.CHUNK_OVERLAP', 10)
    
    content = {"http://test.com": MOCK_TEXT_LONG}
    documents = process_scraped_data(content)
    
    assert len(documents) > 10 
    for doc in documents:
        assert len(doc.page_content) <= 50