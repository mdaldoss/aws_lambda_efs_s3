# Routines to upload/download file to aws bucket

import os
import boto3

# from dotenv import load_dotenv
# load_dotenv(verbose=True)

## Keys Definition
S3_AWS_ACCESS_KEY_ID = "YOUR_KEY"
S3_AWS_ACCESS_KEY_SECRET = "YOUR_SUPER_SUPER_SECRET_KEY"


def aws_session(region_name='eu-central-1'):
    return boto3.session.Session(aws_access_key_id=os.getenv('S3_AWS_ACCESS_KEY_ID', S3_AWS_ACCESS_KEY_ID),
                                aws_secret_access_key=os.getenv('S3_AWS_ACCESS_KEY_SECRET', S3_AWS_ACCESS_KEY_SECRET),
                                region_name=region_name)

# Uploading
def upload_file_to_bucket(bucket_name, file_path, file_name_on_s3=None):
    """ 
       Usage:
       s3_url = upload_file_to_bucket('tci-s3-demo', 'children.csv')
       print(s3_url)
    """
    session = aws_session()
    s3_resource = session.resource('s3')
    if file_name_on_s3 == None:
        file_dir, file_name_on_s3 = os.path.split(file_path)
    bucket = s3_resource.Bucket(bucket_name)
    bucket.upload_file(
      Filename=file_path,
      Key=file_name_on_s3,
      ExtraArgs={'ACL': 'public-read'}
    )
    s3_url = f"https://{bucket_name}.s3.amazonaws.com/{file_name_on_s3}"
    return s3_url

def put_object_bucket(bucket_name, file_name_on_s3, data):
    session = aws_session()
    s3_resource = session.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    bucket.put_object(
        Body=data,
        Key=file_name_on_s3,
        Bucket=bucket_name
    )
    
# Creating a bucket
def make_bucket(name, acl):
  """
  Usage:
  s3_bucket = make_bucket('tci-s3-demo', 'public-read')
  """
  session = aws_session()
  s3_resource = session.resource('s3')
  return s3_resource.create_bucket(Bucket=name, ACL=acl)

# Downloading a bucket
def download_file_from_bucket(bucket_name, s3_key, dst_path):
  """
  Usage:
  download_file_from_bucket('tci-s3-demo', 'children.csv', 'children_download.csv')
  with open('children_download.csv') as fo:
  print(fo.read())
  """
  session = aws_session()
  s3_resource = session.resource('s3')
  bucket = s3_resource.Bucket(bucket_name)
  bucket.download_file(Key=s3_key, Filename=dst_path)


  
