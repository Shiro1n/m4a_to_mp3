"""
M4A to MP3 Converter application.
"""

from src.gui import ConverterGUI
from src.converter import AudioConverter
from src.translations import Translations

__version__ = '1.0.0'
__all__ = ['ConverterGUI', 'AudioConverter', 'Translations']