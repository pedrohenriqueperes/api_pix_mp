#!/usr/bin/env python3
import requests
import json

# Teste da geração de pagamento PIX
url = 'http://127.0.0.1:8000/generate-payment/'
data = {
    'price': 1.0,
    'description': 'Teste de pagamento'
}

try:
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n=== DADOS DO PAGAMENTO ===")
        print(f"Transaction ID: {result.get('transaction_id')}")
        print(f"\nCódigo PIX (clipboard):")
        print(result.get('clipboard'))
        print(f"\nQR Code: {result.get('qrcode')[:100]}...")
        
        # Teste de verificação
        verify_url = 'http://127.0.0.1:8000/verify-payment/'
        verify_data = {'transaction_id': result.get('transaction_id')}
        
        verify_response = requests.post(verify_url, json=verify_data)
        print(f"\n=== VERIFICAÇÃO ===")
        print(f"Status Code: {verify_response.status_code}")
        print(f"Response: {verify_response.text}")
        
except Exception as e:
    print(f"Erro: {e}")