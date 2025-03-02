import jwt, datetime
from decouple import config

class JWTAuthentication():
    @staticmethod
    def generate_jwt(id):
        payload = {
            'admin_id': str(id), 
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1),
            'iat': datetime.datetime.now(datetime.timezone.utc)
        }
        
        return jwt.encode(payload, config('JWT_SECRET'), algorithm='HS256')