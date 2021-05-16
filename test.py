import subprocess
import os
from pytube import YouTube
url = "https://www.youtube.com/watch?v=sy1MNWt7om4"
video = YouTube(url)
subprocess.Popen("pytube {0}".format(url))
# while True:
#     if os.path.exists(video.title):
#         break
print("Download Started:",video.title)