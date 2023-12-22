from typing import Optional
from flask import Flask, render_template
from pathlib import Path
from flask.config import ConfigAttribute
from slugify import slugify
import logging
import os

app = Flask(__name__)


class Song:
    def __init__(self, song_id: str, author: str, name: str, contents_func):
        self.id = song_id
        self.author = author
        self.name = name
        self._contents_func = contents_func

    def contents(self) -> str:
        return self._contents_func()
    
    def slug(self):
        return slugify(f"{self.author}-{self.name}")



class Storage:
    def __init__(self, base_dir: Path):
        self._base_dir = base_dir
        self._songs = {s.id: s for s in [
            Song("1", "Author #1" ,"A Song", lambda: "contents!"),
            Song("2", "Another band!", "Another song!", lambda: "more\ncontents!"),
        ]}

    def get_songs(self) -> list[Song]:
        return sorted(self._songs.values(),key= lambda s: (s.author, s.name))

    def get_song(self, song_id) -> Optional[Song]:
        try:
            return self._songs[song_id]
        except KeyError:
            return None


_STORAGE = Storage(Path(os.path.expanduser("~/.chorddb")))

@app.route("/")
def home():
    return render_template("home.html", songs=_STORAGE.get_songs())


@app.route("/song/<song_id>/<song_slug>")
def song(song_id, song_slug):
    song = _STORAGE.get_song(song_id)
    if song is None:
        return "Song not found", 404
    return render_template("song.html", song=song)


def run(debug=False):
    logging.info("About to run WEB mode")
    app.run(debug=debug)

