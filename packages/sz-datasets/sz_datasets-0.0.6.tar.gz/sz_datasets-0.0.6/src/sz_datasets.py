from os import makedirs
from os.path import isdir, basename
from google.cloud import storage
from sklearn.model_selection import train_test_split

# if your environment was authenticated, the default config will be picked up
# storage_client = storage.Client() # comment this line if you want to use service account
class SZ_datasets:

  def download_data_gcs(path_to_save_data = None,creds_json = None):

    if path_to_save_data is None:
      raise Exception(f"path to save the data is missing")
    
    if creds_json is None:
      raise Exception(f"Authentication file is missing")
    
    # uncomment the line below if you have a service account json
    storage_client = storage.Client.from_service_account_json(creds_json)
    bucket_name = 'sz_datasets'
    # prefix = 'datasets'
    dst_path = path_to_save_data

    if isdir(dst_path) == False:
        makedirs(dst_path)

    bucket = storage_client.bucket(bucket_name=bucket_name)
    blobs = bucket.list_blobs()  # Get list of files

    for blob in blobs:
      
      if blob.name == 'datasets/':
        continue
      
      blob_name = blob.name 
      print(blob_name)
      dst_file_name = blob_name.replace('FOLDER1/FOLDER2', dst_path) #.replace('FOLDER1/FOLDER2', 'D:\\my_blob_data') 
      # extract the final directory and create it in the destination path if it does not exist
      dst_dir = dst_file_name.replace('/' + basename(dst_file_name), '')

      if isdir(dst_dir) == False:
          makedirs(dst_dir)

      # download the blob object
      blob.download_to_filename(dst_file_name)

  def split_datasets(dataset,label_col_name : str, test_split_ratio: int = 0.20, random_state: int = None , val_split_ratio: int = None):
  
    if test_split_ratio > 1 :
      raise Exception(f"test split ratio must be less than 0.30")

    if val_split_ratio > 1 :
      raise Exception(f"val split ratio must be less or equal to  0.20")
      
    dataset = dataset.dropna(subset = [label_col_name])
      
      
    if random_state is None:
      random_state = 42

    if val_split_ratio is None:

      train, test = train_test_split(dataset, test_size = test_split_ratio, stratify=dataset[label_col_name],random_state = random_state) 
      return train, test

    else:
      train, test = train_test_split(dataset, test_size = test_split_ratio, stratify=dataset[label_col_name],random_state = random_state) 

      train, eval = train_test_split(train, test_size = test_split_ratio, stratify=train[label_col_name],random_state = random_state) 
      return train.reset_index(drop = True), test.reset_index(drop = True), eval.reset_index(drop = True)
       