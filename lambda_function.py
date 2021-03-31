import json
import os
import boto3
import io
import zipfile
import sys
from s3_api import *

BUCKET_NAME = "my_s3_bucket_name"

def download_layer(bucket_name, filename, layer_name):
    """ 
        This method download files from S3 and save them to a lambda destination folder, 
        The destination folder can be an EFS (Elastic File System) directory, too.
        Please mind to configure it properly.
        Please note that lambda temporary directory ("/tmp") has a limit of 512 MB!
    """
    
    # Specify the EFS folder where to save the files once downloaded
    project_folder = '/mnt/efs1/{0!s}'.format(layer_name)

    if not os.path.isdir(project_folder):
        session = aws_session()
        s3_resource = session.resource('s3')
        print("start")
        s3_bucket = s3_resource.Bucket(bucket_name)
        print("s3bucket")

        folder_obj = s3_bucket.objects.filter(Prefix=filename).all()
        down_list = [el for el in folder_obj ] 
        obj = down_list[0]
        print("obj",obj)

        print(obj)
        key = obj.key # Get filename
        print(key) 
        zf = io.BytesIO(obj.get()['Body'].read())
        
        # Read the file as a zipfile and process the members
        with zipfile.ZipFile(zf, mode='r') as zipf:
            zipf.extractall(project_folder)

def lambda_handler(event, context):
    # Download layer packages
    download_layer(BUCKET_NAME, 'path-to-my-s3-files.zip', 'destination_folder')
    # List downloaded files
    print("ls: ",os.listdir("/mnt/efs1/"))    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Marco!')
    }
