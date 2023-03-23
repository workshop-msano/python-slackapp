from dotenv import load_dotenv
load_dotenv()

from flask import Flask, redirect, request, url_for, render_template
from googleapiclient import discovery
import os

from components.cred import get_cred
from components.slack import get_posts


app = Flask(__name__)

@app.route('/slack/<mtd>',  methods=["POST", "GET"])
def slack(mtd):
    if request.method == "POST":
        return redirect(url_for(''))
    else:
        return render_template("index.html", method=mtd, url_for=url_for)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        method="post"

        # SPREADSHEET_ID = os.getenv("SHEET_ID")
        SPREADSHEET_ID = request.form["sheet-id"]
        CHANNEL = request.form["channel"]

        cred = get_cred()
        posts = get_posts(CHANNEL)


        service = discovery.build('sheets', 'v4', credentials=cred)


        RANGE_NAME = 'slackapp_test!A2' #シートと書き込み開始位置を指定/定値

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
        return redirect(url_for('slack', mtd=method))
    else:
        method="get"
        return redirect(url_for('slack', mtd=method))
    

if __name__ == "__main__":
    port = 8000
    app.run(debug=True, host='0.0.0.0', port=port)
    