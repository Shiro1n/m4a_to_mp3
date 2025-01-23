# M4A to MP3 Converter

This project is a GUI-based M4A to MP3 audio converter built with Python. It supports drag-and-drop functionality and batch conversion of audio files using the `pydub` library and `FFmpeg`. The app is packaged as a standalone executable using `PyInstaller`.

---

## Features

- **Batch Conversion**: Convert multiple M4A files to MP3 format effortlessly.
- **Drag-and-Drop**: Simplified file selection using drag-and-drop functionality.
- **Custom MP3 Bitrate**: Choose the desired MP3 bitrate for output files.
- **Hidden Console**: Prevents console windows from appearing during conversions for a seamless experience.
- **FFmpeg Installation**: Automatically downloads and installs FFmpeg if not found, ensuring smooth operation.

---

## Prerequisites

- Python 3.9+
- FFmpeg binary (`ffmpeg.exe` in the `src` folder)

---

## Installation

1. Clone this repository:
    ```bash
    git clone <repository-url>
    cd <repository-folder>
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `ffmpeg.exe` is in the `src` folder. If missing, the app will attempt to download it automatically.

---

## Usage

### Running the Application

1. Start the app:
    ```bash
    python main.py
    ```

2. Drag and drop M4A files into the app window or use the file browser to select files.
3. Set the output folder and bitrate (optional).
4. Click **Convert** to start the batch conversion process.

### Building the Executable

1. Clean up previous build artifacts:
    ```bash
    python build.py
    ```

2. Run the build script:
    ```bash
    python build.py
    ```

3. The executable will be located in the `dist` folder as `m4a_to_mp3.exe`.

---

## File Structure

```
project-folder/
├── src/
│   ├── components/
│   │   ├── __init__.py
│   │   ├── controls.py
│   │   ├── file_list.py
│   │   ├── language_selector.py
│   ├── config.py
│   ├── converter.py
│   ├── ffmpeg.exe         # FFmpeg binary
│   ├── ffmpeg_handler.py
│   ├── gui.py
│   ├── pydub_override.py
│   ├── subprocess_handler.py
│   └── translations.py
├── main.py                # Entry point of the application
├── build.py               # PyInstaller build script
├── requirements.txt       # Required Python libraries
└── README.md              # Project documentation
```

---

## Troubleshooting

### FFmpeg Not Found
- Ensure `ffmpeg.exe` is located in the `src` folder.
- The app will download FFmpeg automatically if missing, but this requires an active internet connection.

### Drag-and-Drop Not Working
- Ensure `tkinterdnd2` is installed.
- Check the logs for any initialization errors.

### Recursion Errors
- Ensure no conflicting `subprocess.Popen` overrides are present.
- Use the provided `subprocess_handler.py` implementation to avoid issues.

---

## Dependencies

- Python 3.9+
- `pydub`
- `tkinterdnd2`
- `PyInstaller`

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Credits

- **FFmpeg**: [FFmpeg Official Website](https://ffmpeg.org/)
- **Pydub**: [Pydub GitHub Repository](https://github.com/jiaaro/pydub)

