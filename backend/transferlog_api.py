
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).resolve().parent
RAW_DIR = BASE_DIR / "raw_data"
RAW_DIR.mkdir(parents=True, exist_ok=True)
IMU_FILE = RAW_DIR / "imu_latest.json"

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok", raw_dir=str(RAW_DIR))

@app.route("/api/imu", methods=["POST"])
def imu_post():
    payload = request.get_json(silent=True) or {}
    for k in ["ax","ay","az","gx","gy","gz"]:
        payload.setdefault(k, 0.0)
    payload["ts"] = datetime.utcnow().isoformat() + "Z"
    with open(IMU_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    return jsonify(status="saved", file=str(IMU_FILE), data=payload)

@app.route("/api/imu", methods=["GET"])
def imu_get():
    if IMU_FILE.exists():
        with open(IMU_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"ax":0,"ay":0,"az":9.8,"gx":0,"gy":0,"gz":0,"ts":datetime.utcnow().isoformat()+"Z"}
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
