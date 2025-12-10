# Social Media API - Authentication Documentation

## Overview
This authentication system provides user registration, login, token-based authentication, and profile management for the social media API.

## API Endpoints

### 1. User Registration
**Endpoint:** `POST /api/accounts/register/`

**Permission:** Public (No authentication required)

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "bio": "Hello, I'm John!", // Optional
  "profile_picture": null // Optional (file upload)
}
```

**Response:** `201 CREATED`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "date_joined": "2025-12-10T10:30:00Z"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "User registered successfully"
}
```

**Validation Rules:**
- Username must be unique
- Email must be unique and valid
- Password minimum length: 8 characters
- Passwords must match

---

### 2. User Login
**Endpoint:** `POST /api/accounts/login/`

**Permission:** Public (No authentication required)

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Hello, I'm John!",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "date_joined": "2025-12-10T10:30:00Z"
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "Login successful"
}
```

---

### 3. Get User Profile
**Endpoint:** `GET /api/accounts/profile/`

**Permission:** Authenticated users only

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "bio": "Hello, I'm John!",
  "profile_picture": null,
  "followers_count": 0,
  "following_count": 0,
  "date_joined": "2025-12-10T10:30:00Z"
}
```

---

### 4. Update User Profile
**Endpoint:** `PUT /api/accounts/profile/` or `PATCH /api/accounts/profile/`

**Permission:** Authenticated users only

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Request Body:** (All fields are optional for PATCH)
```json
{
  "email": "newemail@example.com",
  "bio": "Updated bio text",
  "profile_picture": null
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "newemail@example.com",
  "bio": "Updated bio text",
  "profile_picture": null,
  "followers_count": 0,
  "following_count": 0,
  "date_joined": "2025-12-10T10:30:00Z"
}
```

---

### 5. User Logout
**Endpoint:** `POST /api/accounts/logout/`

**Permission:** Authenticated users only

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response:** `200 OK`
```json
{
  "message": "Logout successful"
}
```

**Note:** This endpoint deletes the user's authentication token. After logout, the token will no longer be valid.

---

## Authentication

This API uses **Token Authentication**. After successful registration or login, you'll receive an authentication token. Include this token in the `Authorization` header for all authenticated endpoints:

```
Authorization: Token YOUR_TOKEN_HERE
```

### Example using cURL:
```bash
curl -X GET http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Example using Python Requests:
```python
import requests

token = "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
headers = {"Authorization": f"Token {token}"}

response = requests.get(
    "http://localhost:8000/api/accounts/profile/",
    headers=headers
)
```

---

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Testing the API

### Using Django Shell:
```bash
python manage.py shell
```

```python
from accounts.models import User
from rest_framework.authtoken.models import Token

# Create a test user
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpass123'
)

# Get the token
token = Token.objects.get(user=user)
print(f"Token: {token.key}")
```

### Using cURL:

**Register:**
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Get Profile:**
```bash
curl -X GET http://localhost:8000/api/accounts/profile/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

---

## Setup Instructions

1. **Make sure migrations are applied:**
```bash
python manage.py makemigrations
python manage.py migrate
```

2. **Create a superuser (optional):**
```bash
python manage.py createsuperuser
```

3. **Run the development server:**
```bash
python manage.py runserver
```

4. **Test the endpoints** using the examples above or with tools like:
   - Postman
   - Insomnia
   - cURL
   - HTTPie

---

## Features Implemented

✅ User registration with email validation  
✅ Password confirmation during registration  
✅ Automatic token generation on registration  
✅ User login with token retrieval  
✅ Token-based authentication  
✅ User profile retrieval (authenticated)  
✅ User profile update (authenticated)  
✅ User logout (token deletion)  
✅ Follower/Following counts in user profile  
✅ Password hashing and security  
✅ Custom User model with bio and profile picture  

---

## Next Steps

Consider implementing:
- Password reset functionality
- Email verification
- Social authentication (Google, Facebook, etc.)
- Refresh tokens
- Rate limiting
- Password change endpoint
