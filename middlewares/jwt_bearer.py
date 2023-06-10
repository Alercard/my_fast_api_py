from fastapi.security import HTTPBearer
from fastapi import HTTPException, Request
from utils.jwt_manager import validate_token

# It must addes as a dependency to the routes you want to protect
class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        # invoke parent __call__ (HTTPBearer.__call__)
        auth = await super().__call__(request)
        # validate credencials
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail='Invalid Credentials')
