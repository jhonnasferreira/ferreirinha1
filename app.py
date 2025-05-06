from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações Z-API
ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
INSTANCE_ID = os.getenv("ZAPI_INSTANCE_ID")
WEBHOOK_TOKEN = os.getenv("WEBHOOK_TOKEN")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        # Verifica autenticação
        if request.headers.get("Authorization") != WEBHOOK_TOKEN:
            return jsonify({"error": "Não autorizado"}), 401

        data = request.json
        phone = data.get("phone")
        message = data.get("message", "").lower()

        # Lógica de resposta
        if any(palavra in message for palavra in ["ola", "oi", "olá"]):
            resposta = "Olá! Sou o Ferreirinha 🤖 Como posso te ajudar?"
        elif "reservar" in message:
            resposta = "Para reservas, me informe:\n1. Nome completo\n2. Data de entrada (DD/MM)\n3. Número de hóspedes"
        else:
            resposta = "Não entendi. Digite *ajuda* para ver opções."

        # Envia resposta via Z-API
        enviar_mensagem_zapi(phone, resposta)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        print(f"ERRO: {str(e)}")
        return jsonify({"error": "Erro interno"}), 500

def enviar_mensagem_zapi(destinatario, mensagem):
    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    headers = {"Content-Type": "application/json"}
    payload = {
        "phone": destinatario,
        "message": mensagem
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()

@app.route("/", methods=["GET"])
def health_check():
    return "Ferreirinha online! Use /webhook para o Z-API"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
