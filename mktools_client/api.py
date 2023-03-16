from pathlib import Path
from tkinter import simpledialog
import os
import json
import requests

track_cache = {}

def get_token():
    path = Path.home() / ".mktools" / "credentials.json"
    os.makedirs(path.parent, exist_ok=True)

    if path.exists():
        with open(path) as f:
            creds = json.load(f)
    else:
        creds = {}

    token = creds.get("access-token") 
    if isinstance(token, str):
        return token

    token = simpledialog.askstring("mktools", "Access https://mktools.ebiyuu.com/access-token/ and paste token!!")
    creds["access-token"] = token
    with open(path, "w") as f:
        json.dump(creds, f)
    return token

def register_record(time, track, comment):
    requests.post(
        "https://mktools.ebiyuu.com/api/record/",
        json={
            "time": time,
            "track": track,
            "comment": comment,
        },
        headers={
            "Authorization": "Token " + get_token(),
        },
    )
    del track_cache[track]

def get_track_info(track_id):
    if track_id in track_cache:
        return track_cache[track_id]

    res = requests.get(
        f"https://mktools.ebiyuu.com/api/track/{track_id}/",
        headers={
            "Authorization": "Token " + get_token(),
        },
    ).json()
    track_cache[track_id] = res
    return res


if __name__ == "__main__":
    register_record()
