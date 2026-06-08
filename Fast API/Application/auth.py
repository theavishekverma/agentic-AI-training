from fastapi import Header, HTTPException

VALID_API_KEYS = ["laptop-key-123", "admin-key-456", "test-key-789"]

def verify_api_key(x_api_key: str = Header(..., description="API Key required")) -> str:
    """
    Validate API Key from request header.
    
    Raises:
        HTTPException: 401 if API key is invalid
    """
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="❌ Invalid API Key. Access Denied!",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return x_api_key
