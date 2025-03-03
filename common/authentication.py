import jwt, datetime
from decouple import config
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

from core.models import User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        
        token = request.COOKIES.get('user_session')
        
        if not token:
            return None
        
        try:
            payload = jwt.decode(token, config('JWT_SECRET'), algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Unauthenticated')
        
        user = User.objects.get(id=payload['user_id'])
        
        if user is None:
            raise exceptions.AuthenticationFailed('Unauthenticated')
         
        return (user, None)  
            
    
    @staticmethod
    def generate_jwt(id):
        payload = {
            'user_id': str(id), 
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }
        
        return jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')