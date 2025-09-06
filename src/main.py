import logging
from src.scraping.scraper import scrape_urls
from src.api.search_client import get_search_results
from src.config import setup_logging, load_env_values


setup_logging()

def main():

    logger = logging.getLogger(__name__)
    logger.info("Application starting up...")

    try:
        load_env_values()
    except ValueError as e:
        logger.error(msg=f"Error loading .env variables, original message: {e}")
        logger.info("Application Shutting Down...")
        return

    urls_to_scrape = get_search_results(query="") 
    scraped_data = scrape_urls(urls_to_scrape)
    
    if scraped_data:
        logger.info(f"Successfully scraped {len(scraped_data)} pages.")
    else:
        logger.warning("No data was scraped.")

    logger.info("Application finished.")


if __name__ == "__main__":
    main()