import json
import os 
import webbrowser
import re
import time

TOKEN = '5781531761:AAF8FNJqhoFijcX-D1-ew5zy6Zr2tc9i7nA'

REGISTER_BOT = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url="

PROJECT_PATH = '/home/michael/Desktop/BM_Network/'

os.system("ngrok start --all > /dev/null &")

time.sleep(3)

os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")

with open('tunnels.json') as data_file:    
    datajson = json.load(data_file)


tg_addr = ""
graph_addr = ""

for i in datajson['tunnels']:
    port = int(re.findall(r'(\d*)$',i['config']['addr'])[0])
    if (port == 5000):
        tg_addr = i['public_url']
    if (port == 6006):
        graph_addr = i['public_url']

os.system('rm tunnels.json')

webbrowser.open(REGISTER_BOT + tg_addr)

os.system(f'tensorboard --logdir {PROJECT_PATH} --port 6006 > /dev/null &')

os.system(f'python3 src/server.py {graph_addr} {TOKEN} {PROJECT_PATH}')