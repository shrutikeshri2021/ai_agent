from flask import Flask, request, jsonify
from agent.graph import run_agent
from flask import send_file
import os
import database

app = Flask(__name__)
database.init_db()

@app.route("/")
def home():
    return {"status": "Backend running"}

@app.route("/run", methods=["POST"])
def run_test():
    user_input = request.json.get("instruction")
    report = run_agent(user_input)
    database.add_test_run(user_input, report)
    return jsonify(report)

@app.route("/history", methods=["GET", "DELETE"])
def handle_history():
    if request.method == "DELETE":
        database.clear_history()
        return {"status": "History cleared"}
    return jsonify(database.get_all_test_runs())

# Fix: BASE_DIR should point to 'backend' folder where 'reports' is located
# Use logging to debug path issues
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")
print(f"DEBUG: App BASE_DIR: {BASE_DIR}")
print(f"DEBUG: Reports expected at: {REPORTS_DIR}")

@app.route("/download/pdf")
def download_pdf():
    pdf_path = os.path.join(REPORTS_DIR, "test_report.pdf")
    if not os.path.exists(pdf_path):
        return {"error": f"File not found at {pdf_path}"}, 404
    return send_file(pdf_path, as_attachment=True)

@app.route("/download/json")
def download_json():
    json_path = os.path.join(REPORTS_DIR, "test_report.json")
    if not os.path.exists(json_path):
        return {"error": f"File not found at {json_path}"}, 404
    return send_file(json_path, as_attachment=True)

@app.route("/screenshots/<filename>")
def serve_screenshot(filename):
    # Security: Ensure filename is safe (basic check)
    if ".." in filename or filename.startswith("/"):
         return {"error": "Invalid filename"}, 400
         
    path = os.path.join(REPORTS_DIR, "screenshots", filename)
    if os.path.exists(path):
        return send_file(path)
    return {"error": "File not found"}, 404

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True)


