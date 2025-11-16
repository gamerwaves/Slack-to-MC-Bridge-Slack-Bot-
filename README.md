# Slack to MC Bridge (Slack Bot)

## What this is

This Slack to MC bridge takes slack messages sent in a channel and sends it to minecraft like this: 

`[Slack] <DISPLAY NAME> Message`

## How to use this

Clone this repo, and then create a slack bot using this manifest:
```manifest.json
{
    "display_information": {
        "name": "Slack to MC Bridge"
    },
    "features": {
        "bot_user": {
            "display_name": "Slack to MC Bridge",
            "always_online": false
        }
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "channels:history",
                "channels:join",
                "users:read"
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "bot_events": [
                "message.channels"
            ]
        },
        "interactivity": {
            "is_enabled": true
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": true,
        "token_rotation_enabled": false
    }
}
```

Then, copy .env.example to .env and fill in the information based on your slack bot.
Finally, run main.py.