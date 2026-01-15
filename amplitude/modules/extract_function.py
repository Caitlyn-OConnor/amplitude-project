# Load environment variables
import requests
import os
import time
import logging           
from modules.gunzip_function import gunzip_function
from modules.unzip_function import unzip_function

logger = logging.getLogger()

def extract_function(url, params ,max_attempts, timestamp, api_key, secret_key, zip_data_dir, extract_pathbase, extractgz_pathbase):
    '''
    Docstring for extract_function
    
    :param url: Description
    :param max_attempts: Description
    :param timestamp: Description
    :param api_key: Description
    :param secret_key: Description
    :param zip_data_dir: Description
    :param extract_pathbase: Description
    :param extractgz_pathbase: Description
    '''

    # making the max api calls 3 in case of system errors
    attempt = 1

    while attempt <= max_attempts:
        print(f"Attempt {attempt}...")
        logger.info(f"Attempt {attempt} for Amplitude export...")
        response = requests.get(url, params=params, auth=(api_key, secret_key), timeout = 45)

        if response.status_code == 200: #if api call successful
            try:
                # 1. Create directory if it doesn't exist
                os.makedirs(zip_data_dir, exist_ok=True)
                # 2. Define filename with .zip extension using time of api call
                filepath = os.path.join(zip_data_dir, f'{timestamp}.zip')


                os.makedirs(extract_pathbase, exist_ok=True)
                os.makedirs(extractgz_pathbase, exist_ok=True)


                # 3. Write binary content ('wb') to the file, save the zip files
                with open(filepath, 'wb') as file:
                    file.write(response.content)
        
                print(f'Zip file saved successfully: {filepath}')

               
                unzip_function(zip_data_dir, extract_pathbase)
                gunzip_function(extract_pathbase, extractgz_pathbase)
                
                logger.info(f"Zip file saved successfully: {filepath}")
                break  # Exit loop on success of zip saving

            except Exception as e:
                print(f"Error saving zip file: {e}")
                logger.error(f'An error occurred on saving the zip file {e}')    
                break # Exit loop on error saving 
                
        elif response.status_code >= 500:
            # Server error - wait 10s and retry
            print(f"Server error {response.status_code}. Retrying in 10s...")
            logger.warning(response.reason)
            time.sleep(10)
            attempt += 1
        else:
            # Client error (401, 403, 404) - don't retry
            print(f"Client error {response.status_code}: {response.reason}")
            print(response.text)
            logger.error(response.reason)
            break

    if attempt > max_attempts:
        print("Maximum attempts reached. Download failed.")
        logger.error(response.reason)

