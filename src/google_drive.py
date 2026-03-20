import re
import requests


def extract_file_id(drive_url):
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", drive_url)
    return match.group(1) if match else None


def get_file_bytes(drive_url):

    file_id = extract_file_id(drive_url)

    if not file_id:
        return None

    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(url)

    return response.content