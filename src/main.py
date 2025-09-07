import logging
from src.scraping.scraper import scrape_urls
from src.api.search_client import get_search_results
from src.processing.text_processor import process_scraped_data
from src.rag_core.retriever import Retriever
from src.rag_core.generator import Generator
from src.config import setup_logging, load_env_values


setup_logging()

def pipeline(query: str, retriever: Retriever, generator: Generator):
    urls_to_scrape = get_search_results(query=query)
     
    scraped_data = scrape_urls(urls=urls_to_scrape)
    
    documents = process_scraped_data(scraped_content=scraped_data)

    retriever.build_vector_store(documents=documents)

    context_docs = retriever.retrieve_context(query=query)

    source_urls = set(doc.metadata['source_url'] for doc in context_docs)

    final_answer = generator.generate_answer(query=query, context_docs=context_docs)

    return final_answer, source_urls

def main():

    try:
        load_env_values()
    except ValueError as e:
        logger.error(msg=f"Error loading .env variables, original message: {e}")
        logger.info("Application Shutting Down...")
        return
    
    user_input = input("Your Search Query: ")

    final_answer, source_urls = pipeline(query=user_input, retriever=retriever, generator=generator)

    print("\n--- FINAL ANSWER ---")
    print(final_answer)
    print("\n--- SOURCES ---")
    for url in source_urls:
        print(f"- {url}")
    print("------------------\n")

    logger.info("Application finished.")


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Application starting up...")
    retriever = Retriever()
    generator = Generator()
    retriever.load_model()
    generator.load_model()
    main()