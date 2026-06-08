"""
FastAPI API Key Validation - Multiple Methods
Demonstrates different approaches to validate API keys in FastAPI
"""

from fastapi import FastAPI, HTTPException, status, Header, Query, Depends
from fastapi.security import APIKeyHeader, APIKeyQuery
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="API Key Validation Examples",
    description="Complete guide to validating API keys in FastAPI",
    version="1.0.0"
)

# ============================================================================
# Method 1: Using APIKeyHeader (Most Common - API Key in Headers)
# ============================================================================

api_key_header = APIKeyHeader(name="X-API-Key", description="API Key in header")

async def verify_api_key_header(api_key: str = Depends(api_key_header)):
    """Verify API Key from request headers"""
    # Store valid API keys (in production, use database)
    VALID_API_KEYS = ["secret-api-key-123", "test-key-456", "production-key-789"]
    
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return api_key


@app.get("/method1/data", tags=["Method 1: Header"])
async def get_data_with_header_key(api_key: str = Depends(verify_api_key_header)):
    """Endpoint protected by API Key in header"""
    return {"message": "Success! API Key is valid", "api_key": api_key[:5] + "****"}


# ============================================================================
# Method 2: Using APIKeyQuery (API Key in Query Parameters)
# ============================================================================

api_key_query = APIKeyQuery(name="api_key", description="API Key as query parameter")

async def verify_api_key_query(api_key: str = Depends(api_key_query)):
    """Verify API Key from query parameters"""
    VALID_API_KEYS = ["secret-api-key-123", "test-key-456", "production-key-789"]
    
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key


@app.get("/method2/data", tags=["Method 2: Query Param"])
async def get_data_with_query_key(api_key: str = Depends(verify_api_key_query)):
    """Endpoint protected by API Key in query parameter
    Usage: /method2/data?api_key=secret-api-key-123
    """
    return {"message": "Success! API Key is valid", "api_key": api_key[:5] + "****"}


# ============================================================================
# Method 3: Manual Header Validation (Flexible)
# ============================================================================

async def verify_api_key_manual(x_api_key: Optional[str] = Header(None)):
    """Manually verify API Key from headers"""
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key header missing"
        )
    
    VALID_API_KEYS = ["secret-api-key-123", "test-key-456", "production-key-789"]
    
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return x_api_key


@app.get("/method3/data", tags=["Method 3: Manual Header"])
async def get_data_manual(api_key: str = Depends(verify_api_key_manual)):
    """Endpoint with manual header validation"""
    return {"message": "Success! API Key is valid", "api_key": api_key[:5] + "****"}


# ============================================================================
# Method 4: API Key with Role-Based Access Control (RBAC)
# ============================================================================

class APIKeyUser(BaseModel):
    key: str
    name: str
    role: str  # admin, user, readonly

# Simulated database of API keys with roles
API_KEYS_DB = {
    "secret-api-key-123": APIKeyUser(key="secret-api-key-123", name="Admin User", role="admin"),
    "test-key-456": APIKeyUser(key="test-key-456", name="Regular User", role="user"),
    "production-key-789": APIKeyUser(key="production-key-789", name="Read-only User", role="readonly"),
}

async def verify_api_key_with_role(x_api_key: str = Header(...)):
    """Verify API Key and get user role information"""
    if x_api_key not in API_KEYS_DB:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return API_KEYS_DB[x_api_key]


@app.get("/method4/admin", tags=["Method 4: RBAC"])
async def admin_endpoint(user: APIKeyUser = Depends(verify_api_key_with_role)):
    """Admin only endpoint - requires admin role"""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. User role '{user.role}' is not allowed. Admin role required."
        )
    return {"message": f"Welcome Admin: {user.name}", "role": user.role}


@app.get("/method4/user", tags=["Method 4: RBAC"])
async def user_endpoint(user: APIKeyUser = Depends(verify_api_key_with_role)):
    """User endpoint - requires admin or user role"""
    if user.role not in ["admin", "user"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Access denied. Read-only access not allowed."
        )
    return {"message": f"Welcome User: {user.name}", "role": user.role}


@app.get("/method4/data", tags=["Method 4: RBAC"])
async def read_data_endpoint(user: APIKeyUser = Depends(verify_api_key_with_role)):
    """Public endpoint - all authenticated users can access"""
    return {"message": f"Welcome {user.name}", "role": user.role}


# ============================================================================
# Method 5: API Key with Rate Limiting Metadata
# ============================================================================

class APIKeyWithMeta(BaseModel):
    key: str
    name: str
    requests_per_minute: int
    active: bool

API_KEYS_WITH_LIMITS = {
    "secret-api-key-123": APIKeyWithMeta(key="secret-api-key-123", name="Admin", requests_per_minute=1000, active=True),
    "test-key-456": APIKeyWithMeta(key="test-key-456", name="Developer", requests_per_minute=100, active=True),
    "inactive-key": APIKeyWithMeta(key="inactive-key", name="Disabled", requests_per_minute=50, active=False),
}

async def verify_api_key_with_limits(x_api_key: str = Header(...)):
    """Verify API Key and check if it's active"""
    if x_api_key not in API_KEYS_WITH_LIMITS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    
    key_data = API_KEYS_WITH_LIMITS[x_api_key]
    
    if not key_data.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key is disabled"
        )
    
    return key_data


@app.get("/method5/status", tags=["Method 5: Rate Limiting"])
async def check_key_status(key_data: APIKeyWithMeta = Depends(verify_api_key_with_limits)):
    """Check API Key status and limits"""
    return {
        "name": key_data.name,
        "active": key_data.active,
        "requests_per_minute": key_data.requests_per_minute,
        "status": "Ready to use" if key_data.active else "Disabled"
    }


# ============================================================================
# Method 6: Multiple API Key Methods (Header OR Query)
# ============================================================================

async def verify_api_key_flexible(
    x_api_key: Optional[str] = Header(None),
    api_key: Optional[str] = Query(None)
):
    """Accept API Key from header or query parameter"""
    key = x_api_key or api_key
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API Key required in header (X-API-Key) or query parameter (api_key)"
        )
    
    VALID_API_KEYS = ["secret-api-key-123", "test-key-456", "production-key-789"]
    
    if key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return key


@app.get("/method6/data", tags=["Method 6: Flexible"])
async def flexible_auth(api_key: str = Depends(verify_api_key_flexible)):
    """Accept API Key from header or query parameter"""
    return {"message": "Success! API Key is valid", "api_key": api_key[:5] + "****"}


# ============================================================================
# Health Check / Documentation
# ============================================================================

@app.get("/", tags=["Info"])
async def root():
    """API Documentation - shows all available endpoints"""
    return {
        "title": "API Key Validation Examples",
        "methods": [
            {
                "method": 1,
                "name": "Header-based (Recommended)",
                "endpoint": "/method1/data",
                "usage": "curl -H 'X-API-Key: secret-api-key-123' http://localhost:8000/method1/data"
            },
            {
                "method": 2,
                "name": "Query Parameter",
                "endpoint": "/method2/data",
                "usage": "http://localhost:8000/method2/data?api_key=secret-api-key-123"
            },
            {
                "method": 3,
                "name": "Manual Header",
                "endpoint": "/method3/data",
                "usage": "curl -H 'x-api-key: secret-api-key-123' http://localhost:8000/method3/data"
            },
            {
                "method": 4,
                "name": "Role-Based Access Control",
                "endpoints": ["/method4/admin", "/method4/user", "/method4/data"],
                "usage": "curl -H 'X-API-Key: secret-api-key-123' http://localhost:8000/method4/admin"
            },
            {
                "method": 5,
                "name": "With Rate Limiting",
                "endpoint": "/method5/status",
                "usage": "curl -H 'X-API-Key: secret-api-key-123' http://localhost:8000/method5/status"
            },
            {
                "method": 6,
                "name": "Flexible (Header or Query)",
                "endpoint": "/method6/data",
                "usage": "curl -H 'X-API-Key: secret-api-key-123' http://localhost:8000/method6/data"
            }
        ],
        "valid_api_keys": ["secret-api-key-123", "test-key-456", "production-key-789"],
        "note": "Visit /docs for interactive API documentation (Swagger UI)"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
