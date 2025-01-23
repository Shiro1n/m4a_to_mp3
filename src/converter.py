# converter.py
import asyncio
import logging
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from tkinter import messagebox
from pathlib import Path


class AudioConverter:
    def __init__(self, config, ffmpeg_handler, translations):
        self.config = config
        self.ffmpeg_handler = ffmpeg_handler
        self.tr = translations
        self._cancel_flag = False
        self._configure_pydub()

    def _configure_pydub(self):
        """Configure pydub settings for optimal performance"""
        AudioSegment.converter = str(self.config.ffmpeg_path)
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE

        AudioSegment.converter = str(self.config.ffmpeg_path)
        AudioSegment.converter_kwargs = {
            'hide_banner': None,
            'loglevel': 'panic',
            'startupinfo': startupinfo,
            'shell': False,
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
        }

    def cancel_conversion(self):
        """Signal to stop the conversion process"""
        self._cancel_flag = True
        logging.info("Conversion cancellation requested")

    async def convert_single_file(self, m4a_file: Path, output_folder: Path) -> bool:
        """Convert a single M4A file to MP3 format"""
        if self._cancel_flag:
            return False

        try:
            output_path = output_folder / f"{m4a_file.stem}.mp3"

            def convert():
                if self._cancel_flag:
                    return False

                audio = AudioSegment.from_file(str(m4a_file), format="m4a")
                audio.export(
                    str(output_path),
                    format="mp3",
                    bitrate=self.config.MP3_BITRATE,
                    parameters=self.config.FFMPEG_PARAMS
                )
                return True

            return await asyncio.get_event_loop().run_in_executor(None, convert)

        except Exception as e:
            logging.error(f"Conversion failed for {m4a_file}: {e}")
            if not self._cancel_flag:
                messagebox.showerror(
                    self.tr.get("error"),
                    self.tr.get("conversion_error").format(str(e))
                )
            return False

    async def convert_files(self, files_to_convert, output_folder,
                            progress_callback=None, status_callback=None):
        """Convert multiple files with efficient resource management"""
        logging.info(f"Starting batch conversion of {len(files_to_convert)} files")

        self._cancel_flag = False
        output_folder = Path(output_folder)
        output_folder.mkdir(parents=True, exist_ok=True)

        total_files = len(files_to_convert)
        completed = 0
        tasks = []

        # Create semaphore for limiting concurrent conversions
        sem = asyncio.Semaphore(self.config.MAX_CONCURRENT_CONVERSIONS)

        async def bounded_convert(file):
            async with sem:
                if self._cancel_flag:
                    return False
                return await self.convert_single_file(Path(file), output_folder)

        # Create tasks for all files
        for file in files_to_convert:
            tasks.append(bounded_convert(file))

        try:
            # Process files with controlled concurrency
            for task in asyncio.as_completed(tasks):
                if self._cancel_flag:
                    if status_callback:
                        status_callback(self.tr.get("conversion_cancelled"))
                    return False

                if await task:
                    completed += 1
                    if progress_callback:
                        progress_callback((completed / total_files) * 100)
                    if status_callback:
                        status_callback(self.tr.get("converting").format(completed, total_files))

        except asyncio.CancelledError:
            self._cancel_flag = True
            if status_callback:
                status_callback(self.tr.get("conversion_cancelled"))
            return False

        logging.info(f"Batch conversion completed: {completed}/{total_files} files")
        return completed == total_files
