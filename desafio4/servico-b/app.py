from flask import Flask, jsonify
import requests

app = Flask(__name__)


@app.route("/info")
def info():
    response = requests.get("http://servico-a:5001/users", timeout=5)
    data = response.json()
    processed = [{"msg": f"Usuário {user['name']} ativo."} for user in data]
    return jsonify(processed)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
