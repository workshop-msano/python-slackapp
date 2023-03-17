import requests
import datetime, time

SLACK_CHANNEL_ID = 'CUF6LFWFR'
SLACK_URL_HIS = "https://slack.com/api/conversations.history"
SLACK_URL_REP = "https://slack.com/api/conversations.replies"
TOKEN = "xoxp-967572516294-964908956884-4981362419745-6550b98932bed8621b758f6cec1d05c1"

def main():
    today = datetime.date.today()
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
    # print(msgs)

    #replyメッセージ取得
    for item in msgs:
        payload['ts'] = item['ts']
        response_reply = requests.get(SLACK_URL_REP, headers=headersAuth, params=payload)
        json_data = response_reply.json()
        inner_msgs = json_data['messages']

        # print("rep msgs", inenr_msgs)
        for inner_item in inner_msgs:
            print(inner_item['user'])
            print(inner_item['text'])
            print("-----")


if __name__ == "__main__":
    main()