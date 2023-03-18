from dotenv import load_dotenv
load_dotenv()

from googleapiclient import discovery
import os

from components.cred import get_cred
from components.slack import get_posts


def main():
    posts = get_posts()
    cred = get_cred()

    service = discovery.build('sheets', 'v4', credentials=cred)

    SPREADSHEET_ID = os.getenv("SHEET_ID")
    RANGE_NAME = 'slackapp_test!A2' #シートと書き込み開始位置を指定

    value_input_option = 'RAW'
    range_name = RANGE_NAME
    values = posts
    data = [
        {
            'range': range_name,
            'values': values
        },
    ]
    body = {
    'valueInputOption': value_input_option,
    'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body).execute()
    print(result)


if __name__ == "__main__":
    main()
