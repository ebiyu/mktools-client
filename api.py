from pathlib import Path
import json
import requests

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


if __name__ == "__main__":
    register_record()
