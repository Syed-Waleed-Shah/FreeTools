from flask import Flask, render_template, request, send_from_directory, jsonify, send_file
from flask_restful import Resource, Api, reqparse, abort 
import subprocess
from pytube import YouTube
import time
import os


app = Flask(__name__)
api = Api(app)
@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == "POST" and request.form.get("YoutubeVideoDownload"):
        # url = request.form.get("url")
        # from pytube import YouTube
        # path = YouTube(url).streams[0].download()
        return send_from_directory(os.path.join(app.root_path, 'static'), "style.css")
    return render_template('youtube.html')


@app.route('/download')
def download():
    url = request.args.get("url")    
    video = YouTube(url)
    subprocess.Popen("pytube {0}".format(url))
    time.sleep(5)
    return send_file(video.title+".mp4", as_attachment=True)

@app.route('/test')
def test():
    url = request.args.get("url")
    return send_file(url, as_attachment=True)


# ----------------------------------------------------
# ALL RESOURCES OF API
# ----------------------------------------------------

class YoutubeVideoInfo(Resource):
    def get(self):
        from pytube import YouTube
        url = request.args.get("url")
        video = YouTube(url)
        return jsonify({
            "meta": {
                "status":"200"
            },
            "data": {
            "title":video.title,
            "thumbnailUrl":video.thumbnail_url,
            "views":video.views,
            "id":video.video_id,                    
            }
        })

# ----------------------------------------------------
# ALL ROUTES OF API
# ----------------------------------------------------
api.add_resource(YoutubeVideoInfo, "/api/v1/youtube/videoinfo")


if __name__ == '__main__':
    app.run(debug=True, port=5002)