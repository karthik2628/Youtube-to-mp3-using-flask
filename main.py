from flask import Flask, request, send_file, render_template, redirect
from pytube import YouTube
import logging
import sys
from io import BytesIO
from tempfile import TemporaryDirectory
from flask_ngrok import run_with_ngrok


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
app = Flask(__name__)
run_with_ngrok(app)

@app.route("/")
def youtube_downloader():
     return render_template("audio.html" )


@app.route("/audio", methods=["GET","POST"])
def download_audio():
     try:
          youtube_url = request.form["URL"]
          with TemporaryDirectory() as tmp_dir:
               stream = YouTube(youtube_url).streams.filter(only_audio=True).all()
               path = stream[0].download(tmp_dir)
               name = path.split("\\")[-1]+".mp3"
               file_bytes = ""
               with open(path, "rb") as f:
                    file_bytes = f.read()
               return send_file(BytesIO(file_bytes), attachment_filename=name, as_attachment=True)
     except:
          logging.exception("Failed download")
          return render_template("fail.html")



if __name__ == "__main__":
    app.run()
