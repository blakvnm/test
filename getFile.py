import teleApi as tg
from s import send, recv
import os

def reciveFile(client, fnm):
    # try:
    #     msg = recv(client)
    #     fsize = int(msg)
    #     with open(os.getcwd()+'/'+fnm, 'wb') as file:
    #         file.write(client.recv(fsize), fsize))
    #     return True
    # except Exception as e:
    #     print(e)
    pass
        # return False

def main(client, id, fnm):
    msg = recv(client)
    if  msg == '-1':
        tg.tsend(id, 'Invalid File Path')
        return
    
    tg.tsend(id, msg)
    tg.tsend(id, 'Do you want to continue')
    id, msg = tg.trecv()
    send(client, msg)

    # if 'y' in msg.lower():
    #     if reciveFile(client, fnm):
    #         tg.tsend(id, 'File is recived to the cloud')
    #     else:
    #         tg.tsend(id, 'Failed While reciving file')

    # else:
    #     return


