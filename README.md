# Sistema de Pagamento PIX com Django e Mercado Pago

Este é um projeto Django que implementa um sistema de pagamento PIX integrado com a API do Mercado Pago. O sistema permite gerar códigos PIX para pagamento e verificar o status das transações.

## Funcionalidades

- Geração de códigos PIX para pagamento
- Verificação de status de pagamento em tempo real
- Webhook para atualizações automáticas de status
- Interface web responsiva
- Persistência de transações no banco de dados
- Suporte a múltiplos planos de pagamento

## Requisitos

- Python 3.x
- Django 5.x
- mercadopago
- python-dotenv

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/pedrohenriqueperes/django-mercadopago-pix-.git
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install django mercadopago python-dotenv
```

4. Crie um arquivo `.env` na raiz do projeto com suas credenciais do Mercado Pago:
```
MERCADO_PAGO_PUBLIC_KEY=SEU_PUBLIC_KEY_AQUI
MERCADO_PAGO_ACCESS_TOKEN=SEU_ACCESS_TOKEN_AQUI
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Inicie o servidor:
```bash
python manage.py runserver
```

## Configuração do Webhook (Produção)

Para receber atualizações automáticas do status dos pagamentos:

1. Configure uma URL pública (ex: usando ngrok para testes)
2. Adicione a URL do webhook no painel do Mercado Pago
3. Adicione a URL ao ALLOWED_HOSTS do Django

## Estrutura do Projeto

```
pix_payment/
    ├── manage.py
    ├── .env
    ├── pix_payment/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── payments/
        ├── models.py
        ├── services.py
        ├── urls.py
        ├── views.py
        └── templates/
            └── payments/
                └── index.html
```

## Uso

1. Acesse a aplicação em `http://localhost:8000`
2. Selecione um plano de pagamento
3. Copie o código PIX gerado
4. Efetue o pagamento usando qualquer aplicativo bancário
5. Verifique o status do pagamento usando o botão "Verificar pagamento"

## Customização

Para modificar os valores dos planos, edite o arquivo `payments/templates/payments/index.html`:

```html
<button onclick="generatePayment(50.0, 'Plano 1')">
    <!-- Altere os valores conforme necessário -->
</button>
```

## Ambiente de Produção

Para usar em produção:

1. Use credenciais de produção do Mercado Pago (APP_USR-)
2. Configure ALLOWED_HOSTS apropriadamente
3. Use HTTPS
4. Configure um servidor web adequado (ex: Nginx + Gunicorn)

## Contribuindo

Pull requests são bem-vindos. Para mudanças maiores, abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença

[MIT](https://choosealicense.com/licenses/mit/)

## Suporte

Se você encontrar algum problema ou tiver dúvidas, abra uma issue no repositório.

---
Desenvolvido por [Pedro Peres]
