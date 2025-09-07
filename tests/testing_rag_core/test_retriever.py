import pytest
from src.rag_core.retriever import Retriever
from src.processing.text_processor import Document


MOCK_DOCUMENTS = [
    Document(page_content="Microservices are a popular architectural style.", metadata={"source_url": "url1"}),
    Document(page_content="Python is a versatile programming language.", metadata={"source_url": "url2"}),
    Document(page_content="A monolith contains all functionality in one codebase.", metadata={"source_url": "url3"}),
]

def test_retriever_initialization(mocker):
    """Tests that the Retriever initializes the embedding model on creation."""
    
    mock_embeddings = mocker.patch('src.rag_core.retriever.HuggingFaceEmbeddings')
    
    retriever = Retriever()

    retriever.load_model()
    
    mock_embeddings.assert_called_once()
    assert retriever.vector_store is None

def test_retrieve_context_before_build():
    """Tests that retrieving context before building the store fails gracefully."""

    retriever = Retriever()
    
    results = retriever.retrieve_context("test query")
    assert results == []

def test_build_vector_store_and_retrieve(mocker):
    """
    Tests the end-to-end flow of building a vector store and retrieving context.
    This is an integration test for the Retriever class.
    """
    
    mocker.patch('src.rag_core.retriever.HuggingFaceEmbeddings')
    
    mock_faiss = mocker.patch('src.rag_core.retriever.FAISS')
    
    from langchain.schema import Document as LangChainDocument
    mock_faiss.from_texts.return_value.similarity_search.return_value = [
        LangChainDocument(page_content=doc.page_content, metadata=doc.metadata) for doc in MOCK_DOCUMENTS[:2]
    ]

    retriever = Retriever()
    
    retriever.build_vector_store(MOCK_DOCUMENTS)
    
    retrieved_docs = retriever.retrieve_context("What are microservices?")

    mock_faiss.from_texts.assert_called_once()
    
    mock_faiss.from_texts.return_value.similarity_search.assert_called_once_with(
        query="What are microservices?",
        k=pytest.approx(5)
    )
    
    assert len(retrieved_docs) == 2
    assert retrieved_docs[0].page_content == "Microservices are a popular architectural style."
    assert retrieved_docs[0].metadata["source_url"] == "url1"