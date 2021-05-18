import subprocess
import os
from pytube import YouTube, Playlist
url = "https://www.youtube.com/watch?v=sy1MNWt7om4"


def getVideoInfo(url):
    video = YouTube(url)
    audios = video.streams.filter(only_audio=True)
    videos = video.streams.filter(only_video=True)
    for audio in audios:
        print(audio.title)
        print(audio.mime_type)
        print(audio.abr)
    # print(audio.filesize)
    # print("%.2f" % round(audio.filesize/1024/1024,2))

    for video in videos:
        print(video.mime_type)
        print(video.resolution)


def getPlaylistInfo(url):
    result = []
    yt = Playlist(url)
    videos = yt.videos
    for video in videos:
        audio_streams = video.streams.filter(only_audio=True)
        video_streams = video.streams.filter(only_video=True)
        videosjson = []
        audiosjson = []
        for v in video_streams:
            videosjson.append(
                {
                    "itag":v.itag, "mime_type":v.mime_type, "resolution":v.resolution
                }
            )
        for a in audio_streams:
            audiosjson.append(
                {
                    "itag":a.itag, "mime_type":a.mime_type, "resolution":a.abr
                }
            )

        result.append({
        "title":video.title, "thumbnail":video.thumbnail_url, "views":video.views, "url":"https://youtube.com/watch?v="+video.video_id,
        "videos":videosjson, "audios":audiosjson
        })

    return result


if __name__ == "__main__":
    playlist = getPlaylistInfo("https://www.youtube.com/playlist?list=PLXkEfqYbulLEUsu_kvIcbi8JeKN2iMoux")
    print(playlist)
    

    
