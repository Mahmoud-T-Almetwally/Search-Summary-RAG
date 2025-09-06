from typing import List, Dict
from dataclasses import dataclass
from src import config
import logging

from langchain.text_splitter import RecursiveCharacterTextSplitter


logger = logging.getLogger(__name__)

@dataclass
class Document:
    """A simple data class to hold a chunk of text and its metadata."""
    page_content: str
    metadata: Dict[str, str]

def process_scraped_data(scraped_content: Dict[str, str]) -> List[Document]:
    """
    Processes the raw scraped text by chunking it into smaller documents.

    Args:
        scraped_content: A dictionary where keys are URLs and values are the
                         raw text content from those URLs.

    Returns:
        A list of Document objects, where each object is a chunk of the
        original text with its source URL as metadata.
    """

    logger.info(f"Processing {len(scraped_content)} scraped documents...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True,
    )

    all_chunks = []
    for url, text in scraped_content.items():
        if not text:
            continue 
        
        chunks = text_splitter.split_text(text)
        
        for i, chunk_text in enumerate(chunks):
            doc = Document(
                page_content=chunk_text,
                metadata={"source_url": url, "chunk_index": i}
            )
            all_chunks.append(doc)
    
    logger.info(f"Created {len(all_chunks)} text chunks from the documents.")
    return all_chunks