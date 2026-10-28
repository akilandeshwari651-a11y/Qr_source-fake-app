import os
from flask import Flask, request, jsonify, send_from_directory
from checker import analyze

BASE = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
history = []
reported = set()


@app.route("/")
def home():
    return send_from_directory(BASE, "index.html")


@app.route("/check", methods=["POST"])
def check():
    link = (request.get_json(silent=True) or {}).get("url", "")
    if not link.strip():
        return jsonify(error="No link received"), 400
    result = analyze(link, reported=(analyze(link)["url"] in reported))
    history.append({"url": result["url"], "score": result["score"], "verdict": result["verdict"]})
    return jsonify(result)


@app.route("/report", methods=["POST"])
def report():
    link = (request.get_json(silent=True) or {}).get("url", "")
    if link.strip():
        reported.add(analyze(link)["url"])
    return jsonify(ok=True)


@app.route("/history")
def get_history():
    return jsonify(history[-10:][::-1])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
