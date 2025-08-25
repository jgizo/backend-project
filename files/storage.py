import boto3
from django.conf import settings

s3_client = boto3.client(
    's3',
    endpoint_url=settings.MINIO_ENDPOINT,
    aws_access_key_id=settings.MINIO_ACCESS_KEY,
    aws_secret_access_key=settings.MINIO_SECRET_KEY
)

def upload_file_to_minio(file_obj, file_path, bucket_name=settings.MINIO_BUCKET):
    s3_client.upload_fileobj(file_obj, bucket_name, file_path)
