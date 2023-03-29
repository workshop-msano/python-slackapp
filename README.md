# 🧐 Slack Chat Catcher

> _Automate aggregating number of messages and reduce workload_

# 🔥 Motivation

Reduce workload for staffs aggregating posted messages.

This app will:

- Enter the Slack Channel ID, Google Spread Sheet ID and set period of time. Then run the application, it will automatically update Google Spreadsheet with results.

# 🛫 Getting Started

Before running any scripts, you'll need additional setups. After 2 steps, you should run the next command.

```shell
$ pip install-r requirements.txt
$ python app.py
```

Steps:

1. Setup API key and environment variables


## 🔑 1. Setup API Key for GCP

1. [Visit Google Developer Console](https://console.developers.google.com/) and create a new project.

- Enable Google Sheets API
- Create service account
- Create OAuth 2.0 client ID
- Download JSON files (Name the file as `client_secret.json` from service account and `credentials.json` from 0Auth 2.0 client ID), set files in root directory. 

## 🔑 2. Setup Token for Slack 

1. [Acces Slack API](https://api.slack.com/apps) and create a new app

- Set permission. The permisson should cover :
    - conversations.history, conversations.replies and users.info
- Issue a token 

After creating all necessary keys, run next command and paste appropriate values.
Please modefy the SECRET_KEY. 

```shell
$ cp .env.example .env
```

> _Note: To develop this app with Pyhon, making virtual environment is recommended.  


# 🛠 How To Use

Enter the Slack Channel ID, Google Spread Sheet ID and set period of time.
Then click the `submit` button to get messages and update Google Spreadsheet.

# 🚧 Warning

This app is:

- Expected to be a temporary solution
- Not designed to be scalable
- Not designed for mobile or with accessability (some are included in UI library)

# ⛓ Reference

- [Create a Google Cloud project](https://developers.google.com/workspace/guides/create-project)
- [Google Sheets API](https://console.cloud.google.com/apis/library/sheets.googleapis.com)
- [Create the OAuth web client ID](https://support.google.com/workspacemigrate/answer/9222992) 
- [Slackの特定チャンネルのメッセージをクロールする方法](https://qiita.com/yoshii0110/items/2a7ea29ca8a40a9e42f4)
- [conversations.history](https://api.slack.com/methods/conversations.history)
- [conversations.replies](https://api.slack.com/methods/conversations.replies)
- [users.info](https://api.slack.com/methods/users.info)
- [SlackのチャンネルIDを調べる方法](https://auto-worker.com/blog/?p=132)