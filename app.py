from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, request, url_for, render_template
from googleapiclient import discovery
import os

from components.cred import get_cred
from components.slack import get_posts


app = Flask(__name__)

@app.route('/slack/<msg>',  methods=["POST", "GET"])
def slack(msg):
    if request.method == "POST":
        return redirect(url_for(''))

    else:
        return render_template("index.html", message=msg, url_for=url_for)



@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        message="post"
        return redirect(url_for('slack', msg=message))
    else:
        message="get"
        return redirect(url_for('slack', msg=message))
    

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
    