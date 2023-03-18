from dotenv import load_dotenv
load_dotenv()

# import gspread
from googleapiclient import discovery
import os

from cred import get_cred
from slack import get_posts


def main():
    posts = get_posts()
    # print(posts)
    # for post in posts:
    #     print(post)
    # print("-----//")

    #credential情報を取得する
    cred = get_cred()

    service = discovery.build('sheets', 'v4', credentials=cred)

    #スプレッドシートIDを変数に格納する。
    SPREADSHEET_ID = os.getenv("SHEET_ID")

    RANGE_NAME = 'slackapp_test!A3'

    value_input_option = 'RAW'
    range_name = RANGE_NAME
    values = [['aa']]
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
