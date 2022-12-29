from flask import Flask
from flask import request
from flask import Response
import requests
import os
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument('graph', type=str, help='Graph page address')
parser.add_argument('token', type=str, help='Bot token')
parser.add_argument('path', type=str, help='Path to project')

TOKEN = ''

PROJECT_PATH = ''

GRAPH_PAGE = ''

app = Flask(__name__)

def tmux(command):
    os.system('tmux %s' % command)

def tmux_shell(command):
    tmux('send-keys "%s" "C-m"' % command)
 
def parse_message(message):
    print("message-->",message)
    print(message)
    # print(list(message.keys())[1])
    chat_id = 0
    txt = ''
    # exit(0)
    try:
        chat_id = message['message']['chat']['id']
        txt = message['message']['text'].split()
    except:
        # message = message['edited_message']
        # print(message)
        special_type = list(message.keys())[1]
        chat_id = message[special_type]['chat']['id']
        txt = message['edited_message']['text'].split()
    
    print(txt)
    argument = ''
    if len(txt) > 2:
        txt = 'incorrect_command'
    elif len(txt) == 2:
        argument = txt[1]
        txt = txt[0]
    else:
        txt = txt[0]
    print("chat_id-->", chat_id)
    print("txt-->", txt)
    return chat_id, txt, argument
 
def tel_send_message(chat_id, text): 
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {
                'chat_id': chat_id,
                'text': text
                }
   
    r = requests.post(url,json=payload)
    return r


 
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, txt, argument = parse_message(msg)
        if txt == 'hi' or txt == '/hi':
            tel_send_message(chat_id, 'Hello!!')

        elif txt == '/start_learning':
            tmux('new-session -d -s bm_learn')
            tmux_shell('cd %s' % PROJECT_PATH)
            tmux_shell('/bin/python3 %ssrc/train.py' % PROJECT_PATH)
        
        elif txt == '/stop_learning':
            tmux('kill-server')

        elif txt == '/show_stat':
            f = open(PROJECT_PATH + "tmp.txt", "r")
            tel_send_message(chat_id, f.read())

        elif txt == '/show_graph':
            tel_send_message(chat_id, GRAPH_PAGE)

        elif txt == '/change_lr':
            # json_line = f'lr: {argument}'
            with open(PROJECT_PATH + 'config.json', 'r+') as config:
                data = json.load(config)
                data["lr"] = argument
            with open(PROJECT_PATH + 'config.json', "w") as config:
                json.dump(data, config, indent=4)
            tel_send_message(chat_id, f'Learning rate now: {argument}') 

        elif txt == '/change_bs':
            # json_line = f'lr: {argument}'
            with open(PROJECT_PATH + 'config.json', 'r+') as config:
                data = json.load(config)
                data["batch_size"] = argument
            with open(PROJECT_PATH + 'config.json', "w") as config:
                json.dump(data, config, indent=4)
            tel_send_message(chat_id, f'Batch_size rate now: {argument}') 

        elif txt == '/get_config':
           with open(PROJECT_PATH + 'config.json', 'r+') as config:
            data = json.load(config)
            json_formatted_str = json.dumps(data, indent=4)
            tel_send_message(chat_id, json_formatted_str)
            tel_send_message(chat_id, "use this commands to edit config file")
            tel_send_message(chat_id, "/change_lr learning_rate")
            tel_send_message(chat_id, "/change_bs batch_size")

        elif txt == 'incorrect_command':
            tel_send_message(chat_id, 'Your wrote invalid command')

        elif (txt == '-h') or (txt == '--h') or (txt == 'help') or (txt == '/help'):
            tel_send_message(chat_id, 'Use /get_config to see learning config file')
            tel_send_message(chat_id, 'Use /start_learning to start learning procces')
            tel_send_message(chat_id, 'Use /stop_learning to stop learning procces')
            tel_send_message(chat_id, 'Use /show_stat to see last recordes learning stats')
            tel_send_message(chat_id, 'Use /show_graph to get link on tensorboard data')

        else:
            tel_send_message(chat_id, 'Use -h or /help to get bot information message')

       
        return Response('ok', status=200)
    elif request.method == 'GET':
        return "hello"

 
if __name__ == '__main__':

    args = parser.parse_args()
    GRAPH_PAGE = args.graph
    TOKEN = args.token
    PROJECT_PATH = args.path
    print(GRAPH_PAGE)
    app.run(debug=True)