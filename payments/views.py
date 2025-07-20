# payments/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services import get_payment, verify_payment
from .models import Transaction

def index(request):
    return render(request, 'payments/index.html')

@csrf_exempt
def generate_payment(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        price = data.get('price')
        description = data.get('description')
        payer_data = data.get('payer')  # Dados do pagador vindos da requisição
        
        if not price or not description:
            return JsonResponse({'error': 'Preço e descrição são obrigatórios'}, status=400)
        
        payment_data = get_payment(price, description, payer_data)
        
        # Salvar a transação
        Transaction.objects.create(
            transaction_id=str(payment_data['id']),
            amount=price,
            status='pending'
        )
        
        return JsonResponse({
            'transaction_id': payment_data['id'],
            'clipboard': payment_data['clipboard'],
            'qrcode': payment_data['qrcode']
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def verify_payment_status(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    try:
        data = json.loads(request.body)
        transaction_id = data.get('transaction_id')
        
        if not transaction_id:
            return JsonResponse({'error': 'ID da transação é obrigatório'}, status=400)
        
        payment_status = verify_payment(transaction_id)
        
        # Atualizar status da transação
        try:
            transaction = Transaction.objects.get(transaction_id=transaction_id)
            transaction.status = payment_status['status']
            transaction.save()
        except Transaction.DoesNotExist:
            pass
        
        return JsonResponse(payment_status)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def webhook(request):
    try:
        data = json.loads(request.body)
        if data['type'] == 'payment':
            payment_id = data['data']['id']
            # Verifica o status do pagamento
            payment_status = verify_payment(payment_id)
            # Atualiza o status no seu banco de dados
            transaction = Transaction.objects.get(transaction_id=payment_id)
            transaction.status = payment_status['status']
            transaction.save()
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)