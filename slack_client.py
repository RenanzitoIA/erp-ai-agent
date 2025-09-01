import os, requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

def post_message(text: str):
    if not SLACK_BOT_TOKEN or not SLACK_CHANNEL_ID:
        return {"ok": False, "error": "Slack not configured"}
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_BOT_TOKEN}", "Content-type": "application/json; charset=utf-8"}
    payload = {"channel": SLACK_CHANNEL_ID, "text": text}
    r = requests.post(url, headers=headers, json=payload, timeout=30)
    try:
        return r.json()
    except Exception:
        return {"ok": False, "status": r.status_code, "text": r.text}
