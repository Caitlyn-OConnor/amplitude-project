import os
import logging
from datetime import datetime

def logging_function(logs_dir, timestamp):
    '''
    Docstring for logging_function
    
    :param logs_dir: Description
    '''
    # 1. Create directory if it doesn't exist
    os.makedirs(logs_dir, exist_ok=True)
    
    # 2. Generate filename based on current time
    log_filename = os.path.join(logs_dir, f"{timestamp}.log")
    
    # 3. Configure logging
    log_filename = f"{logs_dir}/{timestamp}.log"
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename=log_filename
    )
    
    logger = logging.getLogger()
    return logger