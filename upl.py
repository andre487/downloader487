import boto3
import os


class Uploader:
    def __init__(
        self, s3_endpoint: str, s3_region: str, s3_bucket: str,
        s3_access: str, s3_secret: str,
    ) -> None:
        self._s3_bucket = s3_bucket

        self._client = boto3.client(
            service_name='s3',
            endpoint_url=s3_endpoint,
            region_name=s3_region,
            aws_access_key_id=s3_access,
            aws_secret_access_key=s3_secret,
        )

    def upload(self, file_path: str) -> None:
        s3_key = os.path.basename(file_path)
        self._client.upload_file(file_path, self._s3_bucket, s3_key)
