# PIX Payment API - Django & Mercado Pago

## Project Overview

This is a Django-based payment system that integrates with Mercado Pago's PIX API. The system enables generating PIX payment codes (Brazil's instant payment system), verifying transaction status in real-time, and handling webhook notifications for automatic status updates.

### Core Features
- PIX payment code generation via Mercado Pago API
- Real-time payment status verification
- Webhook support for automatic status updates
- Responsive web interface
- MySQL database persistence for transactions
- QR code generation for PIX payments
- Multiple payment plan support

### Technology Stack
- **Framework:** Django 5.1
- **Database:** MySQL (via mysqlclient)
- **Payment Provider:** Mercado Pago SDK 2.1.0
- **QR Code:** qrcode library
- **Environment:** python-dotenv

## Project Structure

```
api_pix_mp/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── decode_pix.py            # PIX EMV code decoder utility
├── test_payment.py          # Payment API test script
├── pix_payment/             # Django project settings
│   ├── settings.py          # Django configuration
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI application
└── payments/                # Main application
    ├── models.py            # Transaction model
    ├── views.py             # Payment endpoints
    ├── services.py          # Mercado Pago integration
    ├── pix_utils.py         # PIX code generation utilities
    ├── urls.py              # App URL routing
    ├── admin.py             # Django admin configuration
    └── templates/payments/
        └── index.html       # Frontend interface
```

## Building and Running

### Prerequisites
- Python 3.x
- MySQL database
- Mercado Pago account (with API credentials)

### Installation

1. **Clone and setup virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your credentials
```

4. **Required environment variables:**
```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=3306

# PIX Configuration
PIX_MERCHANT_NAME=Your Name or Company
PIX_CITY=Your City
PIX_KEY=your-pix-key

# Mercado Pago Configuration
MERCADO_PAGO_PUBLIC_KEY=your-public-key
MERCADO_PAGO_ACCESS_TOKEN=your-access-token

# Default Payer Information
DEFAULT_PAYER_EMAIL=payer@example.com
DEFAULT_PAYER_FIRST_NAME=First
DEFAULT_PAYER_LAST_NAME=Last
DEFAULT_PAYER_ID_TYPE=CPF
DEFAULT_PAYER_ID_NUMBER=12345678901
DEFAULT_PAYER_ZIP_CODE=12345-678
DEFAULT_PAYER_STREET_NAME=Street Name
DEFAULT_PAYER_STREET_NUMBER=123
DEFAULT_PAYER_NEIGHBORHOOD=Neighborhood
DEFAULT_PAYER_CITY=City
DEFAULT_PAYER_STATE=SP
```

5. **Run migrations:**
```bash
python manage.py migrate
```

6. **Start development server:**
```bash
python manage.py runserver
```

### Testing

**Run the payment test script:**
```bash
python test_payment.py
```

**Decode a PIX code:**
```bash
python decode_pix.py
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main payment interface |
| `/generate-payment/` | POST | Generate PIX payment code |
| `/verify-payment/` | POST | Verify payment status |
| `/webhook/` | POST | Mercado Pago webhook receiver |

### Request/Response Examples

**Generate Payment:**
```json
POST /generate-payment/
{
  "price": 50.0,
  "description": "Payment description",
  "payer": { /* optional payer data */ }
}

Response:
{
  "transaction_id": "123456789",
  "clipboard": "PIX EMV code",
  "qrcode": "data:image/jpeg;base64,..."
}
```

**Verify Payment:**
```json
POST /verify-payment/
{
  "transaction_id": "123456789"
}

Response:
{
  "id": "123456789",
  "status": "approved",
  "status_detail": "accredited"
}
```

## Development Conventions

### Code Style
- Python standard conventions (PEP 8)
- Django best practices for app structure
- Environment variables for sensitive configuration (never hardcode credentials)

### Testing Practices
- Use `test_payment.py` for API endpoint testing
- Verify webhook functionality with Mercado Pago sandbox
- Test PIX code decoding with `decode_pix.py`

### Database
- MySQL with `utf8mb4` charset
- Strict SQL mode enabled
- Transaction model stores: `transaction_id`, `amount`, `status`, `created_at`, `updated_at`

### Security Considerations
- Keep `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` appropriately
- Use HTTPS in production
- Never commit `.env` file (contains API credentials)
- CSRF exemption on payment endpoints is intentional for API usage

## Common Issues & Solutions

### PIX Configuration Issues
If beneficiary name shows personal data instead of configured `PIX_MERCHANT_NAME`:
- Verify `PIX_MERCHANT_NAME`, `PIX_CITY`, and `PIX_KEY` in `.env`
- Check Mercado Pago account settings
- Ensure credentials are from the correct environment (sandbox vs production)

### Database Connection
- Ensure MySQL is running
- Verify database credentials in `.env`
- Check database exists and user has permissions

### Webhook Setup (Production)
1. Configure public URL (use ngrok for testing)
2. Add webhook URL in Mercado Pago dashboard
3. Add URL to `ALLOWED_HOSTS` in settings

## Transaction Status Flow

```
pending → approved (successful payment)
pending → rejected (payment failed)
pending → cancelled (user cancelled)
```

Status details available via `status_detail` field (e.g., `accredited`, `pending_contingency`).
