import threading

def sayhello():
    print "hello world"
    global t #Notice: use global variable!

t = threading.Thread(target=sayhello)
t.start()
