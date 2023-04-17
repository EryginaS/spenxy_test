import logging

import boto3

from app import settings
from app.exceptions.upload_file import S3SendFileException


class S3Service:
    def __init__(self, bucket_name, aws_access_key_id, aws_secret_access_key):
        self._bucket_name = bucket_name
        self._aws_access_key_id = aws_access_key_id
        self._aws_secret_access_key = aws_secret_access_key

    def upload_file(self, content: bytes, file_name: str) -> None:

        try:
            s3 = boto3.client(
                's3', aws_access_key_id=self._aws_access_key_id, aws_secret_access_key=self._aws_secret_access_key
            )
            s3.upload_fileobj(content, self._bucket_name, file_name)
        except Exception as e:
            logging.error(f'Error send file to s3 {e}')
            raise S3SendFileException(e)


def get_s3_service() -> S3Service:
    return S3Service(
        bucket_name=settings.AWS_S3_BUCKET_NAME,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
