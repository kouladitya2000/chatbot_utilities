from azure.storage.blob import BlobServiceClient
import os


def download_blob(sturl,stkey,cname,blobname,path):
    STORAGEACCOUNTURL = sturl
    STORAGEACCOUNTKEY = stkey
    CONTAINERNAME = cname
    BLOBNAME = blobname
    path_blob = path+blobname

    DESTINATION_PATH = os.path.expanduser(path_blob)

    # Create a BlobServiceClient instance
    blob_service_client_instance = BlobServiceClient(
        account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)

    # Get a BlobClient instance for the specified blob
    blob_client_instance = blob_service_client_instance.get_blob_client(
        CONTAINERNAME, BLOBNAME)

    # Download the blob to the local file
    with open(DESTINATION_PATH, "wb") as local_file:
        blob_data = blob_client_instance.download_blob()
        blob_data.readinto(local_file)

    return (f"Audio file downloaded and saved to {DESTINATION_PATH}")



def upload_blob(sturl,stkey,cname,blobname,path):
    STORAGEACCOUNTURL = sturl
    STORAGEACCOUNTKEY = stkey
    CONTAINERNAME = cname
    BLOBNAME = blobname
    path_blob = path+blobname

    blob_service_client_instance = BlobServiceClient(
        account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY)

    blob_client_instance = blob_service_client_instance.get_blob_client(
        CONTAINERNAME, BLOBNAME)

    # Upload the file to the blob
    with open(path_blob, "rb") as data:
        blob_client_instance.upload_blob(data, overwrite=True)

    return (f"File '{path_blob}' uploaded to '{CONTAINERNAME}/{BLOBNAME}'")

