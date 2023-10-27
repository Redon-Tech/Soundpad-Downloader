from flask import Blueprint, render_template, request, redirect, url_for
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
from urllib.parse import quote_plus
from .soundpad import soundpad
import time
import os

main = Blueprint("main", __name__)
ydl_options = {
    # "YDL_FORMAT": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
    "noplaylist": "True",
}


@main.route("/")
def index():
    return render_template("index.html", title="Home")


@main.route("/search", methods=["GET", "POST"])
def search_get():
    search = request.args.get("search")
    if search is None:
        return render_template("search.html", title="Search")
    else:
        videos = {}

        for video in YoutubeSearch(search, max_results=15).to_dict():
            videos[len(videos) + 1] = video

        return render_template("search.html", title="Search", videos=videos)


@main.route("/download/<video_id>/<download_slot>/<title>", methods=["GET", "POST"])
def download(video_id, download_slot, title):
    if download_slot.isnumeric():
        try:
            os.remove(f"/audio/{download_slot}.mp3")
        except FileNotFoundError:
            pass
        options = ydl_options
        options["outtmpl"] = f"/audio/{download_slot}.%(ext)s"
    else:
        title = quote_plus(title)
        options = ydl_options
        options["outtmpl"] = f"/audio/{title}.%(ext)s"

    success = True
    try:
        with YoutubeDL(options) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
    except Exception as e:
        success = False
        print(e)

    if not download_slot.isnumeric():
        time.sleep(1)
        soundpad.addSound(f"{os.getcwd()}/audio/{title}.mp3")

    search = request.args.get("search")
    if search is None:
        return redirect(url_for("main.search_get", success=success))
    else:
        return redirect(url_for("main.search_get", search=search, success=success))
