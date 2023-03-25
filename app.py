from dotenv import load_dotenv
load_dotenv()

from googleapiclient import discovery
from flask import Flask, redirect, request, url_for, render_template, session
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker

from components.cred import get_cred, get_auth
from components.slack import get_posts

import os


app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
Bootstrap(app)
datepicker(app)


@app.route('/slack/<mtd>',  methods=["POST", "GET"])
def slack(mtd):
    if request.method == "POST":
        return redirect(url_for(''))
    else:
        return render_template("index.html", method=mtd, url_for=url_for)


@app.route("/", methods=["POST", "GET"])
def index():
    cred = get_cred()
    if request.method == "POST":
        method="post"

        SPREADSHEET_ID = request.form["sheet-id"]
        CHANNEL = request.form["channel"]
        START_DATE = request.form["start_date"]
        END_DATE=request.form["end_date"]

        try:
            posts = get_posts(CHANNEL, START_DATE, END_DATE)

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
        except:
            return render_template("index.html", method="error")
    else:
        if "state" not in session:
            auth=get_auth()
            session["state"]=auth["state"]
            return redirect(auth["authorization_url"])
        method="get"
        return redirect(url_for('slack', mtd=method))


@app.route("/signout", methods=["POST", "GET"])
def signout():
    if "state" in session:
        del session["state"]
        return render_template("signout.html")

    
if __name__ == "__main__":
    port = 8000
    app.run(debug=True, host='0.0.0.0', port=port)
    