from src.google_sheets import get_sheet


def highlight_candidate(email):

    sheet = get_sheet()

    rows = sheet.get_all_records()

    for i, row in enumerate(rows):

        if row["Email Address"] == email:

            row_number = i + 2  # header offset

            sheet.format(
                f"A{row_number}:I{row_number}",
                {
                    "backgroundColor": {
                        "red": 0,
                        "green": 1,
                        "blue": 0
                    }
                }
            )

            print("Highlighted:", email)

            break