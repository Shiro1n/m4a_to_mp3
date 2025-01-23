import logging
import os
import subprocess
import sys
import urllib.request
import zipfile
import shutil
from pathlib import Path


class FFmpegHandler:
    def __init__(self, config, translations):
        self.config = config
        self.tr = translations
        self._setup_subprocess_info()

    def _setup_subprocess_info(self):
        self._startupinfo = None
        if sys.platform == 'win32':
            self._startupinfo = subprocess.STARTUPINFO()
            self._startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._startupinfo.wShowWindow = subprocess.SW_HIDE

    def check_installation(self):
        """Check if FFmpeg is installed and available."""
        try:
            ffmpeg_path = self.config.ffmpeg_path
            if ffmpeg_path.exists():
                self._run_ffmpeg_check(ffmpeg_path)
                os.environ["FFMPEG_BINARY"] = str(ffmpeg_path)
                return True
            return self._check_system_ffmpeg()
        except Exception as e:
            logging.error(f"FFmpeg check failed: {e}")
            return False

    def _run_ffmpeg_check(self, ffmpeg_path):
        logging.debug(f"Using FFmpeg at: {ffmpeg_path}")
        subprocess.run(
            [str(ffmpeg_path), '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            startupinfo=self._startupinfo,
            creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
        )

    def _check_system_ffmpeg(self):
        try:
            subprocess.run(
                ['ffmpeg', '-version'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=self._startupinfo,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return True
        except FileNotFoundError:
            return False

    async def install(self, status_callback=None):
        """Download and install FFmpeg asynchronously."""
        try:
            if status_callback:
                status_callback(self.tr.get("downloading_ffmpeg"))

            await self._download_ffmpeg()
            await self._extract_and_setup_ffmpeg(status_callback)

            if status_callback:
                status_callback(self.tr.get("ffmpeg_success"))
            return True

        except Exception as e:
            logging.error(f"FFmpeg installation failed: {e}")
            if status_callback:
                status_callback(self.tr.get("ffmpeg_failed").format(str(e)))
            return False

    async def _download_ffmpeg(self):
        download_path = Path.cwd() / "ffmpeg.zip"
        urllib.request.urlretrieve(self.config.FFMPEG_URL, download_path)
        return download_path

    async def _extract_and_setup_ffmpeg(self, status_callback):
        if status_callback:
            status_callback(self.tr.get("installing_ffmpeg"))

        download_path = Path.cwd() / "ffmpeg.zip"
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(Path.cwd())

        ffmpeg_dir = next(Path.cwd().rglob("ffmpeg.exe")).parent
        for file in ffmpeg_dir.glob("*.exe"):
            shutil.copy(file, Path.cwd())

        # Cleanup
        download_path.unlink()
        shutil.rmtree(next(Path.cwd().glob("ffmpeg-*")))