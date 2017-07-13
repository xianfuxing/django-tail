import json
import time
import subprocess
import threading
from .utils import stop_thread
from django.conf import settings
from channels import Group
from channels.auth import channel_session_user, channel_session_user_from_http


global _groups
_groups = []

global _threads
_threads = []

@channel_session_user_from_http
def ws_connect(message):
    print('connect')
    log_id = message.reply_channel.name.split('.')[-1]
    log_id = log_id.replace('!', '1')
    _groups.append(log_id)

    LOGTAIL_FILE = getattr(settings, 'LOGTAIL_FILE', '')
    cmd = 'tail -f {0}'.format(LOGTAIL_FILE)
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    Group('logs'+log_id).add(message.reply_channel)

    for i in range(0, 10):
        line = popen.stdout.readline()
        Group('logs'+log_id).send({
                    'text': json.dumps({
                    'line': line.decode('utf-8'),
                    'is_logged_in': True
                })
            })

    def tail():
        while True:
            line = popen.stdout.readline()
            if line:
                for log_id in _groups:
                    Group('logs'+log_id).send({
                    'text': json.dumps({
                    'line': line.decode('utf-8'),
                    'is_logged_in': True
                })
            })
    global tailThread
    
    if _threads == []:
        print('create thread')
        tailThread = threading.Thread(name='tail', target=tail)
        tailThread.start()
        _threads.append(tailThread)
    else:
        Group('logs'+log_id).send({'text': json.dumps({'line': ''})})
    print(_groups)

@channel_session_user
def ws_disconnect(message):
    print('disconnect')
    log_id = message.reply_channel.name.split('.')[-1]
    log_id = log_id.replace('!', '1')
    Group('logs'+log_id).send({
        'text': json.dumps({
            #'line': '',
            'is_logged_in': False
        })
    })

    Group('logs'+log_id).discard(message.reply_channel)

    #stop_thread(tailThread)
    _groups.remove(log_id)
