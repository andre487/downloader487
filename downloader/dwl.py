import logging
import os
from typing import Any, Dict, List, Optional, Set

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, ExtractorError


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

        logger = logging.getLogger('ydl')
        logger.setLevel(logging.DEBUG)

        params.setdefault('noplaylist', not playlist)
        params.setdefault('format', 'best[ext=mp4]/best')

        params.update(
            progress_hooks=[self.on_progress],
            outtmpl=f'{self._download_dir}/%(extractor)s-%(playlist)s-%(playlist_index)s-%(title)s-%(id)s.%(ext)s',
            restrictfilenames=True,
            logtostderr=True,
            usenetrc=True,
            quiet=False,
            verbose=True,
            ignoreerrors=True,
            cachedir=False,
            no_color=False,
            logger=logger,
        )

        self._ydl = YoutubeDL(params=params, auto_init=True)
        self._current_files: Set[str] = set()
        self._all_files: Set[str] = set()

    def __enter__(self) -> 'Ydl':
        return self

    def __exit__(self, *_exc_info: List[Any]) -> None:
        if self._cleanup:
            for file_path in self._all_files:
                try:
                    os.unlink(file_path)
                    logging.info(f'File removed: {file_path}')
                except OSError as e:
                    logging.warning(e)

    def download(self, urls: List[str]) -> List[str]:
        error = None
        try:
            self._ydl.download(urls)
        except (DownloadError, ExtractorError) as e:
            error = e

        result = list(self._current_files)
        self._all_files.update(self._current_files)
        self._current_files = set()

        if not result:
            raise YdlDownloadError(f'Download result error: {error}')

        return result

    def on_progress(self, data: Dict) -> None:
        self._current_files.add(data['filename'])
