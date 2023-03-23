from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, request, url_for
from googleapiclient import discovery
import os

from components.cred import get_cred
from components.slack import get_posts


app = Flask(__name__)

@app.route('/message/<msg>')
def message(msg):
   return '%s' % msg

message=""
@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        message="post"
        return redirect(url_for('message', msg=message))
    else:
        message="get"
        return redirect(url_for('message', msg=message))
    

# posts = get_posts()
# cred = get_cred()


# service = discovery.build('sheets', 'v4', credentials=cred)

# SPREADSHEET_ID = os.getenv("SHEET_ID")
# RANGE_NAME = 'slackapp_test!A2' #シートと書き込み開始位置を指定

# value_input_option = 'RAW'
# range_name = RANGE_NAME
# values = posts
# data = [
#     {
#         'range': range_name,
#         'values': values
#     },
# ]
# body = {
# 'valueInputOption': value_input_option,
# 'data': data
# }
# result = service.spreadsheets().values().batchUpdate(
#     spreadsheetId=SPREADSHEET_ID, body=body).execute()
# print(result)


if __name__ == "__main__":
    port = 8000
    app.run(debug=True, host='0.0.0.0', port=port)
    