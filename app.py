from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route("/search", methods=["GET", "POST"])
def search_bar():
    if request.method == "POST":
        artist = request.form["artist"]
        return get_artist(artist)
    else:
        return render_template("search_bar.html")

@app.route("/artist/<artist>", methods=["GET"])
def get_artist(artist):
    url = f"https://api.deezer.com/search/artist?q={artist}"
    response = requests.get(url)
    if response.status_code == 200:
        artist_data = response.json()
        tracklist_url = artist_data["data"][0]["tracklist"]
        top_five_url = tracklist_url.replace("50", "5")
        response = requests.get(top_five_url)
        track_data = response.json()
        tracks = [i["title"] for i in track_data["data"]]
        return render_template("artist.html", data=tracks)
    else:
        return "Error fetching artist data from API"