from setuptools import setup, find_packages

setup(
    name="voice_converter",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pydub>=0.25.1",
        "tkinterdnd2>=0.3.0",
    ],
)