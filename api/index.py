from flask import Flask, request, jsonify
import time

app = Flask(__name__)

@app.route("/meetings.create", methods=["POST"])
def create_meeting():
    data = request.get_json() or {}
    title = data.get("title", "未命名会议")
    meeting_id = f"MTG-{int(time.time())}"
    print(f"[INFO] Create meeting: {title} ({meeting_id})")
    return jsonify({"id": meeting_id, "success": True, "title": title})

@app.route("/meetings.query", methods=["GET"])
def query_meetings():
    sample = [
        {"id": "MTG-1", "title": "东汽焊接工艺片相关需求沟通会"},
        {"id": "MTG-2", "title": "澳洲项目设备方案讨论"}
    ]
    return jsonify({"success": True, "meetings": sample})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "service": "Notion Meeting Agent",
        "version": "1.4.5",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == "__main__":
    app.run(debug=True)
