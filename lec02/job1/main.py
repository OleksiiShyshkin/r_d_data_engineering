from flask import Flask, request, jsonify
from .bll.sales_api import save_sales_to_local_disk

app = Flask(__name__)

@app.route("/sales", methods=["POST"])
def run_job():
    payload = request.get_json(force=True)
    report_date = payload.get("report_date")
    raw_dir = payload.get("raw_dir")

    if not report_date or not raw_dir:
        return jsonify({"error": "report_date і raw_dir обов’язкові"}), 400

    stats = save_sales_to_local_disk(report_date, raw_dir)
    return jsonify({"status": "ok", **stats}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
