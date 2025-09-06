import logging
import logging.config
import sys
import os
from dotenv import load_dotenv

SERPAPI_API_KEY = ''

def load_env_values():
    """
    Ensure the needed environment variables are defined, otherwise raises a VauleError exception.
    """
    load_dotenv()

    global SERPAPI_API_KEY
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
    
    if not SERPAPI_API_KEY:
        raise ValueError("SERPAPI_API_KEY not found in .env file. Please add it.")

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