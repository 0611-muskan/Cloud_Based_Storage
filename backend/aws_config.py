import os
from dotenv import load_dotenv
import boto3

load_dotenv()

print("REGION:", os.getenv("AWS_REGION"))
print("BUCKET:", os.getenv("AWS_BUCKET_NAME"))

# Configure AWS credentials
s3_client = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("AWS_SECRET_KEY")
)

export = s3_client
