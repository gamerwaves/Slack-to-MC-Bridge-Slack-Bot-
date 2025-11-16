from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os
from dotenv import load_dotenv
import requests 

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

TARGET_CHANNEL = "C029E8FARRC"

WEBHOOK_URL = os.getenv("WEBHOOK_URL")

app = App(token=SLACK_BOT_TOKEN)

def get_display_name(client, uid):
    try:
        info = client.users_info(user=uid)
        profile = info.get("user", {}).get("profile", {})
        return profile.get("display_name") or profile.get("real_name") or uid
    except Exception:
        return uid

@app.event("message")
def handle_message_events(body, client):
    event = body.get("event", {})
    channel = event.get("channel")

    if event.get("subtype") is not None:
        return

    if channel == TARGET_CHANNEL:
        text = event.get("text")
        user = event.get("user")
        display_name=get_display_name(client, user)
        ts = event.get("ts")

        payload = {
            "user": display_name,
            "text": text,
            "timestamp": ts,
            "channel": channel
        }

        try:
            r = requests.post(WEBHOOK_URL, json=payload, timeout=3)
            print("Webhook sent:", r.status_code)
        except Exception as e:
            print("Failed to send webhook:", e)

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
