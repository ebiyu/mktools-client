from pathlib import Path
import json
import requests

track_cache = {}

def get_token():
    path = Path("token.json")
    if not path.exists():
        token = input("Access https://nita.ebiyuu.com/access-token/ and paste token !! > ")
        with open(path, "w") as f:
            json.dump(token, f)
        return token
    with open(path) as f:
        token = json.load(f)
    return token

def register_record(time, track, comment):
    requests.post(
        "https://nita.ebiyuu.com/api/record/",
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
        f"https://nita.ebiyuu.com/api/track/{track_id}/",
        headers={
            "Authorization": "Token " + get_token(),
        },
    ).json()
    track_cache[track_id] = res
    return res


if __name__ == "__main__":
    register_record()
