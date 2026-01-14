import os   
import zipfile     


def unzip_function(zip_data_dir, extract_pathbase):
    '''
    Docstring for unzip_function
    
    :param zip_data_dir: where the extracted data is being located after api call
    :param extract_pathbase: where the unzipped data will be outputted to
    '''

    data_filenames = os.listdir(zip_data_dir)

    for file in data_filenames: # Looping through each filename in data folder
        if not file.endswith('.zip'):
            continue # Skip any non zip files in data -- we don't want to extract a normal file (robust check)
        filepath = zip_data_dir + r'/' + file # Constructing relative path of that file as string
        with zipfile.ZipFile(filepath, "r") as zip_ref: # Magic step to read the zip file at the relative filepath
            zip_ref.extractall(extract_pathbase) # Extract the contents to the extractzip folder