import tkinter as tk
from tkinter import ttk, messagebox
import yt_dlp
import threading
import os
import re
import time
import random
import string

# ================== GLOBAL STATE ==================
video_progress_var = None
playlist_progress_var = None
status_label = None
overall_label = None
loading_text = None

total_playlist_bytes = 0
downloaded_playlist_bytes = 0
current_video_bytes = 0

loading_running = False

pause_event = threading.Event()
pause_event.set()
is_paused = False


# ================== HELPERS ==================
def safe_folder_name(name):
    return re.sub(r'[\\/:*?"<>|]', '', name)

def format_mb(b):
    return f"{b / (1024 * 1024):.2f} MB"


# ================== PAUSE / RESUME ==================
def toggle_pause():
    global is_paused

    if not is_paused:
        pause_event.clear()
        pause_btn.config(text="Resume ▶")
        status_label.config(text="⏸️ Download paused")
        is_paused = True
    else:
        pause_event.set()
        pause_btn.config(text="Pause ⏸️")
        status_label.config(text="▶ Download resumed")
        is_paused = False


# ================== MATRIX LOADING ==================
def matrix_loading():
    global loading_running

    chars = string.ascii_letters + string.digits + "@#$%&*"
    messages = [
        "Initializing yt-dlp engine",
        "Connecting to YouTube servers",
        "Fetching playlist metadata",
        "Code locked by Himanshu",
        "Calculating playlist size",
        "Preparing download pipeline"
    ]

    msg_index = 0

    while loading_running:
        random_line = ''.join(random.choice(chars) for _ in range(60))
        message = messages[msg_index % len(messages)]

        loading_text.insert(tk.END, f"> {message}\n")
        loading_text.insert(tk.END, f"{random_line}\n")
        loading_text.see(tk.END)

        msg_index += 1
        time.sleep(0.25)


# ================== PROGRESS HOOK ==================
def progress_hook(d):
    global downloaded_playlist_bytes, current_video_bytes

    # Pause handling
    while not pause_event.is_set():
        time.sleep(0.2)

    if d['status'] == 'downloading':
        total = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)

        if total:
            percent = int(downloaded / total * 100)
            video_progress_var.set(percent)

            delta = downloaded - current_video_bytes
            current_video_bytes = downloaded
            downloaded_playlist_bytes += max(delta, 0)

            overall_percent = int((downloaded_playlist_bytes / total_playlist_bytes) * 100)
            playlist_progress_var.set(overall_percent)

            overall_label.config(
                text=f"Overall: {format_mb(downloaded_playlist_bytes)} / "
                     f"{format_mb(total_playlist_bytes)} ({overall_percent}%)"
            )

            status_label.config(text=f"Downloading... {percent}%")

    elif d['status'] == 'finished':
        current_video_bytes = 0
        video_progress_var.set(100)
        status_label.config(text="Merging audio & video...")


# ================== DOWNLOAD ==================
def download_playlist():
    global total_playlist_bytes, downloaded_playlist_bytes, current_video_bytes, loading_running

    url = url_entry.get().strip()
    resolution = res_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter playlist URL")
        return

    total_playlist_bytes = 0
    downloaded_playlist_bytes = 0
    current_video_bytes = 0

    video_progress_var.set(0)
    playlist_progress_var.set(0)
    overall_label.config(text="Overall: calculating size...")

    loading_text.delete("1.0", tk.END)
    loading_running = True
    status_label.config(text="Preparing backend...")
    threading.Thread(target=matrix_loading, daemon=True).start()

    def task():
        global total_playlist_bytes, loading_running

        try:
            # Fetch playlist info
            with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                info = ydl.extract_info(url, download=False)

            playlist_title = safe_folder_name(info.get('title', 'YouTube_Playlist'))
            playlist_folder = os.path.join(os.getcwd(), playlist_title)
            os.makedirs(playlist_folder, exist_ok=True)

            for entry in info.get('entries', []):
                if entry:
                    size = entry.get('filesize') or entry.get('filesize_approx')
                    if size:
                        total_playlist_bytes += size

            if total_playlist_bytes == 0:
                raise Exception("Could not calculate playlist size")

            # Stop matrix animation
            loading_running = False
            loading_text.insert(tk.END, "\n> Backend ready. Starting download...\n\n")
            loading_text.see(tk.END)

            ydl_opts = {
                # 🎧 GUARANTEED audio + video
                'format': (
                    f'bestvideo[height<={resolution}][ext=mp4]'
                    f'+bestaudio[ext=m4a]/best[height<={resolution}]'
                ),

                'merge_output_format': 'mp4',

                # 🔊 CORRECT MERGER
                'postprocessors': [{
                    'key': 'FFmpegMerger',
                }],

                # 📁 FORCE playlist folder
                'outtmpl': os.path.join(
                    playlist_folder,
                    '%(playlist_index)s - %(title)s.%(ext)s'
                ),

                # 🌐 Stability
                'retries': 10,
                'fragment_retries': 10,
                'force_ipv4': True,
                'ignoreerrors': True,

                # 📊 Progress
                'progress_hooks': [progress_hook],
                'quiet': True,
                'no_warnings': True
            }


            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            status_label.config(text="✅ Download completed")
            messagebox.showinfo("Success", "Playlist downloaded successfully!")

        except Exception as e:
            loading_running = False
            status_label.config(text="❌ Error occurred")
            messagebox.showerror("Error", str(e))

    threading.Thread(target=task, daemon=True).start()


# ================== GUI ==================
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("650x600")
root.resizable(False, False)

tk.Label(root, text="YouTube Playlist Downloader", font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Playlist URL:").pack()
url_entry = tk.Entry(root, width=80)
url_entry.pack(pady=5)

tk.Label(root, text="Backend Activity :", anchor="w").pack(fill="x", padx=10)

loading_text = tk.Text(
    root,
    height=8,
    bg="black",
    fg="#00ff00",
    insertbackground="#00ff00",
    font=("Consolas", 10),
    relief="solid",
    bd=1
)
loading_text.pack(fill="x", padx=10, pady=5)

tk.Label(root, text="Select Resolution:").pack()
res_var = tk.StringVar(value="720")
ttk.Combobox(
    root,
    textvariable=res_var,
    values=["144", "240", "360", "480", "720", "1080", "1440", "2160"],
    state="readonly",
    width=25
).pack(pady=5)

tk.Label(root, text="Current Video Progress:").pack()
video_progress_var = tk.IntVar()
ttk.Progressbar(root, variable=video_progress_var, maximum=100).pack(fill="x", padx=20)

tk.Label(root, text="Overall Playlist Progress:").pack(pady=(10, 0))
playlist_progress_var = tk.IntVar()
ttk.Progressbar(root, variable=playlist_progress_var, maximum=100).pack(fill="x", padx=20)

overall_label = tk.Label(root, text="Overall: 0 MB / 0 MB (0%)", fg="green")
overall_label.pack(pady=5)

status_label = tk.Label(root, text="Waiting...", fg="blue")
status_label.pack()

tk.Button(
    root,
    text="Download Playlist",
    command=download_playlist,
    width=30,
    bg="#111827",
    fg="white",
    font=("Arial", 11, "bold")
).pack(pady=10)

pause_btn = tk.Button(
    root,
    text="Pause ⏸️",
    command=toggle_pause,
    width=30,
    bg="#374151",
    fg="white",
    font=("Arial", 11, "bold")
)
pause_btn.pack(pady=5)

root.mainloop()
