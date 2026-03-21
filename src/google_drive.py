import re
import requests


def extract_file_id(drive_url):

    # file link
    match = re.search(r"/d/([a-zA-Z0-9_-]+)", drive_url)
    if match:
        return match.group(1)

    # open?id= format
    match = re.search(r"id=([a-zA-Z0-9_-]+)", drive_url)
    if match:
        return match.group(1)

    return None


def get_file_bytes(drive_url):
    
    if "folders" in drive_url:
        print("⚠️ Skipping folder link:", drive_url)
        return None

    file_id = extract_file_id(drive_url)

    if not file_id:
        return None

    url = f"https://drive.google.com/uc?export=download&id={file_id}"

    response = requests.get(url)

    return response.content