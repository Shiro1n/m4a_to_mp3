import os
import asyncio
import sys
from pathlib import Path
import urllib.request
import zipfile
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
from tkinter import messagebox


class AudioConverter:
    def __init__(self, translations):
        self.tr = translations

    def check_ffmpeg(self):
        """Check if FFmpeg is installed and available."""
        try:
            # Get the application directory
            if getattr(sys, 'frozen', False):
                # If we're running as a PyInstaller bundle
                application_path = sys._MEIPASS
            else:
                # If we're running in a normal Python environment
                application_path = os.path.dirname(os.path.abspath(__file__))

            # Check for ffmpeg in the application directory
            ffmpeg_path = os.path.join(application_path, 'ffmpeg.exe')
            if os.path.exists(ffmpeg_path):
                subprocess.run([ffmpeg_path, '-version'], capture_output=True)
                os.environ["FFMPEG_BINARY"] = ffmpeg_path  # Set for pydub
                return True

            # As a fallback, try system PATH
            subprocess.run(['ffmpeg', '-version'], capture_output=True)
            return True

        except FileNotFoundError:
            return False

    def install_ffmpeg(self, status_callback=None):
        """Download and install FFmpeg."""
        try:
            if status_callback:
                status_callback(self.tr.get("downloading_ffmpeg"))

            # Download FFmpeg
            ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
            download_path = os.path.join(os.getcwd(), "ffmpeg.zip")

            urllib.request.urlretrieve(ffmpeg_url, download_path)

            if status_callback:
                status_callback(self.tr.get("installing_ffmpeg"))

            # Extract FFmpeg
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())

            # Move ffmpeg.exe to current directory
            ffmpeg_dir = next(Path(os.getcwd()).rglob("ffmpeg.exe")).parent
            for file in ffmpeg_dir.glob("*.exe"):
                shutil.copy(file, os.getcwd())

            # Clean up
            os.remove(download_path)
            shutil.rmtree(next(Path(os.getcwd()).glob("ffmpeg-*")))

            if status_callback:
                status_callback(self.tr.get("ffmpeg_success"))
            return True

        except Exception as e:
            if status_callback:
                status_callback(self.tr.get("ffmpeg_failed").format(str(e)))
            return False

    async def convert_single_file(self, m4a_file, output_folder, executor):
        """Convert a single M4A file to MP3 format asynchronously."""
        try:
            output_filename = os.path.splitext(os.path.basename(m4a_file))[0] + '.mp3'
            output_path = os.path.join(output_folder, output_filename)

            def convert():
                audio = AudioSegment.from_file(m4a_file, format="m4a")
                audio.export(output_path, format="mp3", bitrate="320k")

            await asyncio.get_event_loop().run_in_executor(executor, convert)
            return True

        except Exception as e:
            messagebox.showerror(
                self.tr.get("error"),
                self.tr.get("conversion_error").format(str(e))
            )
            return False

    async def convert_files(self, files_to_convert, output_folder, max_concurrent=3,
                            progress_callback=None, status_callback=None):
        """Convert multiple files concurrently."""
        Path(output_folder).mkdir(parents=True, exist_ok=True)

        total_files = len(files_to_convert)
        completed = 0

        with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
            tasks = [
                self.convert_single_file(file, output_folder, executor)
                for file in files_to_convert
            ]

            semaphore = asyncio.Semaphore(max_concurrent)

            async def bounded_convert(task):
                async with semaphore:
                    return await task

            for task in asyncio.as_completed([bounded_convert(task) for task in tasks]):
                if await task:
                    completed += 1
                    if progress_callback:
                        progress_callback((completed / total_files) * 100)
                    if status_callback:
                        status_callback(self.tr.get("converting").format(completed, total_files))

        return completed == total_files