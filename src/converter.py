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
import logging

logging.basicConfig(filename='converter.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class AudioConverter:
    def __init__(self, translations):
        self.tr = translations
        self._cancel_flag = False
        self._startupinfo = None
        if sys.platform == 'win32':
            self._startupinfo = subprocess.STARTUPINFO()
            self._startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self._startupinfo.wShowWindow = subprocess.SW_HIDE
        self.configure_ffmpeg()

    def configure_ffmpeg(self):
        """Configure FFmpeg path for pydub to prevent console windows"""
        if getattr(sys, 'frozen', False):
            ffmpeg_path = os.path.join(sys._MEIPASS, 'ffmpeg.exe')
        else:
            ffmpeg_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ffmpeg.exe')

        AudioSegment.converter = ffmpeg_path
        # Update converter kwargs to include startupinfo
        AudioSegment.converter_kwargs = {
            'hide_banner': None,
            'loglevel': 'panic'
        }
        # Override pydub's _subprocess_call
        original_subprocess_call = subprocess.call
        def _subprocess_call_override(*args, **kwargs):
            if sys.platform == 'win32':
                kwargs['startupinfo'] = self._startupinfo
                kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
            return original_subprocess_call(*args, **kwargs)
        subprocess.call = _subprocess_call_override

    def cancel_conversion(self):
        """Signal to stop the conversion process"""
        self._cancel_flag = True

    def check_ffmpeg(self):
        """Check if FFmpeg is installed and available."""
        try:
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))

            ffmpeg_path = os.path.join(application_path, 'ffmpeg.exe')

            if os.path.exists(ffmpeg_path):
                subprocess.run(
                    [ffmpeg_path, '-version'],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    startupinfo=self._startupinfo,
                    creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
                )
                os.environ["FFMPEG_BINARY"] = ffmpeg_path
                return True

            # Fallback to system PATH
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
            if self._cancel_flag:
                logging.info(f"Conversion cancelled before starting for {m4a_file}")
                return False

            output_filename = os.path.splitext(os.path.basename(m4a_file))[0] + '.mp3'
            output_path = os.path.join(output_folder, output_filename)

            def convert():
                try:
                    if not self._cancel_flag:
                        logging.debug(f"Starting conversion for {m4a_file}")

                        # Use class-level startupinfo configuration
                        audio = AudioSegment.from_file(m4a_file, format="m4a")
                        audio.export(
                            output_path,
                            format="mp3",
                            bitrate="320k",
                            parameters=["-hide_banner", "-loglevel", "panic"]
                        )
                        logging.info(f"Successfully converted {m4a_file} to {output_path}")
                except Exception as e:
                    logging.error(f"Error during conversion of {m4a_file}: {e}")
                    raise

            await asyncio.get_event_loop().run_in_executor(executor, convert)
            return not self._cancel_flag

        except Exception as e:
            logging.exception(f"Unexpected error during conversion of {m4a_file}: {e}")
            if not self._cancel_flag:
                messagebox.showerror(
                    self.tr.get("error"),
                    self.tr.get("conversion_error").format(str(e))
                )
            return False

    async def convert_files(self, files_to_convert, output_folder, max_concurrent=3,
                            progress_callback=None, status_callback=None):
        """Convert multiple files concurrently."""
        logging.info(f"Starting batch conversion of {len(files_to_convert)} files.")

        self._cancel_flag = False  # Reset cancel flag
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
                if self._cancel_flag:
                    logging.info("Conversion cancelled.")
                    return False
                async with semaphore:
                    if self._cancel_flag:
                        return False
                    try:
                        result = await task
                        logging.info(f"Task completed with result: {result}")
                        return result
                    except Exception as e:
                        logging.error(f"Error in bounded_convert: {e}")
                        return False

            try:
                for task in asyncio.as_completed([bounded_convert(task) for task in tasks]):
                    if self._cancel_flag:
                        if status_callback:
                            status_callback(self.tr.get("conversion_cancelled"))
                        logging.info("Conversion cancelled during processing.")
                        return False

                    if await task:
                        completed += 1
                        if progress_callback:
                            progress_callback((completed / total_files) * 100)
                        if status_callback:
                            status_callback(self.tr.get("converting").format(completed, total_files))
                        logging.info(f"Completed {completed}/{total_files} files.")

            except asyncio.CancelledError:
                self._cancel_flag = True
                if status_callback:
                    status_callback(self.tr.get("conversion_cancelled"))
                logging.warning("Conversion cancelled by user.")
                return False

        logging.info(f"Batch conversion completed: {completed}/{total_files} files.")
        return completed == total_files
