class Translations:
    def __init__(self):
        self.tr = {
            "tr": {
                "title": "M4A'dan MP3'e Dönüştürücü",
                "input_folder": "Giriş Klasörü:",
                "output_folder": "Çıkış Klasörü:",
                "browse": "Gözat",
                "concurrent": "Eşzamanlı Dönüşüm:",
                "convert": "Dönüştür",
                "ready": "Hazır",
                "converting": "Dönüştürülüyor: {}/{} dosya tamamlandı",
                "completed": "Dönüşüm tamamlandı!",
                "files_to_convert": "Dönüştürülecek Dosyalar:",
                "no_files": "Giriş klasöründe M4A dosyası bulunamadı",
                "select_folders": "Lütfen giriş ve çıkış klasörlerini seçin",
                "ffmpeg_required": "FFmpeg gerekli fakat bulunamadı. İndirip kurmak ister misiniz?",
                "downloading_ffmpeg": "FFmpeg indiriliyor...",
                "installing_ffmpeg": "FFmpeg kuruluyor...",
                "ffmpeg_success": "FFmpeg başarıyla kuruldu!",
                "ffmpeg_failed": "FFmpeg kurulumu başarısız oldu: {}",
                "success": "Başarılı",
                "error": "Hata",
                "drag_drop": "M4A dosyalarını buraya sürükleyin",
                "language": "Dil:",
                "all_completed": "Tüm dönüşümler tamamlandı!",
                "conversion_error": "Dönüşüm hatası: {}",
                "clear_all": "Tümünü Temizle",
                "select_all": "Tümünü Seç",
                "remove_selected": "Seçilenleri Kaldır",
                "stop": "Durdur",
                "conversion_cancelled": "Dönüştürme iptal edildi"
            },
            "en": {
                "title": "M4A to MP3 Converter",
                "input_folder": "Input Folder:",
                "output_folder": "Output Folder:",
                "browse": "Browse",
                "concurrent": "Concurrent Conversions:",
                "convert": "Convert",
                "ready": "Ready",
                "converting": "Converting: {}/{} files completed",
                "completed": "Conversion completed!",
                "files_to_convert": "Files to Convert:",
                "no_files": "No M4A files found in the input folder",
                "select_folders": "Please select input and output folders",
                "ffmpeg_required": "FFmpeg is required but not found. Would you like to download and install it?",
                "downloading_ffmpeg": "Downloading FFmpeg...",
                "installing_ffmpeg": "Installing FFmpeg...",
                "ffmpeg_success": "FFmpeg has been installed successfully!",
                "ffmpeg_failed": "Failed to install FFmpeg: {}",
                "success": "Success",
                "error": "Error",
                "drag_drop": "Drag and drop M4A files here",
                "language": "Language:",
                "all_completed": "All conversions completed!",
                "conversion_error": "Conversion error: {}",
                "clear_all": "Clear All",
                "select_all": "Select All",
                "remove_selected": "Remove Selected",
                "stop": "Stop",
                "conversion_cancelled": "Conversion cancelled"

            }
        }
        self.current_lang = "tr"

    def get(self, key, *args):
        text = self.tr[self.current_lang].get(key, key)
        return text.format(*args) if args else text