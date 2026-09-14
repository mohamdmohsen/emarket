# eMarket API
 
This is the backend for eMarket, a small e-commerce project built with Django and Django REST Framework. It covers user accounts (register, login, forgot/reset password by email), a product catalog, and order handling — placing orders, viewing them, and updating their status.
 
I built this mainly to practice DRF properly: token auth, permissions, nested serializers, and wiring up email for password resets instead of just faking it in the console.
 
## Tech Stack
 
- **Framework:** Django + Django REST Framework
- **Auth:** Token Authentication (DRF `authtoken`)
- **Email:** Django's built-in email backend (SMTP) for password reset mail
- **Database:** SQLite for development — swap to PostgreSQL/MySQL in production via `DATABASES` in `settings.py`
## Project Structure
 
```
emarket/
├── account/        # Registration, login, user profile
├── product/        # Product catalog (CRUD)
├── order/          # Orders, order items, status updates
└── emarket/        # Project settings, root urls.py
```
 
## Setup
 
```bash
git clone <your-repo-url>
cd emarket
python -m venv env
env\Scripts\activate        # Windows
# source env/bin/activate   # macOS/Linux
 
pip install -r requirements.txt
 
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
 
## Authentication
 
All protected endpoints require a token in the request header:
 
```
Authorization: Token <your_token_here>
```
 
You get this token by registering or logging in (see below). Endpoints marked 🔒 require `IsAuthenticated`.
 
---
 
## Account Endpoints
 
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/account/register/` | Public | Create a new user account |
| POST | `/api/account/login/` | Public | Log in and receive an auth token |
| GET | `/api/account/profile/` | 🔒 | Get the logged-in user's profile |
| PUT | `/api/account/profile/update/` | 🔒 | Update profile details |
| POST | `/api/account/password/forgot/` | Public | Send a password reset link/token to the user's email |
| POST | `/api/account/password/reset/` | Public | Set a new password using the token from the email |
 
### Register
 
**Request**
```json
{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "strongpassword123"
}
```
 
**Response**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4",
    "user": {
        "id": 3,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```
 
### Login
 
**Request**
```json
{
    "username": "john_doe",
    "password": "strongpassword123"
}
```
 
**Response**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4"
}
```
 
### Forgot Password
 
Sends an email with a reset link (or token, depending on how you wire the frontend) to the address on file.
 
**Request**
```json
{
    "email": "john@example.com"
}
```
 
**Response**
```json
{
    "message": "Password reset email sent"
}
```
 
If the email doesn't match any account, respond with the same generic message anyway — don't leak whether an email is registered.
 
### Reset Password
 
Called after the user clicks the link from their email. The `token` and `uid` come from the query params/path in that link (standard Django `PasswordResetTokenGenerator` flow).
 
**Request**
```json
{
    "uid": "MjM",
    "token": "cf3x1z-3a1e6b2e0e...",
    "new_password": "newStrongerPassword123"
}
```
 
**Response**
```json
{
    "message": "Password has been reset successfully"
}
```
 
Common error cases: expired/invalid token, or `uid` that doesn't decode to a real user — both return 400.
 
---
 
## Product Endpoints
 
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/product/` | Public | List all products |
| GET | `/api/product/<id>/` | Public | Retrieve a single product |
| POST | `/api/product/new/` | 🔒 (admin) | Create a product |
| PUT | `/api/product/<id>/update/` | 🔒 (admin) | Update a product |
| DELETE | `/api/product/<id>/delete/` | 🔒 (admin) | Delete a product |
 
---
 
## Order Endpoints
 
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/order/new/` | 🔒 | Place a new order |
| GET | `/api/order/` | 🔒 | List the logged-in user's orders |
| GET | `/api/order/<id>/` | 🔒 | Retrieve a single order with its items |
| PUT | `/api/order/<id>/status/` | 🔒 (admin) | Update order status (`Proccessing`, `Shipped`, `Delivered`) |
 
### Create Order
 
**Request**
```json
{
    "city": "New York",
    "zipcode": "10001",
    "street": "12 Street, New York",
    "state": "NY",
    "country": "USA",
    "phone_no": "9225551234",
    "order_items": [
        {
            "product": 2,
            "quantity": 8,
            "price": 200.00
        }
    ]
}
```
 
**Response**
```json
{
    "orders": {
        "id": 7,
        "orderitems": [
            {
                "id": 5,
                "name": "Mac book",
                "quantity": 8,
                "price": "200.00",
                "product": 2,
                "order": 7
            }
        ],
        "city": "New York",
        "zipcode": "10001",
        "street": "12 Street, New York",
        "state": "NY",
        "country": "USA",
        "phone_no": "9225551234",
        "total_amount": 1600,
        "Payment_Status": "Unpaid",
        "payment_mod": "CARD",
        "status": "Proccessing",
        "create_at": "2026-09-14T15:34:41.731360Z",
        "user": 3
    }
}
```
 
### Update Order Status
 
**Request**
```json
{
    "status": "Shipped"
}
```
 
**Response**
```json
{
    "orders": {
        "id": 7,
        "status": "Shipped",
        "...": "..."
    }
}
```
 
Valid `status` values: `Proccessing`, `Shipped`, `Delivered`
Valid `Payment_Status` values: `Paid`, `Unpaid`
Valid `payment_mod` values: `CARD`, `Cash on Delivered`
 
---
 
## Email Configuration
 
Password reset emails need a real email backend, or they'll just print to the console during development. Add this to `settings.py`:
 
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'          # or your provider's SMTP host
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'   # not your normal password — use an app password
DEFAULT_FROM_EMAIL = 'eMarket <your_email@gmail.com>'
```
 
Don't hardcode these — pull them from environment variables in real deployments (`python-decouple` or `django-environ` work fine for this). While developing without SMTP set up yet, you can fall back to:
 
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
 
which just prints the email content to your terminal instead of sending it.
 
## Custom Error Responses
 
404 and 500 errors return JSON instead of Django's default HTML error pages, so the frontend always gets something predictable to parse:
 
```python
# views.py or wherever your handlers live
def handler404(request, exception):
    return JsonResponse({"error": "Path Not Found"}, status=404)
 
def handler500(request):
    return JsonResponse({"error": "Internal server error"}, status=500)
```
 
Wired up in the root `urls.py`:
 
```python
handler404 = 'emarket.views.handler404'
handler500 = 'emarket.views.handler500'
```
 
`DEBUG` needs to be `False` for these to actually fire — Django ignores custom handlers while `DEBUG = True` and shows its own debug page instead.
 
## Permissions Summary
 
| Role | Can do |
|---|---|
| Anonymous | Register, log in, browse products |
| Authenticated user | Place orders, view own orders, view/update own profile |
| Admin/staff | Manage products, update order status, view all orders |
 
Endpoints are protected using DRF's `IsAuthenticated` permission class:
 
```python
@permission_classes([IsAuthenticated])
```
 
For admin-only routes, pair this with a role check (e.g. `request.user.is_staff`) or a custom permission class.
 
## Error Handling
 
Errors are returned as JSON with an appropriate HTTP status code:
 
```json
{
    "error": "No Order Received"
}
```
 
| Status Code | Meaning |
|---|---|
| 400 | Bad request (e.g. missing/invalid fields) |
| 401 | Unauthorized (missing/invalid token) |
| 404 | Resource not found |
| 500 | Server error |
 
## Running Tests
 
```bash
python manage.py test
```
 
