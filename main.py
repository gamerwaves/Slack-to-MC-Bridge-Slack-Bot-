from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
import requests 

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

TARGET_CHANNEL = "C09T2TZ5P0T"
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = App(token=SLACK_BOT_TOKEN)

def get_display_name(client, uid):
    try:
        info = client.users_info(user=uid)
        profile = info.get("user", {}).get("profile", {})
        return profile.get("display_name") or profile.get("real_name") or uid
    except Exception:
        return uid

def get_parent_message(client, channel, thread_ts):
    try:
        resp = client.conversations_replies(channel=channel, ts=thread_ts, limit=1)
        messages = resp.get("messages", [])
        if len(messages) > 0:
            return messages[0].get("text", "")
    except Exception as e:
        print("Failed to fetch parent message:", e)
    return ""

def get_parent_user(client, channel, thread_ts):
    try:
        resp = client.conversations_replies(channel=channel, ts=thread_ts, limit=1)
        messages = resp.get("messages", [])
        if len(messages) > 0:
            return messages[0].get("user", "")
    except Exception as e:
        print("Failed to fetch parent user:", e)
    return ""

@app.event("message")
def handle_message_events(body, client):
    event = body.get("event", {})
    channel = event.get("channel")

    if event.get("subtype") is not None:
        return

    if channel != TARGET_CHANNEL:
        return

    text = event.get("text", "")
    user = event.get("user", "")
    display_name = get_display_name(client, user)
    ts = event.get("ts", "")
    thread_ts = event.get("thread_ts", "")

    if thread_ts and thread_ts != ts:
        message_type = "thread_reply"
        parent_text = get_parent_message(client, channel, thread_ts)
        parent_user_id = get_parent_user(client, channel, thread_ts)
        parent_user = get_display_name(client, parent_user_id) if parent_user_id else ""
    else:
        message_type = "channel_message"
        parent_text = ""
        parent_user = ""

    payload = {
        "user": display_name,
        "text": text,
        "timestamp": ts,
        "channel": channel,
        "type": message_type,
        "parent_text": parent_text,
        "parent_user": parent_user
    }

    if message_type == "thread_reply":
        payload["parent_ts"] = thread_ts

    print("Prepared payload:", payload)

    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=3)
        print("Webhook sent:", r.status_code)
    except Exception as e:
        print("Failed to send webhook:", e)

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
