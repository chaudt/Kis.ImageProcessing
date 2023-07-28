from fastapi import HTTPException, status, Security, FastAPI
from fastapi.security import APIKeyHeader, APIKeyQuery
import uvicorn

API_KEYS = [
    "9d207bf0-10f5-4d8f-a479-22ff5aeff8d1",
    "f47d4a2c-24cf-4745-937e-620a5963c0b8",
    "b7061546-75e8-444b-a2c4-f19655d07eb8",
]

api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )

app = FastAPI()

@app.get("/public")
def public():
    """A public endpoint that does not require any authentication."""
    return "Public Endpoint"

@app.get("/private")
def private(api_key: str = Security(get_api_key)):
    """A private endpoint that requires a valid API key to be provided."""
    return f"Private Endpoint. API Key: {api_key}"



if __name__=='__main__':
    uvicorn.run(app, host="127.0.0.1", port=3003)