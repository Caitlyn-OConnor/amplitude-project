import os    
import gzip        
import shutil 

def gunzip_function(extract_pathbase, extractgz_pathbase):
    '''
    Docstring for gunzip_function
    
    :param extract_pathbase: where the unzipped data from the unzip function is outputted = ideally 'extractzip'
    :param extractgz_pathbase: where the final extracted jsons are loaded into = ideally 'data'
    :param zip_data_dir: where the zip files are saved from the api call = ideally 'zipdata'
    '''
    # Ensure the output directory exists before writing to it
    os.makedirs(extractgz_pathbase, exist_ok=True)
    
    # First go one level into the folder by getting the result of what is in the base folder
    extract_subfolder = os.listdir(extract_pathbase)[0]
    # if you wanted to not assume you only get one subfolder, you would loop through all the subfolders like:
    # for extract_subfolder in os.listdir(extract_pathbase):
        # do rest of the code

    # Overwrite extract_pathbase with the subfolder attached e.g. 'extractzip/100011471'
    extract_fullpathbase = os.path.join(extract_pathbase,extract_subfolder)

    # Get full list of filenames in the subfolder of extractzip, contained in extract_pathbase
    extract_filenames = os.listdir(extract_fullpathbase)


    for filename in extract_filenames: # Looping through each filename in data folder
        if not filename.endswith('.gz'):
            continue # Skip any non gzip files in data -- we don't want to extract a normal file
        filepath = os.path.join(extract_fullpathbase, filename) # Constructing relative path of that file as string, escape the backslash to make it a single backslash
       
        output_filename = filename[:-3] # returns the string except for the last 3 characters, which is .gz

        output_path = os.path.join(extractgz_pathbase, output_filename) # construct desired output path
        with gzip.open(filepath, 'rb') as gz_file, open(output_path, 'wb') as out_file:
            shutil.copyfileobj(gz_file, out_file)

