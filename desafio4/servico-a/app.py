from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/users")
def users():
    return jsonify([
        {"id": 1, "name": "Ana"},
        {"id": 2, "name": "Bruno"}
    ])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
