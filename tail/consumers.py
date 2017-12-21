# coding: utf-8
import os
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

    # Multi logs
    popens = {}
    LOGTAIL_FILES = getattr(settings, 'LOGTAIL_FILES', [])
    for log in LOGTAIL_FILES:
        tail_cmd = 'tail -f {0}'.format(log)
        tail_popen = subprocess.Popen(tail_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        popens[log] = tail_popen
    # Add message channel
    Group('logs'+log_id).add(message.reply_channel)

    # pre read
    pre_read(log_id, popens, 10)

    # Thread target
    # 采用工厂函数方式，如果没有make_tail，将会导致
    # 所有的多线程都采用for最后loop的结果。
    targets = {}
    for log in popens:
        def make_tail(log):
            def tail():
                while True:
                    line = popens[log].stdout.readline()
                    log_name = log.rsplit('/', 1)[-1].split('.')[0]
                    #print(log_name)
                    for log_id in _groups:
                        Group('logs'+log_id).send({
                        'text': json.dumps({log_name: line.decode('utf-8')})
                    })
            return tail
        targets[log] = make_tail(log)
    global tailThread
    print(targets)
    
    if _threads == []:
        print('create thread')
        for log in popens:
            tailThread = threading.Thread(name='log_tail', target=targets[log])
            tailThread.start()
            _threads.append(tailThread)
    else:
        text_json = {}
        for log in popens:
            log_name = log.rsplit('/', 1)[-1].split('.')[0]
            text_json[log_name] = ''
        Group('logs'+log_id).send({'text': json.dumps(text_json)})
    print(_groups)
    print(_threads)

@channel_session_user
def ws_disconnect(message):
    print('disconnect')
    log_id = message.reply_channel.name.split('.')[-1]
    log_id = log_id.replace('!', '1')
    Group('logs'+log_id).send({
        'text': json.dumps({
            'is_logged_in': False
        })
    })

    Group('logs'+log_id).discard(message.reply_channel)

    #stop_thread(tailThread)
    _groups.remove(log_id)

# 预读日志文件，默认tail预读10行，
# count 可以指定预读行数，少于count
# 则预读所有
def pre_read(log_id, popens, count):
    for log in popens:
        try:
            log_len = file_len(log)
        except IOError:
            continue
        if log_len < count:
            count = log_len
        for i in range(0, count):
            line = popens[log].stdout.readline()
            log_name = log.rsplit('/', 1)[-1].split('.')[0]
            # Send pre-reading
            Group('logs'+log_id).send({
                'text': json.dumps({log_name: line.decode('utf-8')})
        })


# count file lines using buf count
# 性能上是 wc -l 的一半
def file_len(fname):
    f = open(fname)                  
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.read # loop optimization

    buf = read_f(buf_size)
    while buf:
        lines += buf.count('\n')
        buf = read_f(buf_size)

    return lines
