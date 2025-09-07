import pytest
from src.rag_core.generator import Generator
from src.processing.text_processor import Document


MOCK_CONTEXT_DOCS = [
    Document(page_content="The sky is blue because of Rayleigh scattering.", metadata={"source_url": "science.com/sky"}),
    Document(page_content="The ocean is also blue.", metadata={"source_url": "science.com/ocean"}),
]


def test_generator_build_prompt():
    """
    A pure unit test for the prompt building logic. No mocking needed.
    This is a high-value test.
    """
    
    prompt = Generator._build_prompt(None, "Why is the sky blue?", MOCK_CONTEXT_DOCS)

    assert "Why is the sky blue?" in prompt
    assert "Source URL: science.com/sky" in prompt
    assert "Rayleigh scattering" in prompt
    assert "You are an AI assistant." in prompt

def test_generator_answer_parsing(mocker):
    """
    Tests that the generator can correctly parse the answer from the LLM's raw output.
    """
    
    mocker.patch('src.rag_core.generator.AutoModelForCausalLM.from_pretrained')
    mocker.patch('src.rag_core.generator.AutoTokenizer.from_pretrained')

    generator = Generator()

    generator.load_model()

    raw_llm_output = """
    **Instruction:** ...
    **Context:** ...
    **User Query:** Why is the sky blue?
    **Answer:**
    The sky appears blue due to a phenomenon called Rayleigh scattering.
    """

    mocker.patch.object(generator.model, 'generate')
    mocker.patch.object(generator.tokenizer, 'decode', return_value=raw_llm_output)

    answer = generator.generate_answer("Why is the sky blue?", MOCK_CONTEXT_DOCS)

    expected_answer = "The sky appears blue due to a phenomenon called Rayleigh scattering."
    assert answer.strip() == expected_answer

def test_generator_handles_no_context():
    """Tests that the generator gives a fallback answer if no context is provided."""

    generator = Generator()

    generator.load_model()
    
    answer = generator.generate_answer("Any query", [])
    assert "could not find any relevant information" in answer.lower()