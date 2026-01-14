import os
import logging
import boto3
from datetime import datetime, timedelta
from dotenv import load_dotenv
import shutil
from modules.extract_function import extract_function
from modules.load_function import load_function
from modules.logging_function import logging_function


# 1. Setup - Variables must be defined BEFORE use
load_dotenv()
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
logs_dir = 'logs'


logger = logging_function(logs_dir, timestamp)
logger.info("--- ETL Pipeline Started ---")


# 3. Parameters
today_midnight = datetime.now()
last_week_midnight = today_midnight - timedelta(days=7)

url = 'https://analytics.eu.amplitude.com/api/2/export'
params = {
    'start': last_week_midnight.strftime('%Y%m%dT%H'),
    'end': today_midnight.strftime('%Y%m%dT%H')
}

api_key = os.getenv("AMP_API_KEY")
secret_key = os.getenv("AMP_SECRET_KEY")
zip_data_dir = 'zipdata'
extract_pathbase = 'extractzip'
extractgz_pathbase = 'data'

# 4. Execution
extract_function(url, params, 3, timestamp, api_key, secret_key, 
                 zip_data_dir, extract_pathbase, extractgz_pathbase)

# 5. AWS S3 Upload
aws_access_key = os.getenv('AWS_ACCESS_KEY')
aws_secret_key = os.getenv('AWS_SECRET_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

s3_client = boto3.client(
    's3',
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key
)

load_function(extractgz_pathbase, aws_bucket_name, s3_client)

# Cleaning up file directories
shutil.rmtree(extract_pathbase) 
shutil.rmtree(zip_data_dir)
