
# -*- coding: utf-8 -*-
# Vercel Serverless (Python) — Notion Meeting Agent Webhook
# Endpoints:
#   - GET  /                 : health check
#   - POST /meetings.create  : create a meeting note page in Notion DB
#   - POST /meetings.query   : query meeting notes by status (optional)
#
# Environment variables required on Vercel:
#   - NOTION_TOKEN : your Notion internal integration token (secret_... or ntn_...)
#   - DATABASE_ID  : Notion database id (e.g., 29dd6934-6604-813e-9960-fbad9839145a)
#   - API_KEY      : a string you choose; requests must send Authorization: Bearer <API_KEY>
# Optional:
#   - NOTION_VERSION : default '2022-06-28'

import os
import json
from flask import Flask, request, jsonify, abort
import requests

app = Flask(__name__)

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "").strip()
DATABASE_ID = os.environ.get("DATABASE_ID", "").strip()
API_KEY = os.environ.get("API_KEY", "").strip()
NOTION_VERSION = os.environ.get("NOTION_VERSION", "2022-06-28")
BASE_URL = "https://api.notion.com/v1"

def notion_headers():
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

@app.before_request
def check_ready_and_auth():
    # Health path can be open
    if request.path == "/":
        return
    # basic readiness checks
    if not NOTION_TOKEN or not DATABASE_ID:
        abort(500, description="Server not configured: missing NOTION_TOKEN or DATABASE_ID")
    # API key auth (required)
    auth = request.headers.get("Authorization", "")
    if not API_KEY or auth != f"Bearer {API_KEY}":
        abort(401, description="Unauthorized: missing or invalid Authorization header")

@app.get("/")
def home():
    return jsonify({"status": "OK", "service": "Notion Meeting Agent", "routes": ["/meetings.create", "/meetings.query"]})

@app.post("/meetings.create")
def create_meeting():
    data = request.get_json(force=True, silent=True) or {}
    # required fields
    title = data.get("title")
    date = data.get("date")
    start = data.get("start")
    end = data.get("end")
    attendees = data.get("attendees", [])
    mtype = data.get("meeting_type", "沟通会")
    content = data.get("content", "")
    decisions = data.get("decisions", "")
    todos = data.get("todos", "")
    status = data.get("status", "草稿")

    if not all([title, date, start, end]):
        return jsonify({"success": False, "error": "Missing required fields: title,date,start,end"}), 400

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "会议主题": {"title": [{"text": {"content": title}}]},
            "会议日期": {"date": {"start": date}},
            "开始时间": {"rich_text": [{"text": {"content": start}}]},
            "结束时间": {"rich_text": [{"text": {"content": end}}]},
            "参会人员": {"multi_select": [{"name": str(n).strip()} for n in attendees if str(n).strip()]},
            "会议类型": {"select": {"name": mtype}},
            "核心议题与讨论内容": {"rich_text": [{"text": {"content": content}}]},
            "关键结论与决策": {"rich_text": [{"text": {"content": decisions}}]},
            "待办事项": {"rich_text": [{"text": {"content": todos}}]},
            "状态": {"select": {"name": status}}
        }
    }
    r = requests.post(f"{BASE_URL}/pages", headers=notion_headers(), data=json.dumps(payload))
    if r.status_code >= 300:
        return jsonify({"success": False, "error": r.text}), 400
    page = r.json()
    return jsonify({"success": True, "id": page.get("id"), "title": title})

@app.post("/meetings.query")
def query_meetings():
    data = request.get_json(force=True, silent=True) or {}
    status = data.get("status")
    query = {"page_size": 10}
    if status:
        query["filter"] = {"property": "状态", "select": {"equals": status}}
    r = requests.post(f"{BASE_URL}/databases/{DATABASE_ID}/query", headers=notion_headers(), data=json.dumps(query))
    if r.status_code >= 300:
        return jsonify({"success": False, "error": r.text}), 400
    items = []
    for res in r.json().get("results", []):
        props = res.get("properties", {})
        title = ""
        if props.get("会议主题", {}).get("title"):
            title = props["会议主题"]["title"][0].get("plain_text", "")
        date = props.get("会议日期", {}).get("date", {}).get("start", "")
        st = props.get("状态", {}).get("select", {}).get("name", "")
        items.append({"id": res.get("id"), "title": title, "date": date, "status": st})
    return jsonify({"success": True, "results": items})
