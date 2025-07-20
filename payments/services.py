# payments/services.py
import mercadopago
from django.conf import settings
import os

def get_payment(price, description, payer_data=None):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    
    # ❌ REMOVER: Dados hardcoded
    # Dados padrão do pagador (vindos das variáveis de ambiente)
    default_payer = {
        "email": os.getenv('DEFAULT_PAYER_EMAIL'),
        "first_name": os.getenv('DEFAULT_PAYER_FIRST_NAME'),
        "last_name": os.getenv('DEFAULT_PAYER_LAST_NAME'),
        "identification": {
            "type": os.getenv('DEFAULT_PAYER_ID_TYPE'),
            "number": os.getenv('DEFAULT_PAYER_ID_NUMBER')
        },
        "address": {
            "zip_code": os.getenv('DEFAULT_PAYER_ZIP_CODE'),
            "street_name": os.getenv('DEFAULT_PAYER_STREET_NAME'),
            "street_number": os.getenv('DEFAULT_PAYER_STREET_NUMBER'),
            "neighborhood": os.getenv('DEFAULT_PAYER_NEIGHBORHOOD'),
            "city": os.getenv('DEFAULT_PAYER_CITY'),
            "federal_unit": os.getenv('DEFAULT_PAYER_STATE')
        }
    }
    
    payment_data = {
        "transaction_amount": float(price),
        "description": str(description),
        "payment_method_id": "pix",
        "payer": payer_data if payer_data else default_payer
    }
    
    payment_response = sdk.payment().create(payment_data)
    payment = payment_response["response"]
    data = payment['point_of_interaction']['transaction_data']
    return {'clipboard': str(data['qr_code']), 'qrcode': 'data:image/jpeg;base64,{}'.format(data['qr_code_base64']), 'id': payment['id']}

def verify_payment(payment_id):
    sdk = mercadopago.SDK(settings.MERCADO_PAGO_ACCESS_TOKEN)
    payment_response = sdk.payment().get(int(payment_id))
    payment = payment_response["response"]
    status = payment['status']
    detail = payment['status_detail']
    return {'id': payment_id, 'status': status, 'status_detail': detail}