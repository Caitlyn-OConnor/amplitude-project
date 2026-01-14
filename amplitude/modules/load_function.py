# Load libraries
import boto3
import os


def load_function(extractgz_pathbase, aws_bucket_name, s3_client):
    '''
    Docstring for load_function
    
    :param extractgz_pathbase: Description
    :param aws_bucket_name: Description
    '''

    json_files = [f for f in os.listdir(extractgz_pathbase) if f.endswith('.json')]

    if json_files:
        print(f"Found {len(json_files)} files. Starting upload...")
        
        for file in json_files:
            local_file_path = os.path.join(extractgz_pathbase, file)
            aws_file_destination = f"python-import/{file}"
            
            try:
                # Upload to S3
                s3_client.upload_file(local_file_path, aws_bucket_name, aws_file_destination)
                
                # Delete local file AFTER successful upload
                os.remove(local_file_path) 
                print(f'Successfully uploaded and removed {file} :)')

            except Exception as e:
                print(f'Upload error for {file}: {e}')
    else:
        # This runs if json_files is empty
        print('No JSON files found in the directory. Nothing to upload.')
