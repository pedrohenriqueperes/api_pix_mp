# PIX Payment System with Django and Mercado Pago

This is a Django project that implements a PIX payment system integrated with the Mercado Pago API. The system allows generating PIX payment codes and verifying transaction status.

## Features

- PIX payment code generation
- Real-time payment status verification
- Webhook for automatic status updates
- Responsive web interface
- Transaction persistence in database
- Support for multiple payment plans

## Requirements

- Python 3.x
- Django 5.x
- mercadopago
- python-dotenv

## Installation

1. Clone the repository:
```bash
git clone https://github.com/pedrohenriqueperes/django-mercadopago-pix-.git
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install django mercadopago python-dotenv
```

4. Create a `.env` file in the project root with your Mercado Pago credentials:
```
MERCADO_PAGO_PUBLIC_KEY=YOUR_PUBLIC_KEY_HERE
MERCADO_PAGO_ACCESS_TOKEN=YOUR_ACCESS_TOKEN_HERE
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the server:
```bash
python manage.py runserver
```

## Webhook Configuration (Production)

To receive automatic payment status updates:

1. Configure a public URL (e.g., using ngrok for testing)
2. Add the webhook URL in the Mercado Pago dashboard
3. Add the URL to Django's ALLOWED_HOSTS

## Project Structure

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

## Usage

1. Access the application at `http://localhost:8000`
2. Select a payment plan
3. Copy the generated PIX code
4. Make the payment using any banking app
5. Verify payment status using the "Verify Payment" button

## Customization

To modify payment plan values, edit the `payments/templates/payments/index.html` file:

```html
<button onclick="generatePayment(50.0, 'Plan 1')">
    <!-- Change values as needed -->
</button>
```

## Production Environment

For production use:

1. Use production Mercado Pago credentials (APP_USR-)
2. Configure ALLOWED_HOSTS appropriately
3. Use HTTPS
4. Set up a proper web server (e.g., Nginx + Gunicorn)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Support

If you encounter any problems or have questions, please open an issue in the repository.

---
Developed by [Pedro Peres]
