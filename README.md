# ts3notifybot
TS3 notification bot for telegram

## Get Telegram Bot Token
https://core.telegram.org/bots#3-how-do-i-create-a-bot

## Get Telegram Chat IDs
```
curl -s https://api.telegram.org/bot<TOKEN>/getUpdates | jq '[.result[].message.chat.id]' | jq 'unique'
```

## RUN
```
usage: run.py [-h] [--host HOST] [--port PORT] [--sid SID] [--user USER] --pw
              PW --bot TOKEN --chat CHAT_ID [CHAT_ID ...]
              [--tsuser TS_UID [TS_UID ...]]

Send TS3 online Notifications

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           TS3 Query Host Address
  --port PORT           TS3 Query Port
  --sid SID             TS3 Virtual Server ID
  --user USER           Username
  --pw PW               Password
  --bot TOKEN           Telegram Bot Token
  --chat CHAT_ID [CHAT_ID ...]
                        Telegram chat_id
  --tsuser TS_UID [TS_UID ...]
                        TS3 User ID to notify about

```