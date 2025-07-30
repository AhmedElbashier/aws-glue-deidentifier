# test_presigned_url.py
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name="eu-north-1"
)

s3 = session.client("s3")
s3.head_object(Bucket='ahmed-healthcare-deidentified-data', Key="fdb2ea47-8155-4c53-9462-d3eaa6f3fc81.csv")

file_id = "fdb2ea47-8155-4c53-9462-d3eaa6f3fc81.csv"

url = s3.generate_presigned_url(
    ClientMethod='get_object',
    Params={
        'Bucket': 'ahmed-healthcare-deidentified-data',
        'Key': file_id
    },
    ExpiresIn=600
)

print("Presigned URL:")
print(url)
