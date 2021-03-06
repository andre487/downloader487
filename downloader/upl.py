import logging
import os
from typing import Optional

import boto3


class Uploader:
    def __init__(
            self, s3_endpoint: str, s3_region: str, s3_bucket: str,
            s3_access: Optional[str], s3_secret: Optional[str],
    ) -> None:
        self._s3_bucket = s3_bucket

        self._client = boto3.client(
            service_name='s3',
            endpoint_url=s3_endpoint,
            region_name=s3_region,
            aws_access_key_id=s3_access,
            aws_secret_access_key=s3_secret,
        )

    def upload(self, file_path: str) -> bool:
        if not os.path.exists(file_path):
            logging.error(f'File not found: {file_path}')
            return False

        s3_key = os.path.basename(file_path)
        self._client.upload_file(file_path, self._s3_bucket, s3_key)
        return True
