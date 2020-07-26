from urllib.parse import quote, unquote
import requests as req
from conf import apiKey
api = apiKey

def serv(page, *datas):
    data1 = ""
    for data in datas:
        data1 += data + "&"

    resp = req.get(f"https://api.telegram.org/bot{api}/"+page+"?"+data1)

    if resp.status_code == 200:
        return resp.json()
    return 0


def tfreshStart():
    while 1:
        msg = serv('getupdates')
        if msg['result'] == []:
            break
        serv('getupdates', "offset="+str(msg['result'][0]['update_id']+1))
    return 1


def clearBuffer(msg):
    serv('getupdates', "offset="+str(msg['result'][0]['update_id']+1))


def trecv():
    try:
        while 1:
            msg = serv("getupdates", "timeout=999999999")
            if msg['result'] != []:
                clearBuffer(msg)
                break
        return msg['result'][0]['message']['from']['id'], msg['result'][0]['message']['text'].lower()
    except:
        return False
    
def tsend(id, text):
    text = quote(text)
    return serv('sendmessage', "chat_id="+str(id), "text="+text)

def main():
    # tfreshStart()
    # id, msg = trecv()
    # tsend(id, msg)
    pass


if __name__ == "__main__":
    import os
    os.system('clear')
    main()

