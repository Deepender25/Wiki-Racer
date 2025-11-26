import logging
import os
from datetime import datetime

def setup_logger(name, log_dir="logs"):
    """
    Sets up a logger that writes to a file named with the current date.
    Each run will append to the day's log file, or we could make it unique per run.
    The user requested "separate files for each day".
    """
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Create a custom logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create handlers
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"{today_str}.log")
    
    # Check if handler already exists to avoid duplicate logs
    if not logger.handlers:
        # File Handler with UTF-8 encoding
        f_handler = logging.FileHandler(log_file, encoding='utf-8')
        f_handler.setLevel(logging.INFO)

        # Create formatters and add it to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(formatter)

        # Add handlers to the logger
        logger.addHandler(f_handler)
        
        # Console Handler
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.INFO)
        c_handler.setFormatter(formatter)
        logger.addHandler(c_handler)
        
        # Ensure stdout handles utf-8 on Windows
        if os.name == 'nt':
            import sys
            try:
                sys.stdout.reconfigure(encoding='utf-8')
            except AttributeError:
                # For older python versions or if reconfigure isn't available
                pass

    return logger
