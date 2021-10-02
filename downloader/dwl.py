import logging
import os
from typing import Any, Dict, List, Optional, Set

from youtube_dl import YoutubeDL
from youtube_dl.utils import DownloadError, ExtractorError


class YdlDownloadError(Exception):
    pass


class Ydl:
    def __init__(
            self, download_dir: str = '/tmp/downloader487',
            params: Optional[Dict] = None, playlist: bool = False,
            cleanup: bool = True,
    ):
        self._download_dir = download_dir
        self._cleanup = cleanup
        if params is None:
            params = {}

        os.makedirs(download_dir, exist_ok=True)

        params.setdefault('format', 'bestvideo[ext=mp4]/bestvideo/bestaudio')
        params.setdefault('noplaylist', not playlist)
        params.update(
            progress_hooks=[
                self.on_progress],
            outtmpl=f'{self._download_dir}/%(extractor)s-%(playlist)s-%(playlist_index)s-%(title)s-%(id)s.%(ext)s',
            restrictfilenames=True,
            logtostderr=True,
        )

        self._ydl = YoutubeDL(params=params, auto_init=True)
        self._current_files: Set[str] = set()
        self._all_files: Set[str] = set()

    def __enter__(self) -> 'Ydl':
        return self

    def __exit__(self, *_exc_info: List[Any]) -> None:
        if self._cleanup:
            for file_path in self._all_files:
                os.unlink(file_path)

    def download(self, urls: List[str]) -> List[str]:
        errors = []
        for url in urls:
            try:
                res_code = self._ydl.download([url])
            except (DownloadError, ExtractorError) as e:
                errors.append(e)
                res_code = 1

            if res_code != 0:
                logging.error(f'Download error for {url}')

        result = list(self._current_files)
        self._current_files = set()

        if not result:
            raise YdlDownloadError(f'Download result error: {errors}')

        self._all_files.update(self._current_files)
        return result

    def on_progress(self, data: Dict) -> None:
        self._current_files.add(data['filename'])
