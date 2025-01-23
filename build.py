# build.py
import PyInstaller.__main__
import os
import shutil

def cleanup():
    """Clean up build artifacts"""
    dirs_to_remove = ['build', 'dist']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    if os.path.exists('m4a_to_mp3.spec'):
        os.remove('m4a_to_mp3.spec')

def build():
    """Build the executable"""
    PyInstaller.__main__.run([
        'main.py',
        '--name=m4a_to_mp3',
        '--onefile',
        '--noconsole',
        '--icon=assets/app.ico',
        '--add-data=src;src',
        '--hidden-import=tkinter',
        '--hidden-import=tkinterdnd2',
        '--hidden-import=pydub',
        '--hidden-import=asyncio',
        '--collect-all=tkinterdnd2',
        '--add-binary=src/ffmpeg.exe;.',
        '--clean',
    ])

if __name__ == "__main__":
    cleanup()
    build()
    print("Build completed successfully!")