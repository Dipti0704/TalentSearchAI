import gspread
from google.oauth2.service_account import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]


def get_sheet():

    creds = Credentials.from_service_account_file(
        "credentials.json",
        scopes=SCOPES
    )

    client = gspread.authorize(creds)

    #  OPEN FIRST SHEET AUTOMATICALLY (no name dependency)
    spreadsheet = client.openall()[0]
    sheet = spreadsheet.sheet1

    return sheet


def map_columns(headers):

    mapping = {}

    for h in headers:
        h_lower = h.lower()

        if "name" in h_lower:
            mapping["name"] = h

        elif "email" in h_lower and "sst" not in h_lower:
            mapping["email"] = h

        elif "resume" in h_lower:
            mapping["resume"] = h

    return mapping


def get_candidates():

    sheet = get_sheet()

    rows = sheet.get_all_records()
    headers = sheet.row_values(1)

    mapping = map_columns(headers)

    candidates = []

    for r in rows:

        candidate = {
            "name": r.get(mapping.get("name")),
            "email": r.get(mapping.get("email")),
            "resume_link": r.get(mapping.get("resume"))
        }

        # skip invalid rows
        if candidate["resume_link"]:
            candidates.append(candidate)

    return candidates