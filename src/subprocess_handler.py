import subprocess
import sys

_original_popen = subprocess.Popen


def _get_startupinfo():
    if sys.platform == 'win32':
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        return startupinfo
    return None


class SuppressedPopen:
    def __init__(self, *args, **kwargs):
        if sys.platform == 'win32':
            kwargs['startupinfo'] = _get_startupinfo()
            kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
            kwargs['shell'] = False
            kwargs.setdefault('stdin', subprocess.PIPE)
            kwargs.setdefault('stdout', subprocess.PIPE)
            kwargs.setdefault('stderr', subprocess.PIPE)
        self.process = _original_popen(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.process, name)


def _suppressed_call(*args, **kwargs):
    if sys.platform == 'win32':
        kwargs['startupinfo'] = _get_startupinfo()
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
        kwargs['shell'] = False
    return subprocess.call(*args, **kwargs)


def _suppressed_run(*args, **kwargs):
    if sys.platform == 'win32':
        kwargs['startupinfo'] = _get_startupinfo()
        kwargs['creationflags'] = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
        kwargs['shell'] = False
    return subprocess.run(*args, **kwargs)


# Replace subprocess methods
subprocess.Popen = SuppressedPopen
subprocess.call = _suppressed_call
subprocess.run = _suppressed_run
