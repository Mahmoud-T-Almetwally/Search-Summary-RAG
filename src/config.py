import logging
import logging.config
import sys
import torch
import os
from dotenv import load_dotenv

SERPAPI_API_KEY = ''

HF_HOME = './model_cache'

DEVICE = 'gpu:0' if torch.cuda.is_available() else 'cpu'

MODEL_ID = ''

EMBEDDING_MODEL_ID = 'all-MiniLM-L6-v2'

CHUNK_SIZE = 1000

CHUNK_OVERLAP = 200

NUM_RETRIEVED_DOCS = 5

def load_env_values():
    """
    Loads & Ensures the needed environment variables are defined, otherwise raises a VauleError exception.
    Some Variables have fallback defaults defined in 'src.config', but some must be set in code (e.g. 'src.config.DEVICE'), while others are defined only in '.env'.
    """
    load_dotenv()

    global SERPAPI_API_KEY
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY not found in .env file or in 'src.config'. Please add it.")
    
    global HF_HOME
    HF_HOME = os.getenv("HF_HOME") if not os.getenv("HF_HOME") else HF_HOME 

    if not HF_HOME:
        raise ValueError("HF_HOME not found in .env file or in 'src.config'. Please add it.")
    
    global MODEL_ID
    MODEL_ID = os.getenv("MODEL_ID") if not os.getenv("MODEL_ID") else MODEL_ID 

    if not MODEL_ID:
        raise ValueError("MODEL_ID not found in .env file or in 'src.config'. Please add it.")
    
    global EMBEDDING_MODEL_ID
    EMBEDDING_MODEL_ID = os.getenv("EMBEDDING_MODEL_ID") if not os.getenv("EMBEDDING_MODEL_ID") else EMBEDDING_MODEL_ID 

    if not EMBEDDING_MODEL_ID:
        raise ValueError("EMBEDDING_MODEL_ID not found in .env file or in 'src.config'. Please add it.")
    
    global CHUNK_SIZE
    CHUNK_SIZE = os.getenv("CHUNK_SIZE") if not os.getenv("CHUNK_SIZE") else CHUNK_SIZE 

    if not CHUNK_SIZE:
        raise ValueError("CHUNK_SIZE not found in .env file or in 'src.config'. Please add it.")
    
    global CHUNK_OVERLAP
    CHUNK_OVERLAP = os.getenv("CHUNK_OVERLAP") if not os.getenv("CHUNK_OVERLAP") else CHUNK_OVERLAP

    if not CHUNK_OVERLAP:
        raise ValueError("CHUNK_OVERLAP not found in .env file or in 'src.config'. Please add it.")
    
    if (not DEVICE) or (DEVICE != 'gpu:0' and DEVICE != 'cpu'):
        raise ValueError("DEVICE is not set in 'config.py' file or has an invalid value.")


def setup_logging():
    """
    Configures logging for the entire application.
    """
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] - [%(name)s] - %(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'level': 'DEBUG',
                'stream': sys.stdout,
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'standard',
                'filename': 'app.log',
                'maxBytes': 10485760,  
                'backupCount': 5,
                'level': 'INFO',
            },
        },
        'loggers': {
            '': { 
                'handlers': ['console', 'file'],
                'level': 'DEBUG',
                'propagate': True
            }
        }
    }
    logging.config.dictConfig(LOGGING_CONFIG)