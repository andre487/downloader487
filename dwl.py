from enum import auto
import dataclasses
import os
from typing import Dict, List, Optional
from youtube_dl import YoutubeDL


class DownloadError(Exception):
    pass


class Ydl:
    def __init__(self, download_dir: str = '/tmp/downloader487', params: Optional[Dict] = None, playlist: bool = False):
        self._download_dir = download_dir
        if params is None:
            params = {}

        os.makedirs(download_dir, exist_ok=True)

        params.setdefault('format', 'bestvideo[ext=mp4]/bestvideo/bestaudio')
        params.setdefault('noplaylist', not playlist)
        params.update(
            progress_hooks=[self.on_progress],
            outtmpl=f'{self._download_dir}/%(playlist)s-%(playlist_index)s-%(title)s-%(id)s.%(ext)s',
            restrictfilenames=True,
            logtostderr=True,
        )

        self._ydl = YoutubeDL(params=params, auto_init=True)
        self._current_files = set()
        self._all_files = set()

    def download(self, urls: List[str]) -> List[str]:
        res_code = self._ydl.download(urls)
        if res_code != 0:
            raise DownloadError(f'Download result code is {res_code}')

        result = list(self._current_files)

        self._all_files.update(self._current_files)
        self._current_files = set()

        return result

    def on_progress(self, data: Dict):
        self._current_files.add(data['filename'])
