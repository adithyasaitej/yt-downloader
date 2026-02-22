# YouTube Downloader (Windows EXE)

A simple desktop YouTube downloader for Windows built with Python, `yt-dlp`, and Tkinter.

## What this project gives you

- A desktop app (`.exe`) for downloading videos from YouTube.
- A way to share the built app with others.
- No Python installation required for end users when you distribute the built folder.

## Features

- Download to MP4 when available.
- Choose output folder.
- Optional custom filename template.
- Download progress and status updates.

## Legal notice

Only download content when you have permission from the content owner and when it complies with YouTube's Terms of Service and local laws.

## 1) Development setup (on Windows)

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/).
2. Open PowerShell in this project folder.
3. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

4. Install dependencies:

```powershell
pip install -r requirements.txt
```

5. Run the app:

```powershell
python app.py
```

## 2) Build the EXE

Use the provided build script:

```powershell
build_windows.bat
```

After building, the distributable files will be in:

- `dist\YTDownloader\YTDownloader.exe`

## 3) Share with others

Zip the entire `dist\YTDownloader` folder and share it.

Example:

```powershell
Compress-Archive -Path .\dist\YTDownloader\* -DestinationPath .\YTDownloader-win64.zip
```

Your users can extract and run `YTDownloader.exe` directly.

## Optional: update downloader backend

`yt-dlp` updates frequently. Rebuild your app occasionally:

```powershell
pip install -U yt-dlp
build_windows.bat
```
