from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Configurações - preencha no Render.com
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("Authorization") != WEBHOOK_TOKEN:
        return jsonify({"error": "Não autorizado"}), 401
    
    data = request.json
    phone = data["phone"]
    message = data.get("message", "").lower()
    
    if "oi" in message or "olá" in message:
        resposta = "Olá! Ferreirinha respondendo ✅"
    else:
        resposta = "Digite 'ajuda' para opções"
    
    requests.post(
        f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text",
        json={"phone": phone, "message": resposta},
        headers={"Content-Type": "application/json"}
    )
    return jsonify({"status": "success"}), 200

@app.route("/", methods=["GET"])
def health_check():
    return "Ferreirinha Online ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Alterado para 10000
    app.run(host="0.0.0.0", port=port)  # Bind explícito
