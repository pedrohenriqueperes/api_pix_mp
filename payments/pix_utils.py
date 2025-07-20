# payments/pix_utils.py
import qrcode
import base64
from io import BytesIO
from django.conf import settings

def generate_pix_code(transaction_amount, merchant_name=None, city=None, pix_key=None):
    # Usar configurações do Django settings se não fornecidas
    if merchant_name is None:
        # ❌ PROBLEMA: Nome da empresa hardcoded
        merchant_name = getattr(settings, 'PIX_MERCHANT_NAME', None)
        if merchant_name is None:
            raise ValueError("PIX_MERCHANT_NAME deve ser configurada nas variáveis de ambiente")
    if city is None:
        # ❌ PROBLEMA: Cidade hardcoded
        city = getattr(settings, 'PIX_CITY', None)
        if city is None:
            raise ValueError("PIX_CITY deve ser configurada nas variáveis de ambiente")
    if pix_key is None:
        # ❌ PROBLEMA: Chave PIX hardcoded
        pix_key = getattr(settings, 'PIX_KEY', None)  # Remover o valor padrão
        if pix_key is None:
            raise ValueError("PIX_KEY deve ser configurada nas variáveis de ambiente")
    # Payload Format Indicator
    payload_format = "000201"
    
    # Point of Initiation Method
    initiation_method = "010212"
    
    # Merchant Account Information (Campo 26)
    gui = "0014br.gov.bcb.pix"
    key = f"01{len(pix_key):02d}{pix_key}"
    merchant_account_info = gui + key
    merchant_account = f"26{len(merchant_account_info):02d}{merchant_account_info}"
    
    # Merchant Category Code
    category_code = "52040000"
    
    # Transaction Currency (986 = BRL)
    currency = "5303986"
    
    # Transaction Amount
    amount_str = f"{transaction_amount:.2f}"
    amount = f"54{len(amount_str):02d}{amount_str}"
    
    # Country Code
    country = "5802BR"
    
    # Merchant Name
    name = f"59{len(merchant_name):02d}{merchant_name}"
    
    # Merchant City
    city_field = f"60{len(city):02d}{city}"
    
    # Additional Data Field Template (Campo 62)
    reference_label = "mpqrinter" + str(int(transaction_amount * 100)).zfill(10)
    reference = f"05{len(reference_label):02d}{reference_label}"
    additional_data = f"62{len(reference):02d}{reference}"
    
    # Montar payload sem CRC
    payload_without_crc = (
        payload_format +
        initiation_method +
        merchant_account +
        category_code +
        currency +
        amount +
        country +
        name +
        city_field +
        additional_data +
        "6304"  # CRC placeholder
    )
    
    # Calcular CRC
    crc = crc16_ccitt(payload_without_crc)
    
    # Payload final
    return payload_without_crc + crc

def crc16_ccitt(payload):
    crc = 0xFFFF
    polynom = 0x1021

    for byte in payload.encode():
        crc ^= byte << 8
        for _ in range(8):
            if crc & 0x8000:
                crc = (crc << 1) ^ polynom
            else:
                crc <<= 1
            crc &= 0xFFFF
    return f"{crc:04X}"

def generate_qr_code(pix_code):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pix_code)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()