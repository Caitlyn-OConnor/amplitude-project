# Load environment variables
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
import time
import logging        
import zipfile     
import gzip        
import shutil     
import tempfile    

logs_dir = 'logs'
filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

# making sure the log directory exists before creating one
if os.path.exists(logs_dir):
    pass
else:
    os.mkdir(logs_dir)


# creating log filename
log_filename = f"logs/{filename}.log"

# configured log files
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename=log_filename
)

# creating logger variable
logger = logging.getLogger()

load_dotenv()

url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': '20260101T00',
    'end': '20260108T00'
}

api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

# making the max api calls 3 in case of system errors
max_attempts = 3
attempt = 0

while attempt <= max_attempts:
    print(f"Attempt {attempt}...")
    response = requests.get(url, params=params, auth=(api_key, secret_key))

    if response.status_code == 200: #if api call successful
        try:
            # 1. Create directory if it doesn't exist
            zip_data_dir = "zipdata"

            os.makedirs(zip_data_dir, exist_ok=True)
            
            # 2. Define filename with .zip extension using time of api call
            filepath = f'zipdata/{filename}.zip'

            extract_pathbase = 'extractzip'
            if not os.path.exists(extract_pathbase):
                os.mkdir(extract_pathbase)

            extractgz_pathbase = 'data'
            if not os.path.exists(extractgz_pathbase):
                os.mkdir(extractgz_pathbase)

            # 3. Write binary content ('wb') to the file, save the zip files
            with open(filepath, 'wb') as file:
                file.write(response.content)
    
            print(f'Zip file saved successfully: {filepath}')

            # Get a Python list of all filenames (with extension) in the data_pathbase folder
            data_filenames = os.listdir(zip_data_dir)

            for file in data_filenames: # Looping through each filename in data folder
                if not file.endswith('.zip'):
                    continue # Skip any non zip files in data -- we don't want to extract a normal file (robust check)
                filepath = zip_data_dir + r'/' + file # Constructing relative path of that file as string
                with zipfile.ZipFile(filepath, "r") as zip_ref: # Magic step to read the zip file at the relative filepath
                    zip_ref.extractall(extract_pathbase) # Extract the contents to the extractzip folder



            # First go one level into the folder by getting the result of what is in the base folder
            extract_subfolder = os.listdir(extract_pathbase)[0]
            # if you wanted to not assume you only get one subfolder, you would loop through all the subfolders like:
            # for extract_subfolder in os.listdir(extract_pathbase):
                # do rest of the code

            # Overwrite extract_pathbase with the subfolder attached e.g. 'extractzip/100011471'
            extract_fullpathbase = os.path.join(extract_pathbase,extract_subfolder)

            # Get full list of filenames in the subfolder of extractzip, contained in extract_pathbase
            extract_filenames = os.listdir(extract_fullpathbase)
            # print(extract_filenames)

            for filename in extract_filenames: # Looping through each filename in data folder
                if not filename.endswith('.gz'):
                    continue # Skip any non gzip files in data -- we don't want to extract a normal file (robust check)
                filepath = os.path.join(extract_fullpathbase, filename) # Constructing relative path of that file as string, escape the backslash to make it a single backslash
                # print(filepath) # Validate last step
                output_filename = filename[:-3] # returns the string except for the last 3 characters, which is .gz
                output_path = extractgz_pathbase + r'/' + output_filename # construct desired output path
                with gzip.open(filepath, 'rb') as gz_file, open(output_path, 'wb') as out_file:
                    shutil.copyfileobj(gz_file, out_file)

            # Then delete the previous contents of used files
            # shutil.rmtree(data_pathbase)
            shutil.rmtree(extract_pathbase) # Remove file AFTER finishing extracting. Alternatively, can loop through os.listdir and use os.remove on each filename individually for more control instead of using shutil.rmtree to delete the full folder and contents all at once. E.g. if you want to ensure you only remove zip files, and not blanket remove everything
            shutil.rmtree(zip_data_dir)

            logger.info(f'Download successful and saved successfully at {filename} :)')  
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

