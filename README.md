# youtube-playlist-downloader

📥 YouTube Playlist Downloader (Python GUI)

A Python-based desktop application that allows users to download entire YouTube playlists with video and audio merged, resolution selection, real-time progress tracking, pause/resume, and a Matrix-style backend loading animation.

* ⚠️ This project is intended for educational and personal use only.
* 🚀 Features
* ✅ Download complete YouTube playlists
* 🎞️ Multiple resolution support (144p – 2160p)
* 🔊 Automatic audio + video merging (no silent videos)
* 📁 Playlist-wise folder creation
* 📊 Real-time video & playlist progress tracking
* ⏸️ Pause and resume download
* 💻 Matrix-style backend activity animation
* 🧵 Multithreaded (GUI never freezes)
* 🎨 Clean and user-friendly interface

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

:🛠️ Tech Stack & Libraries
Technology                    	Purpose
Python                          3.8+	Core programming language
Tkinter                       	GUI design
yt-dlp	                        YouTube playlist & video downloading
FFmpeg	                        Merging video and audio
threading	                      Background downloads
os, re	                        File & folder handling
time, random, string	          Animation & delays

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

:💻 System Requirements

* Hardware
Minimum 4 GB RAM
At least 2 GB free storage
Stable internet connection

* Software
Windows / Linux / macOS
Python 3.8 or above
FFmpeg installed and added to PATH

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

📦 Installation & Setup

1️⃣ Clone the repository
git clone https://github.com/himanshu7714/youtube-playlist-downloader

2️⃣ Install required Python library
pip install yt-dlp
-Tkinter comes pre-installed with Python.

3️⃣ Install FFmpeg

Windows:
Download from https://ffmpeg.org
 → add to PATH
 
Linux:
sudo apt install ffmpeg

macOS:
brew install ffmpeg

Verify:
ffmpeg -version

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

▶️ How to Run the Application
* Run python main.py in vscode /python IDLE

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

🧑‍💻 How to Use

* Launch the application

* Paste a YouTube playlist URL

* Select desired video resolution

* Click Download Playlist

* Watch live progress and backend activity

* Use Pause / Resume if needed

* Videos will be saved in a playlist-named folder

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

⚠️ Limitations

* Requires internet connection
* Cannot download private or restricted playlists
* Not intended for commercial use
* Subject to YouTube Terms of Service

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

🔮 Future Enhancements

* 🌐 Web-based version
* 📱 Android application
* 🎵 Audio-only download option
* 📦 ZIP download feature
* 🎨 Enhanced UI themes

///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

🎓 Academic Use
* This project was developed as a college Python project to demonstrate:
* GUI development
* Multithreading
* Third-party library integration
* Real-world problem solving

 ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

📜 Disclaimer

This project is for educational purposes only.
Downloading copyrighted content may violate YouTube’s Terms of Service.

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

👤 Author

Himanshu Varma
BCA (AI & ML) – Galgotias University
📧 himanshu69byte@gmail.com
🔗 GitHub

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

⭐ Support
If you like this project:
* ⭐ Star the repository
* 🍴 Fork it
* 🐛 Report issues
