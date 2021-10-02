import click
from typing import List
from dwl import Ydl


@click.command()
@click.option('-u', '--url', required=True, multiple=True)
@click.option('-d', '--download-dir', default='/tmp/downloader487', show_default=True)
@click.option('-p', '--playlist', is_flag=True)
@click.option('-n', '--no-cleanup', is_flag=True)
def main(url: List[str], download_dir: str, playlist: bool, no_cleanup: bool):
    with Ydl(download_dir=download_dir, playlist=playlist, cleanup=not no_cleanup) as ydl:
        results = ydl.download(url)
        print(results)


if __name__ == '__main__':
    main()
