from flask import Flask, jsonify
import routeros_api

app = Flask(__name__)

ROUTER_IP = "192.168.15.2"
USER = "admin"
PASSWORD = "senha"

def conectar():
    connection = routeros_api.RouterOsApiPool(
        ROUTER_IP,
        username=USER,
        password=PASSWORD,
        port=8728,
        plaintext_login=True
    )
    return connection.get_api()

@app.route("/usuarios")
def usuarios():
    api = conectar()
    hosts = api.get_resource('/ip/hotspot/host')
    dados = hosts.get()
    return jsonify(dados)

@app.route("/interfaces")
def interfaces():
    api = conectar()
    interfaces = api.get_resource('/interface')
    dados = interfaces.get()
    return jsonify(dados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)