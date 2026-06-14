from fastapi import Header, HTTPException

def authenticate_user(api_key: str = Header(...)):
    print(f"Received API key: {api_key}")
    print(f"Expected API key: my_secure_api_key")
    # In a real application, you would check this against a database or environment variable
    if api_key != "my_secure_api_key":
        raise HTTPException(status_code=403, detail="User is not authorized to perform this action")
    return True