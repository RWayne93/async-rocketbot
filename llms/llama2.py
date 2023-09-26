from hugchat import hugchat
from hugchat.login import Login
from utils.credentials import load_env

creds = load_env()

def setup_hugging_chat():
    email = creds['hug_email']
    passwd = creds['hug_pass']
    sign = Login(email, passwd)
    cookies = sign.login()
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    return chatbot

chatbot_instance = setup_hugging_chat()