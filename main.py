import os
from repository.database import db 
from flask import Flask, jsonify, request, send_file, render_template
from db_models.payment import Payment
from datetime import datetime, timedelta
from payments.pix import Pix
from flask_socketio import SocketIO

#BASE_DIR = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'SECRET_KEY_WEBSOCKET'

socketio = SocketIO(app)
db.init_app(app)


@app.route("/payments/pix", methods=['POST'])
def create_payments_pix():
    data = request.get_json()
    if 'value' not in data:
        jsonify({'message':'Invalid value'}),400
    expiration_date = datetime.now() + timedelta(minutes=30)

    new_payment = Payment(value=data['value'], expiration_date=expiration_date)
    pix_obj = Pix()
    data_payment_pix = pix_obj.create_payment()
    new_payment.bank_payment_id = data_payment_pix['bank_payment_id']
    new_payment.qrcode = data_payment_pix['qr_code_path']
    db.session.add(new_payment)
    db.session.commit()
    return jsonify({'message': 'Pix payment created'}, {'payment': new_payment.to_dict()}), 201


@app.route("/payments/pix/qr_code/<file_name>", methods=['GET'])
def get_image(file_name):
    return send_file(f'static/img/{file_name}.png', mimetype='image/png') 

@app.route("/payments/pix/confirmation", methods=['POST'])
def pix_confirmation():
    return jsonify({'message': 'Pix payment confirmed'}), 201

#webhook
@app.route('/payments/pix/<int:payment_id>', methods=['GET']) 
def payments_pix_page(payment_id):
    payment = Payment.query.get(payment_id)
    return render_template('payment.html', payment_id=payment.id, 
                                            value=payment.value, 
                                            host='http://127.0.0.1:5000',
                                            qr_code=payment.qrcode)

def main():
    app.run(port=int(os.environ.get('PORT', 80)))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port, debug=True)