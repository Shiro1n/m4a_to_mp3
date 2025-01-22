from PyInstaller.utils.hooks import collect_data_files

datas = collect_data_files('pydub')

def pre_safe_import_module(api):
    api.add_runtime_package('subprocess')