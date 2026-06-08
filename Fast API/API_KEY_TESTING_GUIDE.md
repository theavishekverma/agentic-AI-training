# FastAPI API Key Validation - Testing Guide

## Quick Start

### 1. Run the API Server
```bash
cd "c:\Users\Avishek\agentic-AI-training\Fast API"
uvicorn api_key_validation:app --reload
# or
uvicorn main:app --reload
```

Visit: http://localhost:8000/docs (Swagger UI)

---

## Testing API Key Validation

### Valid API Keys for Testing:
- `your-secure-api-key-123`
- `test-key-456`
- `production-key-789`

---

## Method 1: Using cURL with Header (Recommended)

```bash
# ✅ SUCCESS - Valid API Key
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/method1/data

# ❌ FAILURE - Invalid API Key
curl -H "X-API-Key: invalid-key" http://localhost:8000/method1/data

# ❌ FAILURE - Missing API Key
curl http://localhost:8000/method1/data
```

---

## Method 2: Using Query Parameter

```bash
# ✅ SUCCESS - Valid API Key in query
http://localhost:8000/method2/data?api_key=your-secure-api-key-123

# Using cURL:
curl "http://localhost:8000/method2/data?api_key=your-secure-api-key-123"

# ❌ FAILURE - Invalid API Key
curl "http://localhost:8000/method2/data?api_key=invalid-key"
```

---

## Method 3: Manual Header Validation

```bash
# ✅ SUCCESS
curl -H "x-api-key: your-secure-api-key-123" http://localhost:8000/method3/data

# ❌ FAILURE - Missing header
curl http://localhost:8000/method3/data
```

---

## Method 4: Role-Based Access Control (RBAC)

### Available Keys with Roles:
| API Key | Name | Role | Permissions |
|---------|------|------|-------------|
| `your-secure-api-key-123` | Admin User | admin | All endpoints |
| `test-key-456` | Regular User | user | User & data endpoints |
| `production-key-789` | Read-only User | readonly | Data endpoint only |

### Test Admin Endpoint:
```bash
# ✅ SUCCESS - Admin can access
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/method4/admin

# ❌ FAILURE - Regular user cannot access admin endpoint
curl -H "X-API-Key: test-key-456" http://localhost:8000/method4/admin

# ❌ FAILURE - Read-only user cannot access admin endpoint
curl -H "X-API-Key: production-key-789" http://localhost:8000/method4/admin
```

### Test User Endpoint:
```bash
# ✅ SUCCESS - Admin can access
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/method4/user

# ✅ SUCCESS - Regular user can access
curl -H "X-API-Key: test-key-456" http://localhost:8000/method4/user

# ❌ FAILURE - Read-only user cannot access
curl -H "X-API-Key: production-key-789" http://localhost:8000/method4/user
```

### Test Public Data Endpoint:
```bash
# ✅ SUCCESS - All can access
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/method4/data
curl -H "X-API-Key: test-key-456" http://localhost:8000/method4/data
curl -H "X-API-Key: production-key-789" http://localhost:8000/method4/data
```

---

## Method 5: API Key with Rate Limiting

```bash
# ✅ SUCCESS - Active key
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/method5/status

# ❌ FAILURE - Disabled key
curl -H "X-API-Key: inactive-key" http://localhost:8000/method5/status
```

---

## Method 6: Flexible Authentication (Header OR Query)

```bash
# ✅ SUCCESS - Using header
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/method6/data

# ✅ SUCCESS - Using query parameter
curl "http://localhost:8000/method6/data?api_key=your-secure-api-key-123"

# ❌ FAILURE - No API Key provided
curl http://localhost:8000/method6/data
```

---

## Testing Laptop CRUD API (main.py)

### Example Requests:

#### Get All Laptops:
```bash
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/laptops
```

#### Get Specific Laptop:
```bash
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/laptops/1
```

#### Create New Laptop:
```bash
curl -X POST \
  -H "X-API-Key: your-secure-api-key-123" \
  -H "Content-Type: application/json" \
  -d '{"laptop_id": 1, "laptop_name": "Dell XPS 13", "laptop_brand": "Dell", "laptop_price": 999.99}' \
  http://localhost:8000/laptops
```

#### Get Laptops by Brand:
```bash
curl -H "X-API-Key: your-secure-api-key-123" http://localhost:8000/laptops_brand/Dell
```

#### Delete Laptop:
```bash
curl -X DELETE \
  -H "X-API-Key: your-secure-api-key-123" \
  http://localhost:8000/laptops/1
```

---

## Testing with Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"
API_KEY = "your-secure-api-key-123"
HEADERS = {"X-API-Key": API_KEY}

# Get all laptops
response = requests.get(f"{BASE_URL}/laptops", headers=HEADERS)
print(response.json())

# Create laptop
laptop_data = {
    "laptop_id": 1,
    "laptop_name": "Dell XPS 13",
    "laptop_brand": "Dell",
    "laptop_price": 999.99
}
response = requests.post(f"{BASE_URL}/laptops", json=laptop_data, headers=HEADERS)
print(response.json())

# Get specific laptop
response = requests.get(f"{BASE_URL}/laptops/1", headers=HEADERS)
print(response.json())

# Delete laptop
response = requests.delete(f"{BASE_URL}/laptops/1", headers=HEADERS)
print(response.json())

# Invalid API Key (should fail)
invalid_headers = {"X-API-Key": "invalid-key"}
response = requests.get(f"{BASE_URL}/laptops", headers=invalid_headers)
print(response.status_code)  # 401
print(response.json())
```

---

## Key Concepts

### 1. **APIKeyHeader Security**
- Uses FastAPI's built-in security schemes
- Automatically validates and documents in Swagger UI
- Standard HTTP header: `X-API-Key`

### 2. **Dependency Injection**
- `Depends(verify_api_key)` ensures every protected endpoint checks the key
- DRY principle - validation logic in one place

### 3. **HTTP Status Codes**
- `200 OK` - Successful request
- `201 Created` - Resource created
- `401 Unauthorized` - Invalid/missing API Key
- `403 Forbidden` - Valid key but insufficient permissions
- `404 Not Found` - Resource not found
- `400 Bad Request` - Invalid request data

### 4. **Best Practices**
✅ Store API keys in database (encrypted)  
✅ Use HTTPS in production  
✅ Rotate keys regularly  
✅ Log all authentication attempts  
✅ Rate limit API requests  
✅ Use different keys for different environments (dev, test, prod)

---

## Production Recommendations

1. **Store API Keys in Database**
   ```python
   # Instead of hardcoded list
   VALID_API_KEYS = ["key1", "key2"]  # ❌ Bad
   
   # Use database
   api_key = db.query(APIKey).filter(APIKey.key == x_api_key).first()  # ✅ Good
   ```

2. **Hash API Keys**
   ```python
   from passlib.context import CryptContext
   pwd_context = CryptContext(schemes=["bcrypt"])
   hashed_key = pwd_context.hash(api_key)
   ```

3. **Add Rate Limiting**
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   @app.get("/data")
   @limiter.limit("100/minute")
   async def get_data(api_key: str = Depends(verify_api_key)): ...
   ```

4. **Use CORS Properly**
   ```python
   from fastapi.middleware.cors import CORSMiddleware
   app.add_middleware(CORSMiddleware, ...)
   ```

5. **Add Logging**
   ```python
   import logging
   logger = logging.getLogger(__name__)
   logger.info(f"API Key validation: {api_key[:5]}****")
   ```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 Unauthorized | Check if API Key is correct and in X-API-Key header |
| 403 Forbidden | Check if user has proper role/permissions |
| Missing header error | Add X-API-Key header to request |
| CORS error | Configure CORS middleware |
| Database error | Check database connection string |

