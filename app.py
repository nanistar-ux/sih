import os, json, logging
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

PORT = 5001
API_KEY = "YOUR_SECRET_KEY_HERE"

ALLOWED = {
    ("Ramesh","Arepally"), ("Lakshmi","Arepally"), ("Sita","Arepally"),
    ("Arjun","Damera"), ("Bheema","Damera"), ("Sundari","Damera"),
    ("Raju","Oglapur"), ("Kavya","Oglapur"), ("Lalitha","Oglapur"),
    ("Bheema Rao","Oorugonda"), ("Sita Bai","Oorugonda"), ("Ramesh Koya","Oorugonda")
}

DATA_PATH = os.path.join("data", "claims.json")
os.makedirs("data", exist_ok=True)

app = Flask(__name__, template_folder="templates")
CORS(app)
logging.basicConfig(level=logging.INFO)

@app.route("/")
def index():
    return render_template("map.html")

@app.route("/api/claims", methods=["POST"])
def receive_claims():
    key = request.headers.get("x-api-key")
    if key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    if not data: return jsonify({"error": "No JSON"}), 400

    if isinstance(data, dict): data = [data]

    cleaned = []
    for item in data:
        name = item.get("person_name")
        village = item.get("village")
        coords = item.get("coordinates") or {}
        lat = coords.get("lat")
        lng = coords.get("lng")
        area = item.get("area_ha")
        doc = item.get("doc_url", "")
        status = item.get("status", "pending")
        state = item.get("state", "Telangana")

        if (name, village) not in ALLOWED:
            continue
        if lat is None or lng is None: continue

        cleaned.append({
            "person_name": name,
            "village": village,
            "state": state,
            "lat": float(lat),
            "lng": float(lng),
            "area_ha": float(area) if area else None,
            "status": status,
            "doc_url": doc
        })

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned, f, ensure_ascii=False, indent=2)

    logging.info(f"Saved {len(cleaned)} claims")
    return jsonify({"status": "ok", "saved": len(cleaned)}), 200

@app.route("/api/claims", methods=["GET"])
def get_claims():
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    return jsonify([])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=False)
