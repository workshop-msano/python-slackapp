import requests
import datetime, time, os
from dotenv import load_dotenv

load_dotenv()

SLACK_CHANNEL_ID = 'CUF6LFWFR'
SLACK_URL_HIS = "https://slack.com/api/conversations.history"
SLACK_URL_REP = "https://slack.com/api/conversations.replies"
SLACK_URL_USERSINFO = "https://slack.com/api/users.info"

TOKEN = os.getenv("TOKEN")

def main():
    today = datetime.date.today() #ファイル実行のタイミングに注意
    start_date = today + datetime.timedelta(days=-7)
    end_date = today + datetime.timedelta(days=1)

    payload = {
        "channel": 'CUF6LFWFR',
        "latest": time.mktime(end_date.timetuple()),
        "oldest" : time.mktime(start_date.timetuple()),  
        "inclusive": True
    }
    headersAuth = {
    'Authorization': 'Bearer '+ str(TOKEN),
    }  
    #mainメッセージ取得
    response_main = requests.get(SLACK_URL_HIS, headers=headersAuth, params=payload)
    json_data = response_main.json()
    msgs = json_data['messages']

    #replyメッセージ取得
    result = []
    for msg in msgs:
        payload['ts'] = msg['ts'] #update payload
        response_reply = requests.get(SLACK_URL_REP, headers=headersAuth, params=payload)
        json_data = response_reply.json()
        include_reply_msgs = json_data['messages']

        for msg in include_reply_msgs:
            info = {}
            payload['user'] = msg['user'] #update payload
            response_usersinfo = requests.get(SLACK_URL_USERSINFO, headers=headersAuth, params=payload)
            json_data = response_usersinfo.json()
            info["real_name"] = json_data['user']['real_name']
            info["user_id"] = msg['user']
            info["text"] = msg['text']
            if "parent_user_id" in msg : 
                info["is_reply"] = True
            else:
                info["is_reply"] = False
            
            print(info)
            print("-----")
            result.append(info)
    print(result)
    return result


if __name__ == "__main__":
    main()