from flask import Flask, request
import sys
import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{now}] Recebida requisição de {request.remote_addr}"
    print(log_message, file=sys.stderr)
    return f"Olá do Servidor! Hora: {now}\n"

if __name__ == '__main__':
    print("Servidor iniciando na porta 8080...", file=sys.stderr)
    app.run(host='0.0.0.0', port=8080)
