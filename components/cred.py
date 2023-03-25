import google_auth_oauthlib.flow
from google.oauth2.service_account import Credentials
import os


def get_auth():
    # Use the client_secret.json file to identify the application requesting
    # authorization. The client ID (from that file) and access scopes are required.

    CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    # client_secret_file=str(CURR_DIR)+'/client_secret.json'
    # flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
    #     client_secret_file,
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        '/etc/secrets/client_secret_file',
        scopes=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive'])

    # Indicate where the API server will redirect the user after the user completes
    # the authorization flow. The redirect URI is required. The value must exactly
    # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
    # configured in the API Console. If this value doesn't match an authorized URI,
    # you will get a 'redirect_uri_mismatch' error.

    flow.redirect_uri = 'https://slack-chat-catcher.onrender.com'


    # Generate URL for request to Google's OAuth 2.0 server.
    # Use kwargs to set optional request parameters.
    authorization_url, state = flow.authorization_url(
        # Enable offline access so that you can refresh an access token without
        # re-prompting the user for permission. Recommended for web server apps.
        access_type='offline',
        # Enable incremental authorization. Recommended as a best practice.
        include_granted_scopes='true')
    return {"authorization_url": authorization_url, "state":state}


def get_cred():
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']

    #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
    # CURR_DIR = os.path.dirname(os.path.realpath(__file__))
    # print("CURR_DIR: ", CURR_DIR)
    # credential_file=str(CURR_DIR)+'/credentials.json'
    # print("credential_file: ", credential_file)
    # credentials = Credentials.from_service_account_file(credential_file, scopes=scope)
    credentials = Credentials.from_service_account_file('/etc/secrets/credentials.json', scopes=scope)

    return credentials
