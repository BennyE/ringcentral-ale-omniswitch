#!/usr/bin/env python3

#
# Imports
#
import sys
import json
try:
    import requests
except ImportError as ie:
    print(ie)
    # python3 -m pip install requests
    sys.exit("Please install python-requests!")
import socket
import subprocess
from ringcentral_webhook_secrets import secrets

webhook_url = secrets["webhook_url"]

webhook_header = {
    "Content-Type": "application/json"
}

def collect_omniswitch_details():
    system_info = {
        "description": "",
        "uptime": "",
        "contact": "",
        "name": "",
        "location": "",
        "date_time": "",
        "fqdn": "",
        "ip": ""
    }
    show_system = subprocess.run(["show", "system"], capture_output=True)
    show_system_output = show_system.stdout.decode("utf-8").split("\n")
    for output in show_system_output:
        if "Description:" in output:
            system_info["description"] = f"{'Unknown' if output.split('Description:')[1].strip().rstrip(',') == '' else output.split('Description:')[1].strip().rstrip(',')}"
        elif "Up Time:" in output:
            system_info["uptime"] = f"{'Unknown' if output.split('Up Time:')[1].strip().rstrip(',') == '' else output.split('Up Time:')[1].strip().rstrip(',')}"
        elif "Contact:" in output:
            system_info["contact"] = f"{'Unknown' if output.split('Contact:')[1].strip().rstrip(',') == '' else output.split('Contact:')[1].strip().rstrip(',')}"
        elif "Name:" in output:
            system_info["name"] = f"{'Unknown' if output.split('Name:')[1].strip().rstrip(',') == '' else output.split('Name:')[1].strip().rstrip(',')}"
        elif "Location:" in output:
            system_info["location"] = f"{'Unknown' if output.split('Location:')[1].strip().rstrip(',') == '' else output.split('Location:')[1].strip().rstrip(',')}"
        elif "Date & Time:" in output:
            system_info["date_time"] = f"{'Unknown' if output.split('Date & Time:')[1].strip().rstrip(',') == '' else output.split('Date & Time:')[1].strip().rstrip(',')}"
        else:
            continue
    system_info["fqdn"] = f"{socket.getfqdn() if (socket.getfqdn() != socket.gethostname()) else socket.gethostbyname(socket.gethostname())}"
    system_info["ip"] = socket.gethostbyname(socket.gethostname())
    return system_info    

def send_post(message):
    webhook_msg = {
        "body": message
    }
    #Fix: "Invalid Custom payload: no supported fields" text -> body in json payload
    webhook_resp = requests.post(webhook_url, headers=webhook_header, json=webhook_msg)

    if webhook_resp.status_code == 200 or webhook_resp.status_code == 201:
       print(webhook_resp.status_code, webhook_resp.reason, "- Webhook/App/Post")
       print(json.dumps(webhook_resp.json(), indent=4))
    else:
       sys.exit(f"Sending Post failed! Error code: {webhook_resp.status_code, webhook_resp.reason, webhook_resp.json()}")

def send_notification_card(message):
    system_info = collect_omniswitch_details()
    card_msg = {
        "activity": "Alcatel-Lucent Enterprise",
        "attachments": [
            {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "fallbackText": f"{system_info['name'] + ':' + message}",
                "version": "1.0",
                "body": [
                {
                    "type": "TextBlock",
                    "text": f"Digital Age Network Notification for {system_info['name']}",
                    "weight": "bolder",
                    "size": "medium",
                    "wrap": True
                },
                {
                    "type": "ColumnSet",
                    "columns": [
                    {
                        "type": "Column",
                        "width": "auto",
                        "items": [
                        {
                            "type": "Image",
                            "url": "https://bennye.github.io/logos/omniswitch.png",
                            "size": "small",
                            "style": "person"
                        }
                        ]
                    },
                    {
                        "type": "Column",
                        "width": "stretch",
                        "items": [
                        {
                            "type": "TextBlock",
                            "text": f"WebView: [{system_info['fqdn']}](https://{system_info['fqdn']})",
                            "weight": "bolder",
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "spacing": "none",
                            "text": f"Date/Time: {system_info['date_time']}",
                            "isSubtle": True,
                            "wrap": True
                        },
                        {
                            "type": "TextBlock",
                            "spacing": "none",
                            "text": f"Notification: {message}",
                            "wrap": True
                        }
                        ]
                    }
                    ]
                },
                {
                    "type": "FactSet",
                    "facts": [
                    {
                        "title": "System Description:",
                        "value": f"{system_info['description']}"
                    },
                    {
                        "title": "System Uptime:",
                        "value": f"{system_info['uptime']}"
                    },
                    {
                        "title": "System Contact:",
                        "value": f"{system_info['contact']}"
                    },
                    {
                        "title": "System Location:",
                        "value": f"{system_info['location']}"
                    }
                    ]
                }
                ]
            }
        ]
    }

    webhook_card_resp = requests.post(webhook_url, headers=webhook_header, json=card_msg)

    if webhook_card_resp.status_code == 200 or webhook_card_resp.status_code == 201:
        print(webhook_card_resp.status_code, webhook_card_resp.reason, "- Webhook/App/Post/Card")
        print(json.dumps(webhook_card_resp.json(), indent=4))
    else:
        sys.exit(f"Sending Post/Card failed! Error code: {webhook_card_resp.status_code, webhook_card_resp.reason, webhook_card_resp.json()}")

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) > 1:
        if sys.argv[1] == "send_post":
            send_post(sys.argv[2])
        elif sys.argv[1] == "send_notification_card":
            send_notification_card(sys.argv[2])
        else:
            sys.exit("Unsupported action specified, only send_post & send_card supported!")
    else:
        sys.exit("Not enough arguments specified")