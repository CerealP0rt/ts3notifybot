import requests, argparse, ts3


class telegramBot(object):

    TELEGRAM_BASE_URL = 'https://api.telegram.org/bot'

    def __init__(self, token, chats):
        self._token = token
        self._url = self.TELEGRAM_BASE_URL + self._token
        try:
            r = requests.get(self._url + '/getMe')
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(err)
        else:
            data = r.json()
            self._id = data['result']['id']
            self._username = data['result']['username']
            self._name = data['result']['first_name']
        self._chats = set(chats)


    def sendMessage(self, chat_id, message):
        url = self._url + "/sendMessage"
        try:
            r = requests.post(url, json={"chat_id":chat_id,"text": message})
            r.raise_for_status()
        except requests.exceptions.RequestException as err:
            print(err)
        else:
            print("Message sent to chat_id %s" % chat_id)


    def sendMessageAll(self, message):
        for chat in self._chats:
            self.sendMessage(chat, message)


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Send TS3 online Notifications')
    parser.add_argument('--host', default='localhost', help='TS3 Query Host Address')
    parser.add_argument('--port', default=10011, help='TS3 Query Port')
    parser.add_argument('--sid', default=1, help='TS3 Virtual Server ID')
    parser.add_argument('--user', default='serveradmin', help='Username')
    parser.add_argument('--pw', required=True, help='Password')
    parser.add_argument('--bot', required=True, metavar='TOKEN', help='Telegram Bot Token')
    parser.add_argument('--chat', nargs='+', required=True, metavar='CHAT_ID', help='Telegram chat_id')
    parser.add_argument('--tsuser', nargs='+', metavar='TS_UID', help='TS3 User ID to notify about')

    args = parser.parse_args()

    # init telegram bot
    tbot = telegramBot(token=args.bot, chats=args.chat)
    print("Bot Name: %s" % tbot._name)
    print("Bot ID: %s" % tbot._id)

    try:
        with ts3.query.TS3Connection(args.host, args.port) as ts3conn:
            print('connecting')
            try:
                ts3conn.login(client_login_name=args.user, client_login_password=args.pw)
                ts3conn.use(sid=args.sid)
                ts3conn.servernotifyregister(event="server")
            except:
                print("login failed")
            else:
                print("start event monitoring")
                clid = {}
                while True:
                    ts3conn.send_keepalive()
                    try:
                        event = ts3conn.wait_for_event(timeout=550)
                    except ts3.query.TS3TimeoutError:
                        pass
                    else:
                        if event[0]["reasonid"] == "0" and event[0]['client_unique_identifier'] in args.tsuser:
                            clid[event[0]['clid']] = event[0]['client_nickname']
                            tbot.sendMessageAll("%s online" % event[0]['client_nickname'])
                        elif event[0]["reasonid"] == "8" and event[0]['clid'] in clid.keys():
                            tbot.sendMessageAll("%s %s" % (clid[event[0]['clid']], event[0]["reasonmsg"]))
                            del clid[event[0]['clid']]
                        elif event[0]["reasonid"] == "3" and event[0]['clid'] in clid.keys():
                            tbot.sendMessageAll("%s %s" % (clid[event[0]['clid']], event[0]["reasonmsg"]))
                            del clid[event[0]['clid']]

    except ConnectionRefusedError:
        print('TS connection failed')
