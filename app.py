from flask import Flask, render_template, request, jsonify
import requests
import hashlib
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # default to 5000 for local dev
    app.run(host="0.0.0.0", port=port, debug=True)


app = Flask(__name__)

def check_pwned(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    res = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
    hashes = (line.split(':') for line in res.text.splitlines())
    return any(s == suffix for s, _ in hashes)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check_password", methods=["POST"])
def check_password():
    data = request.json
    password = data.get("password", "")
    pwned = check_pwned(password)
    return jsonify({"pwned": pwned})

if __name__ == "__main__":
    app.run(debug=True)
