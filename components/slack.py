import requests
import datetime, os

SLACK_URL_HIS = "https://slack.com/api/conversations.history"
SLACK_URL_REP = "https://slack.com/api/conversations.replies"
SLACK_URL_USERSINFO = "https://slack.com/api/users.info"

TOKEN = os.getenv("TOKEN") 

def get_posts(channel_id, start_date, end_date):
    formated_start_date = datetime.datetime.strptime(start_date,"%Y-%m-%d")
    Unix_start_date_timestamp = datetime.datetime.timestamp(formated_start_date) 
    formated_end_date = datetime.datetime.strptime(end_date,"%Y-%m-%d")
    Unix_end_date_timestamp = datetime.datetime.timestamp(formated_end_date) 


    payload = {
        "channel": channel_id,
        "oldest" : Unix_start_date_timestamp,  
        "latest" : Unix_end_date_timestamp,
        "inclusive": True
    }
    headersAuth = {
    'Authorization': 'Bearer '+ str(TOKEN),
    }  

    #slack投稿からmainメッセージ取得
    response_main = requests.get(SLACK_URL_HIS, headers=headersAuth, params=payload)
    json_data = response_main.json()
    msgs = json_data['messages']

    #slack投稿からreplyメッセージ取得
    result = []
    for msg in msgs:
        payload['ts'] = msg['ts'] #update payload
        response_reply = requests.get(SLACK_URL_REP, headers=headersAuth, params=payload)
        json_data = response_reply.json()
        include_reply_msgs = json_data['messages']

        #投稿ユーザーのreal nameを取得
        for inner_msg in include_reply_msgs:
            info = [] 
            payload['user'] = inner_msg['user'] #update payload
            response_usersinfo = requests.get(SLACK_URL_USERSINFO, headers=headersAuth, params=payload)
            json_data = response_usersinfo.json()

            info.append(datetime.datetime.fromtimestamp(float(inner_msg['ts'])).strftime('%Y-%m-%d %H:%M:%S'))
            info.append(inner_msg['user']) #user id
            info.append(json_data['user']['profile']['real_name']) #user name
            info.append(inner_msg['text']) #text 
            if "parent_user_id" in inner_msg : #is text reply(True) or not(False)
                info.append(True)
            else:
                info.append(False)
                        
            result.append(info)
    return result


if __name__ == "__main__":
    get_posts()