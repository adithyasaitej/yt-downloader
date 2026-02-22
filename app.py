import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

from yt_dlp import YoutubeDL


class DownloaderApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.geometry("640x300")
        self.root.resizable(False, False)

        self.url_var = tk.StringVar()
        self.output_var = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.filename_var = tk.StringVar(value="%(title)s.%(ext)s")
        self.status_var = tk.StringVar(value="Ready")
        self.progress_var = tk.DoubleVar(value=0)

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self.root, padding=14)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="YouTube URL").grid(row=0, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.url_var, width=72).grid(row=1, column=0, columnspan=3, sticky="ew", pady=(2, 12))

        ttk.Label(frame, text="Output folder").grid(row=2, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.output_var, width=54).grid(row=3, column=0, columnspan=2, sticky="ew", pady=(2, 8))
        ttk.Button(frame, text="Browse", command=self._choose_output_dir).grid(row=3, column=2, padx=(8, 0), sticky="ew")

        ttk.Label(frame, text="Filename template (optional)").grid(row=4, column=0, sticky="w")
        ttk.Entry(frame, textvariable=self.filename_var, width=72).grid(row=5, column=0, columnspan=3, sticky="ew", pady=(2, 12))

        self.progress = ttk.Progressbar(frame, maximum=100, variable=self.progress_var)
        self.progress.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(0, 8))

        ttk.Label(frame, textvariable=self.status_var).grid(row=7, column=0, columnspan=3, sticky="w")

        self.download_btn = ttk.Button(frame, text="Download", command=self._start_download)
        self.download_btn.grid(row=8, column=0, columnspan=3, pady=(16, 0), sticky="ew")

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=0)

    def _choose_output_dir(self) -> None:
        selected = filedialog.askdirectory(initialdir=self.output_var.get())
        if selected:
            self.output_var.set(selected)

    def _set_status(self, text: str) -> None:
        self.root.after(0, lambda: self.status_var.set(text))

    def _set_progress(self, value: float) -> None:
        self.root.after(0, lambda: self.progress_var.set(value))

    def _toggle_button(self, enabled: bool) -> None:
        state = "normal" if enabled else "disabled"
        self.root.after(0, lambda: self.download_btn.config(state=state))

    def _download_hook(self, d: dict) -> None:
        status = d.get("status")
        if status == "downloading":
            total = d.get("total_bytes") or d.get("total_bytes_estimate")
            downloaded = d.get("downloaded_bytes", 0)
            if total:
                self._set_progress((downloaded / total) * 100)
            speed = d.get("speed")
            if speed:
                mbps = speed / 1024 / 1024
                self._set_status(f"Downloading... {mbps:.2f} MB/s")
            else:
                self._set_status("Downloading...")
        elif status == "finished":
            self._set_progress(100)
            self._set_status("Download complete. Finalizing file...")

    def _start_download(self) -> None:
        url = self.url_var.get().strip()
        output_dir = self.output_var.get().strip()
        filename_template = self.filename_var.get().strip() or "%(title)s.%(ext)s"

        if not url:
            messagebox.showerror("Missing URL", "Please enter a YouTube URL.")
            return

        if not os.path.isdir(output_dir):
            messagebox.showerror("Invalid folder", "Please choose a valid output folder.")
            return

        self._set_progress(0)
        self._set_status("Starting download...")
        self._toggle_button(False)

        threading.Thread(
            target=self._download_worker,
            args=(url, output_dir, filename_template),
            daemon=True,
        ).start()

    def _download_worker(self, url: str, output_dir: str, filename_template: str) -> None:
        options = {
            "format": "best[ext=mp4]/best",
            "outtmpl": os.path.join(output_dir, filename_template),
            "noplaylist": True,
            "quiet": True,
            "no_warnings": True,
            "progress_hooks": [self._download_hook],
        }

        try:
            with YoutubeDL(options) as ydl:
                ydl.download([url])
            self._set_status("Done! File saved successfully.")
            self.root.after(0, lambda: messagebox.showinfo("Success", "Download completed successfully."))
        except Exception as exc:  # noqa: BLE001
            self._set_status("Download failed.")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Download failed:\n{exc}"))
        finally:
            self._toggle_button(True)


def main() -> None:
    root = tk.Tk()
    app = DownloaderApp(root)
    _ = app
    root.mainloop()


if __name__ == "__main__":
    main()
