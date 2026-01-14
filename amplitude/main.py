from modules.gunzip_function import gunzip_function
from modules.unzip_function import unzip_function
from modules.extract_function import extract_function
from modules.load_function import load_function
import logging    
import os
import requests
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta
import time
import logging    
import boto3


logs_dir = 'logs'
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


filename = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
load_dotenv()


today_midnight = datetime.now()
last_week_midnight = today_midnight - timedelta(days=7)

url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': last_week_midnight.strftime('%Y%m%dT%H'),
    'end': today_midnight.strftime('%Y%m%dT%H')
}


api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")

max_attempts=3
zip_data_dir = 'zipdata'
extract_pathbase = 'extractzip'
extractgz_pathbase = 'data'

extract_function(url, 
                 params, 
                 max_attempts, 
                 filename, 
                 api_key, 
                 secret_key, 
                 zip_data_dir, 
                 extract_pathbase, 
                 extractgz_pathbase)


# loading...

aws_access_key=os.getenv('AWS_ACCESS_KEY')
aws_secret_key=os.getenv('AWS_SECRET_KEY')
aws_bucket_name=os.getenv('AWS_BUCKET_NAME')

# Create S3 Client using AWS Credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

load_function(extractgz_pathbase, 
              aws_bucket_name, 
              s3_client)