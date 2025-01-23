import subprocess
import sys

_original_popen = subprocess.Popen


def custom_popen(*args, **kwargs):
    if sys.platform == "win32":
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        kwargs['startupinfo'] = startupinfo
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW
    return _original_popen(*args, **kwargs)


subprocess.Popen = custom_popen
