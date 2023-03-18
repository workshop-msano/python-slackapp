import gspread
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv
load_dotenv()

from slack import get_posts

def main():
    #slack apiでデータを取得する
    posts = get_posts()
    # print(posts)
    # for post in posts:
    #     print(post)
    print("-----//")

    #スプレッドシート書き込み
    # お決まりの文句
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
    credentials = Credentials.from_service_account_file("./credential.json", scopes=scope)
    #OAuth2の資格情報を使用してGoogle APIにログイン。
    gc = gspread.authorize(credentials)
    #スプレッドシートIDを変数に格納する。
    SPREADSHEET_KEY = os.getenv("SHEET_ID")
    # スプレッドシート（ブック）を開く
    workbook = gc.open_by_key(SPREADSHEET_KEY)
    # シートを開く
    worksheet = workbook.worksheet('slackapp_test')
    
    # セルA1に”test value”という文字列を代入する。
    worksheet.update_cell(1, 1, 'slackapp_test')


if __name__ == "__main__":
    main()
