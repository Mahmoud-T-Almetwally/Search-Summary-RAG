import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from typing import List

import logging

from src import config
from src.processing.text_processor import Document


logger = logging.getLogger(__name__)

class Generator:
    """
    Manages a locally-run Hugging Face model for text generation.
    """

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Generator, cls).__new__(cls)
            cls._instance.model = None
            cls._instance.tokenizer = None
        else:
            logger.warning(f"generator already defined, 'Generator' class should only be instantiated once.")

        return cls._instance

    def load_model(self):
        """
        Initializes the Generator by loading the LLM model.
        This is a resource-intensive operation and should be done only once.
        """
        if self.model is None:
            logger.info("Initializing local generator...")
            self.device = config.DEVICE
            self.model_id = config.MODEL_ID

            try:
                bnb_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16,
                    llm_int8_enable_fp32_cpu_offload=True
                )

                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_id,
                    quantization_config=bnb_config,
                    cache_dir=str(config.HF_HOME),
                    device_map="auto"
                )

                self.tokenizer = AutoTokenizer.from_pretrained(self.model_id, cache_dir=str(config.HF_HOME))
            except Exception as e :
                logger.error(f"Could Not load Generator Model, original error message: {e}")
                return

            logger.info("Model and tokenizer loaded successfully.")
        else:
            logger.warning(f"Generator Model already loaded, 'generator.load_model' should only be called once.")


    def _build_prompt(self, query: str, context_docs: List[Document]) -> str:
        """
        Builds a structured prompt for the LLM using the retrieved context.
        """
        
        context_str = "\n\n".join([f"Source URL: {doc.metadata['source_url']}\nContent: {doc.page_content}" for doc in context_docs])

        prompt = f"""
        **Instruction:**
        You are an AI assistant. Your task is to provide a clear and concise answer to the following user query based ONLY on the provided context.
        Do not use any external knowledge. If the context does not contain the answer, state that you cannot answer based on the information given.
        Cite the source URL for the information you use.

        **Context:**
        {context_str}

        **User Query:**
        {query}

        **Answer:**
        """
        return prompt

    def generate_answer(self, query: str, context_docs: List[Document]) -> str:
        """
        Generates an answer based on the query and the provided context documents.
        """
        if not context_docs:
            return "I could not find any relevant information to answer your query."

        prompt = self._build_prompt(query, context_docs)

        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=4096, truncation=True).to(self.device)

        outputs = self.model.generate(**inputs, max_new_tokens=512, pad_token_id=self.tokenizer.eos_token_id)
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        answer_marker = "**Answer:**"
        answer_position = generated_text.find(answer_marker)
        if answer_position != -1:
            return generated_text[answer_position + len(answer_marker):].strip()
        
        return generated_text.strip()