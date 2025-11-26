from flask import Flask, request, jsonify
from .bll.convert_to_avro import save_avro_from_json

app = Flask(__name__)

@app.route("/stg", methods=["POST"])
def run_job2():
    payload = request.get_json(force=True)
    raw_dir = payload.get("raw_dir")
    stg_dir = payload.get("stg_dir")

    if not raw_dir or not stg_dir:
        return jsonify({"error": "raw_dir are stg_dir are required"}), 400

    try:
        res = save_avro_from_json(raw_dir=raw_dir, stg_dir=stg_dir)
        return jsonify({"status": "ok", **res}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8082)