from typing import List
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

import logging

from src import config
from src.processing.text_processor import Document


logger = logging.getLogger(__name__)

class Retriever:
    """
    Manages the creation of text embeddings and the retrieval of relevant documents.
    """

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Retriever, cls).__new__(cls)
            cls._instance.embedding_model = None
        else:
            logger.warning(f"retriever already defined, 'Retriever' class should only be instantiated once.")
        return cls._instance
    
    def load_model(self):
        """
        Initializes the Retriever by loading the embedding model.
        This is a resource-intensive operation and should be done only once.
        """

        if self.embedding_model is None:

            logger.info("Initializing Retriever and loading embedding model...")

            try:
                self.embedding_model = HuggingFaceEmbeddings(
                    model_name=config.EMBEDDING_MODEL_ID,
                    model_kwargs={'device': config.DEVICE},
                    cache_folder=str(config.HF_HOME)
                )
            except Exception as e :
                logger.error(f'Could Not load Retriever Model, original error message: {e}')
                return

            self.vector_store = None

            logger.info("Embedding model loaded.")
        
        else:
            logger.warning(f"Retriever Model already loaded, 'retriever.load_model' should only be called once.")

    def build_vector_store(self, documents: List[Document]):
        """
        Builds the FAISS vector store from a list of processed documents.

        Args:
            documents: A list of Document objects from the text processor.
        """

        if not documents:
            logger.warning("No documents provided to build vector store.")
            return

        logger.info(f"Building vector store from {len(documents)} document chunks...")
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        self.vector_store = FAISS.from_texts(
            texts=texts,
            embedding=self.embedding_model,
            metadatas=metadatas
        )

        logger.info("Vector store built successfully.")

    def retrieve_context(self, query: str) -> List[Document]:
        """
        Retrieves the most relevant document chunks for a given query.

        Args:
            query: The user's query string.

        Returns:
            A list of the most relevant Document objects.
        """
        if self.vector_store is None:
            logger.error("Vector store has not been built yet.")
            return []

        logger.info(f"Retrieving context for query: '{query}'...")
        retrieved_docs = self.vector_store.similarity_search(
            query=query,
            k=config.NUM_RETRIEVED_DOCS
        )
        
        custom_docs = [
            Document(page_content=doc.page_content, metadata=doc.metadata)
            for doc in retrieved_docs
        ]
        
        logger.info(f"Retrieved {len(custom_docs)} relevant document chunks.")
        return custom_docs