import google_auth_oauthlib.flow
from google.oauth2.service_account import Credentials
import os


def handle_env():
    if os.environ.get("ENV_VAR") == 'DEVELOPMENT':
        env_var_info = {
            'client_secret_path' : os.path.abspath(os.path.basename("../client_secret.json")), 
            'credentials_path' : os.path.abspath(os.path.basename("../credentials.json")), 
            'redirect_url':'http://localhost:8000'}
    else:
        env_var_info = {
            'client_secret_path' : '/etc/secrets/client_secret.json', 
            'credentials_path' : '/etc/secrets/credentials.json', 
            'redirect_url':'https://slack-chat-catcher.onrender.com'}
    return env_var_info


def get_auth():
        env_var_info = handle_env()

        # Use the client_secret.json file to identify the application requesting
        # authorization. The client ID (from that file) and access scopes are required.
        flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
            env_var_info['client_secret_path'],
            scopes=['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive'])

        # Indicate where the API server will redirect the user after the user completes
        # the authorization flow. The redirect URI is required. The value must exactly
        # match one of the authorized redirect URIs for the OAuth 2.0 client, which you
        # configured in the API Console. If this value doesn't match an authorized URI,
        # you will get a 'redirect_uri_mismatch' error.
        flow.redirect_uri = env_var_info['redirect_url']


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
    env_var_info = handle_env()
    # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
    scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_file(env_var_info['credentials_path'], scopes=scope)
    return credentials
