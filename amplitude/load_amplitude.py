# Single JSON file upload to S3 with KMS key

# Load libraries
import boto3
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read .env file
aws_access_key=os.getenv('AWS_ACCESS_KEY')
aws_secret_key=os.getenv('AWS_SECRET_KEY')
aws_bucket_name=os.getenv('AWS_BUCKET_NAME')

# defining directory where the jsons are found
filepath = 'data'

# 1. Create a session using your specific profile name
session = boto3.Session(profile_name='amplitude_test') 
# 2. Create an S3 client from that session 
s3 = session.client('s3')

# get a list of jsons in data directory
json_files = [f for f in os.listdir(filepath) if f.endswith('.json')]

# 2. Use the list for your if/else logic
if json_files:
    print(f"Found {len(json_files)} files. Starting upload...")
    
    for file in json_files:
        local_file_path = os.path.join(filepath, file)
        aws_file_destination = f"python-import/{file}"
        
        try:
            # Upload to S3
            s3.upload_file(local_file_path, aws_bucket_name, aws_file_destination)
            
            # Delete local file AFTER successful upload
            os.remove(local_file_path) 
            print(f'Successfully uploaded and removed {file} :)')

        except Exception as e:
            print(f'Upload error for {file}: {e}')
else:
    # This runs if json_files is empty
    print('No JSON files found in the directory. Nothing to upload.')
