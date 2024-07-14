from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import User
from .utils import decode_jwt


class CryptoJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return None
        if not authorization_header.startswith('Bearer '):
            raise AuthenticationFailed('Invalid Authorization header')
        jwt_token = authorization_header.split(' ')[1]
        payload = decode_jwt(jwt_token)
        if not payload:
            raise AuthenticationFailed('Invalid JWT token')
        try:
            request.role=payload.pop('role','')
            user = User.objects.get(**payload)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid user')
        return (user, None)
        
        
