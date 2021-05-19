from flask import Flask, render_template, request, send_from_directory, jsonify, send_file
from flask_restful import Resource, Api, reqparse, abort 
from flask_cors import CORS
import _thread as thread
import subprocess
from pytube import YouTube, Playlist
from pytube.exceptions import VideoUnavailable
from sanitize_filename import sanitize
import time
import random
import os


def downloadVideo(url, itag, title):
    while True:
        try:
            yt = YouTube(url)
            yt.streams.get_by_itag(itag).download(os.path.join(app.root_path , "Videos"), sanitize(title),   max_retries=5)
        except:
            pass
        else:
            break
    

def getVideDetails(url):   
    try:
        yt = YouTube(url)
    except:
        return {"error":404}
    else:
        while True:
            try:
                videos = yt.streams.filter(file_extension="mp4").filter(only_video=True)
            except:
                pass
            else:
                break

        videosjson = []
        for video in videos:
            videosjson.append(
                {
                    "itag":video.itag, "mime_type":video.mime_type, "resolution":video.resolution, "download_url":video.url
                }
            )       

        return {
            "title":yt.title, "thumbnail":yt.thumbnail_url, "views":yt.views, "url":url,
            "videos":videosjson
        }

def getPlaylistDetails(url):
    result = []
    try:
        yt = Playlist(url)  
    except VideoUnavailable:
        pass
    else:
        videos = yt.videos
        for video in videos:       
            while True:            
                try: 
                    video_streams = video.streams.filter(file_extension="mp4").filter(only_video=True)
                except:
                    pass
                else:
                    break


            videosjson = []
            for v in video_streams:
                videosjson.append(
                    {
                        "itag":v.itag, "mime_type":v.mime_type, "resolution":v.resolution
                    }
                )           
            result.append({
            "title":video.title, "thumbnail":video.thumbnail_url, "views":video.views, "url":"https://youtube.com/watch?v="+video.video_id, "id":video.video_id,
            "videos":videosjson
            })

    return result


app = Flask(__name__)
CORS(app)
api = Api(app)
@app.route('/', methods=["GET", "POST"])
def index():    
    if request.method == "POST" and request.form.get("YoutubeVideoDownload"):
        url = request.form.get("url")
        videodetails = getVideDetails(url)       
        return render_template('youtube.html', videodetails=videodetails)
    return render_template('youtube.html')


# Youtube video downloader
@app.route('/tools/youtube/youtube-video-downloader', methods=["GET", "POST"])
def youtubevideodownloader():
    if request.method == "POST" and request.form.get("YoutubeVideoDownload"):
        url = request.form.get("url")
        videodetails = getVideDetails(url)       
        return render_template('youtube-video.html', videodetails=videodetails)
    return render_template('youtube-video.html')

# Youtube playlist downloader
@app.route('/tools/youtube/youtube-playlist-downloader', methods=["GET", "POST"])
def youtubeplaylistdownloader():
    if request.method == "POST" and request.form.get("YoutubeVideoDownload"):
        url = request.form.get("url")
        playlistdetails = getPlaylistDetails(url)       
        return render_template('youtube-playlist.html', playlistdetails=playlistdetails)
    return render_template('youtube-playlist.html')


@app.route('/download')
def download():
    url = request.args.get("url")    
    itag = request.args.get("itag")
    video = YouTube(url)
    title = "video_" + str(random.randrange(1000,20000))
    thread.start_new_thread(downloadVideo, (url, itag, title, ))    
    # return send_file(app.root_path + "\\Videos\\" + sanitize(title)+".mp4", as_attachment=True)
    while True:
        try:
            return send_file(os.path.join(app.root_path, "Videos" , sanitize(title)+".mp4"), as_attachment=True)
        except Exception as e:
            time.sleep(2)
            print(e)
        else:
            break



@app.route('/test')
def test():
    url = request.args.get("url")
    return send_file(url, as_attachment=True)

@app.route('/path-test')
def pathtest():
    return str(os.path.join(app.root_path, "Videos", "Audios"))


# ----------------------------------------------------
# ALL RESOURCES OF API
# ----------------------------------------------------

class YoutubeVideoInfo(Resource):
    def get(self):
        from pytube import YouTube
        url = request.args.get("url")
        yt = YouTube(url)
        audios =yt.streams.filter(only_audio=True)
        videos = yt.streams.filter(only_video=True)
        videosjson = []
        audiosjson = []
        for video in videos:
            videosjson.append(
                {
                    "itag":video.itag, "mime_type":video.mime_type, "resolution":video.resolution
                }
            )
        for audio in audios:
            audiosjson.append(
                {
                    "itag":audio.itag, "mime_type":audio.mime_type, "resolution":audio.abr
                }
            )

        return {
            "title":yt.title, "thumbnail":yt.thumbnail_url, "views":yt.views,
            "videos":videosjson, "audios":audiosjson
        }


# ----------------------------------------------------
# ALL ROUTES OF API
# ----------------------------------------------------
api.add_resource(YoutubeVideoInfo, "/api/v1/youtube/videoinfo")


if __name__ == '__main__':
    app.run(debug=True, port=5002)