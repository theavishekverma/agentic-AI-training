from fastapi import Depends, Header, HTTPException
from fastapi.security import APIKeyHeader, HTTPBasic

VALID_API_KEYS = ["laptop-key-123", "admin", "test-key-789"]

# api_key_header = APIKeyHeader(name="X-API-Key", description="API Key required for authentication")

# secret_key = HTTPBasic()

# def verify_api_key(x_api_key: str = Header(..., description="API Key required")) -> str:
#     """
#     Validate API Key from request header.
    
#     Raises:
#         HTTPException: 401 if API key is invalid or missing.
#     """
#     if x_api_key not in VALID_API_KEYS:
#         raise HTTPException(
#             status_code=401,
#             detail="❌ Invalid API Key. Access Denied!",
#             headers={"WWW-Authenticate": "Bearer"}
#         )
#     return x_api_key


# ============================================================================
# API Key Security
# ============================================================================

api_key_header = APIKeyHeader(name="X-API-Key", description="API Key required for authentication")

async def verify_api_key(x_api_key: str = Depends(api_key_header)):
    """Verify API Key from request headers"""
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return x_api_key
