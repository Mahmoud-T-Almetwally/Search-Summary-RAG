import pytest
from src import main
from src.processing.text_processor import Document

MOCK_QUERY = "What is Python?"

MOCK_SEARCH_RESULTS = [{'link': 'http://python.org/about'}]
MOCK_SCRAPED_CONTENT = {'http://python.org/about': 'Python is a high-level, general-purpose programming language.'}
MOCK_PROCESSED_DOCS = [Document(page_content='Python is a high-level, general-purpose programming language.', metadata={'source_url': 'http://python.org/about'})]
MOCK_FINAL_ANSWER = "Based on the context, Python is a high-level programming language."


def test_full_rag_pipeline_end_to_end(mocker):
    """
    An end-to-end test of the entire run_pipeline function.
    It mocks all external services and slow models to test the application's
    internal logic and data flow from start to finish.
    """

    mock_get_search_results = mocker.patch('src.main.get_search_results')
    mock_get_search_results.return_value = MOCK_SEARCH_RESULTS

    mock_scrape_urls = mocker.patch('src.main.scrape_urls')
    mock_scrape_urls.return_value = MOCK_SCRAPED_CONTENT

    mock_process_scraped_data = mocker.patch('src.main.process_scraped_data')
    mock_process_scraped_data.return_value = MOCK_PROCESSED_DOCS
    
    mock_retriever_instance = mocker.patch('src.main.Retriever').return_value
    mock_retriever_instance.build_vector_store.return_value = None
    mock_retriever_instance.retrieve_context.return_value = MOCK_PROCESSED_DOCS

    mock_generator_instance = mocker.patch('src.main.Generator').return_value
    mock_generator_instance.generate_answer.return_value = MOCK_FINAL_ANSWER

    answer, source_urls = main.pipeline(
        query=MOCK_QUERY,
        retriever=mock_retriever_instance,
        generator=mock_generator_instance
    )

    assert MOCK_FINAL_ANSWER in answer
    assert "http://python.org/about" in source_urls

    mock_get_search_results.assert_called_once_with(query=MOCK_QUERY)
    mock_scrape_urls.assert_called_once_with(urls=MOCK_SEARCH_RESULTS)
    mock_retriever_instance.retrieve_context.assert_called_once_with(query=MOCK_QUERY)
    mock_generator_instance.generate_answer.assert_called_once_with(query=MOCK_QUERY, context_docs=MOCK_PROCESSED_DOCS)