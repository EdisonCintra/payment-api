import os

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/payments/pix", methods=['POST'])
def create_payments_pix():
    return jsonify({'message': 'Pix payment created'}), 201

@app.route("/payments/pix/confirmation", methods=['POST'])
def pix_confirmation():
    return jsonify({'message': 'Pix payment confirmed'}), 201

#webhook
@app.route('/payments/pix/<int:payment_id>', methods=['GET']) 
def payments_pix_page(payment_id):
    return 'payment pix'

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)