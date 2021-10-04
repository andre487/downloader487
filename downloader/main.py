import logging
import os
from typing import List

import click

from dwl import Ydl
from upl import Uploader
from util import get_secret_value


@click.command()
@click.option('-u', '--url', required=True, multiple=True)
@click.option('-d', '--download-dir',
              default='/tmp/downloader487', show_default=True)
@click.option('-p', '--playlist', is_flag=True)
@click.option('--s3-endpoint', default='https://storage.yandexcloud.net')
@click.option('--s3-region', default='ru-central1')
@click.option('--s3-bucket', default='downloader487-files')
@click.option('--s3-access-file',
              default=os.path.expanduser('~/.tokens/s3-access'))
@click.option('--s3-secret-file',
              default=os.path.expanduser('~/.tokens/s3-secret'))
@click.option('--no-cleanup', is_flag=True)
@click.option('--no-s3', is_flag=True)
def main(
    url: List[str],
    download_dir: str,
    playlist: bool,
    no_cleanup: bool,
    s3_endpoint: str,
    s3_region: str,
    s3_bucket: str,
    s3_access_file: str,
    s3_secret_file: str,
    no_s3: bool,
) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s\t%(levelname)s\t%(message)s')

    s3_access = None
    s3_secret = None

    if not no_s3:
        s3_access = get_secret_value('S3_ACCESS_KEY', s3_access_file)
        s3_secret = get_secret_value('S3_SECRET_KEY', s3_secret_file)

    with Ydl(download_dir=download_dir, playlist=playlist, cleanup=not no_cleanup) as ydl:
        logging.info('Download files')

        results = ydl.download(url)
        if not no_s3:
            uploader = Uploader(
                s3_endpoint=s3_endpoint,
                s3_region=s3_region,
                s3_bucket=s3_bucket,
                s3_access=s3_access,
                s3_secret=s3_secret,
            )

            error_count = 0
            for file_path in results:
                logging.info(f'Upload {file_path}')
                res = uploader.upload(file_path)
                if not res:
                    error_count += 1

            if error_count == len(results):
                raise Exception('No files were uploaded')
            elif error_count:
                logging.error('There were upload errors')


if __name__ == '__main__':
    main()
