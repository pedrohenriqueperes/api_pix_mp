#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para decodificar código PIX EMV e verificar dados do beneficiário
"""

def decode_pix_emv(pix_code):
    """
    Decodifica um código PIX EMV e extrai as informações principais
    """
    print("=== DECODIFICAÇÃO DO CÓDIGO PIX ===")
    print(f"Código PIX: {pix_code}")
    print("\n=== ANÁLISE DOS CAMPOS ===")
    
    # Campos principais do EMV
    fields = {
        '00': 'Payload Format Indicator',
        '01': 'Point of Initiation Method',
        '26': 'Merchant Account Information',
        '52': 'Merchant Category Code',
        '53': 'Transaction Currency',
        '54': 'Transaction Amount',
        '58': 'Country Code',
        '59': 'Merchant Name',
        '60': 'Merchant City',
        '62': 'Additional Data Field Template',
        '63': 'CRC'
    }
    
    i = 0
    while i < len(pix_code):
        if i + 4 > len(pix_code):
            break
            
        # Extrai tag (2 dígitos) e tamanho (2 dígitos)
        tag = pix_code[i:i+2]
        length_str = pix_code[i+2:i+4]
        
        # Verifica se o tamanho é um número válido
        try:
            length = int(length_str)
        except ValueError:
            print(f"Erro ao processar campo {tag} - tamanho inválido: {length_str}")
            break
        
        if i + 4 + length > len(pix_code):
            break
            
        # Extrai o valor
        value = pix_code[i+4:i+4+length]
        
        # Mostra informação do campo
        field_name = fields.get(tag, f'Campo {tag}')
        print(f"Tag {tag} ({field_name}): {value}")
        
        # Análise especial para campos importantes
        if tag == '26':  # Merchant Account Information
            print("  -> Analisando informações da conta:")
            decode_merchant_info(value)
        elif tag == '59':  # Merchant Name
            print(f"  -> NOME DO BENEFICIÁRIO: {value}")
        elif tag == '60':  # Merchant City
            print(f"  -> CIDADE: {value}")
        elif tag == '54':  # Transaction Amount
            if value:
                print(f"  -> VALOR: R$ {value}")
            else:
                print(f"  -> VALOR: Não especificado (PIX dinâmico)")
        
        i += 4 + length

def decode_merchant_info(merchant_data):
    """
    Decodifica as informações da conta do merchant (campo 26)
    """
    i = 0
    while i < len(merchant_data):
        if i + 4 > len(merchant_data):
            break
            
        tag = merchant_data[i:i+2]
        length = int(merchant_data[i+2:i+4])
        
        if i + 4 + length > len(merchant_data):
            break
            
        value = merchant_data[i+4:i+4+length]
        
        if tag == '00':
            print(f"    GUI: {value}")
        elif tag == '01':
            print(f"    CHAVE PIX: {value}")
        
        i += 4 + length

def simple_decode(pix_code):
    """
    Decodificação simples focada nos campos principais
    """
    print("\n=== DECODIFICAÇÃO SIMPLES ===")
    
    # Busca por padrões específicos
    import re
    
    # Procura pelo nome do beneficiário (campo 59)
    name_match = re.search(r'59(\d{2})([^0-9]{2,})', pix_code)
    if name_match:
        name_length = int(name_match.group(1))
        name = name_match.group(2)[:name_length]
        print(f"NOME DO BENEFICIÁRIO: {name}")
    
    # Procura pela cidade (campo 60)
    city_match = re.search(r'60(\d{2})([^0-9]{2,})', pix_code)
    if city_match:
        city_length = int(city_match.group(1))
        city = city_match.group(2)[:city_length]
        print(f"CIDADE: {city}")
    
    # Procura pela chave PIX
    pix_key_match = re.search(r'01(\d{2})([a-f0-9-]{36})', pix_code)
    if pix_key_match:
        key_length = int(pix_key_match.group(1))
        pix_key = pix_key_match.group(2)[:key_length]
        print(f"CHAVE PIX: {pix_key}")

if __name__ == "__main__":
    # Código PIX do teste anterior
    pix_code = "00020126580014br.gov.bcb.pix01367f07e6ec-2076-44e4-bfa6-07c1281ea920520400005303986540041.005802BR5924PERESPEDRO202306251807486009Sao Paulo62250521mpqrinter11540144411463042D21"
    
    decode_pix_emv(pix_code)
    simple_decode(pix_code)
    
    print("\n=== CONCLUSÃO ===")
    print("Verifique se o NOME DO BENEFICIÁRIO está correto.")
    print("Se ainda aparecer dados pessoais, o problema está nas credenciais do Mercado Pago.")