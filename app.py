from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, threading

app = Flask(__name__)
CORS(app)

FILE = "data.json"
lock = threading.Lock()

def load():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

@app.get("/weights/<note_id>")
def get_weights(note_id):
    data = load()
    return jsonify(data.get(note_id, [0,0,0,0,0]))

@app.post("/weights")
def set_weights():
    payload = request.get_json(silent=True)

    # 🔁 Fallback for sendBeacon (text/plain)
    if payload is None:
        try:
            payload = json.loads(request.data.decode("utf-8"))
        except Exception:
            return {"error": "Invalid payload"}, 400

    note_id = str(payload["noteId"])
    weights = payload["weights"]

    with lock:
        data = load()
        data[note_id] = weights
        save(data)

    return {"ok": True}


@app.get("/debug/all")
def debug_all():
    return load()
