from azure.storage.blob import BlobServiceClient
import os
import requests, uuid, json
import azure.cognitiveservices.speech as speechsdk


def download_blob(sturl,stkey,cname,blobname,path):
    '''
       About:
       ---------
       Download a file from Blob Storage in Azure
        Return the difference in days between the current date and game release date.

        Parameter
        ---------
        sturl : str
            Release date in string format.
        stkey : str
            Key of the Storage account. HIGHLY Restricted
        cname : str
            Container name of the Storage account
        blobname : str
            Blob name to download
        path : str
            Path from which file to download
        

        Returns
        -------
        string

    
    '''

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
    '''
       About:
       ---------
       Upload a file to Blob Storage in Azure
        Return the difference in days between the current date and game release date.

        Parameter
        ---------
        sturl : str
            Release date in string format.
        stkey : str
            Key of the Storage account. HIGHLY Restricted
        cname : str
            Container name of the Storage account
        blobname : str
            Blob name to upload
        path : str
            Path from which file to upload
        

        Returns
        -------
        string

    
    '''
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


def tanslator(key,endpoint,location,path,text_content):
    '''
       About:
       ---------
       Translates a text with the help of Azure Translator.

        Parameter
        ---------
        key : str
            key to Azure Translator.HIGHLY Restricted
        endpoint : str
            Endpoint of  Azure Translator. 
        location : str
            Location of Translator.
        path : str
            Path to define what is needed to be done.like translate and all etc.
        text_content : str
            Text to be converted from Azure Translator

        Returns
        -------
        string
    
    '''
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'hi',
        'to': ['fr', 'en']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text_content
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    # Extract the translated text from the response
    return response[0]['translations'][1]['text']

def speech_to_text(path,speech_subscription,speech_region):
    '''
       About:
       ---------
       Translates a text with the help of Azure Translator.

        Parameter
        ---------
        speech_subscription : str
            key to Azure Speech.HIGHLY Restricted
        speech_region : str
            Location of Translator.
        path : str
            Path to define what is needed to be done.like translate and all etc.

        Returns
        -------
        string
    
    '''
    # This example requires environment variables named "SPEECH_KEY" and "SPEECH_REGION"
    speech_config = speechsdk.SpeechConfig(subscription=speech_subscription, region=speech_region)
    speech_config.speech_recognition_language="en-US"

    #audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    audio_config = speechsdk.audio.AudioConfig(filename=path)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("Converting the Speech.")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return "{}".format(speech_recognition_result.text)
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        return "No speech could be recognized: {}".format(speech_recognition_result.no_match_details)
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Did you set the speech resource key and region values?")
            return("Error details: {}".format(cancellation_details.error_details))


