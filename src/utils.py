import json
import requests


def manage_request_error(r: requests.models.Response):
    if r.status_code != 200:
        try:
            error = json.loads(r._content.decode())
        except json.decoder.JSONDecodeError:
            print(f"{r.status_code}: {r._content.decode()}")
            r.raise_for_status()
        if "message" in error:
            print(error["message"])
        elif "detail" in error:
            print(error["detail"])
        else:
            print(error)
        r.raise_for_status()
