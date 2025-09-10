import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

print("\n=== Criar Pagamento Pix ===")
r = requests.post(f"{BASE_URL}/payments/pix", json={"value": 150.0})
print(r.status_code, r.text)

# Se a criação deu certo, pega o ID do pagamento retornado
if r.status_code == 201:
    response_json = r.json()
    payment_id = response_json["payment"]["id"]
    print(f"✅ Pagamento criado com ID: {payment_id}")
else:
    payment_id = None

print("\n=== Consultar Pagamento Pix por ID ===")
if payment_id:
    r = requests.get(f"{BASE_URL}/payments/pix/{payment_id}")
    print(r.status_code, r.text)
else:
    print("❌ Nenhum pagamento criado para consultar")

print("\n=== Confirmar Pagamento Pix ===")
r = requests.post(f"{BASE_URL}/payments/pix/confirmation", json={"payment_id": payment_id})
print(r.status_code, r.text)
