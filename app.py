from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")  # Update for Atlas if needed
db = client["webhookDB"]
collection = db["events"]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid data"}), 400

    event_type = data.get("event")
    author = data.get("author")
    from_branch = data.get("from_branch")
    to_branch = data.get("to_branch")
    timestamp = data.get("timestamp")

    try:
        dt = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
        readable_timestamp = dt.strftime("%d %B %Y - %I:%M %p UTC")
    except:
        readable_timestamp = timestamp

    entry = {
        "event": event_type,
        "author": author,
        "from_branch": from_branch,
        "to_branch": to_branch,
        "timestamp": readable_timestamp
    }

    collection.insert_one(entry)
    return jsonify({"status": "received"}), 200

@app.route('/events')
def events():
    recent = list(collection.find().sort("_id", -1).limit(10))
    for item in recent:
        item["_id"] = str(item["_id"])
    return jsonify(recent)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
