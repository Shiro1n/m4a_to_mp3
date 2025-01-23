import sys
import logging
from pathlib import Path


class Config:
    def __init__(self):
        self.FFMPEG_URL = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
        self.MAX_CONCURRENT_CONVERSIONS = 3
        self.MP3_BITRATE = "320k"
        self.FFMPEG_PARAMS = ["-hide_banner", "-loglevel", "panic"]

        # Setup logging
        logging.basicConfig(
            filename='converter.log',
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    @property
    def ffmpeg_path(self):
        # Always point to the 'src' folder for ffmpeg.exe
        if getattr(sys, 'frozen', False):
            return Path(sys._MEIPASS) / 'src' / 'ffmpeg.exe'
        return Path(__file__).parent / 'src' / 'ffmpeg.exe'