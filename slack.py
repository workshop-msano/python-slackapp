import requests
import datetime, time, os

SLACK_CHANNEL_ID = 'CUF6LFWFR'
SLACK_URL_HIS = "https://slack.com/api/conversations.history"
SLACK_URL_REP = "https://slack.com/api/conversations.replies"
SLACK_URL_USERSINFO = "https://slack.com/api/users.info"

TOKEN = os.getenv("TOKEN") 

def get_posts():
    today = datetime.date.today()
    end_date = today + datetime.timedelta(days=1)
    # start_date = today + datetime.timedelta(days=-10)
    start_date = "1/31/2023" #取得開始日
    formated_start_date = datetime.datetime.strptime(start_date,"%m/%d/%Y")
    Unix_start_date_timestamp = datetime.datetime.timestamp(formated_start_date) 
    # print(Unix_start_date_timestamp)

    payload = {
        "channel": os.getenv("CHANNEL"),
        "latest": time.mktime(end_date.timetuple()),
        # "oldest" : time.mktime(start_date.timetuple()),  
        "oldest" : Unix_start_date_timestamp,  
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
        # print(include_reply_msgs)

        #投稿ユーザーのreal nameを取得
        for inner_msg in include_reply_msgs:
            info = {}
            payload['user'] = inner_msg['user'] #update payload
            response_usersinfo = requests.get(SLACK_URL_USERSINFO, headers=headersAuth, params=payload)
            json_data = response_usersinfo.json()
            # print(json_data)

            info["timestamp"] = datetime.datetime.fromtimestamp(float(inner_msg['ts'])).strftime('%Y-%m-%d %H:%M:%S')
            info["user_id"] = inner_msg['user']
            info["text"] = inner_msg['text']
            if "parent_user_id" in inner_msg : 
                info["is_reply"] = True
            else:
                info["is_reply"] = False
            
            info["real_name"] = json_data['user']['profile']['real_name']
            
            # print(inner_msg)
            # print("-----")
            result.append(info)
    # print(result)
    return result


if __name__ == "__main__":
    get_posts()