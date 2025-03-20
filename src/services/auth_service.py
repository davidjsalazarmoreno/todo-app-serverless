import jwt
import datetime
from ..models.user import User
from ..repositories.user_repository import UserRepository
from ..utils.exceptions import AuthenticationException

class AuthService:
    def __init__(self, user_repository: UserRepository, secret_key: str):
        self.user_repository = user_repository
        self.secret_key = secret_key

    def authenticate(self, username: str, password: str):
        user = self.user_repository.find_by_username(username)
        
        if not user or not self._verify_password(password, user.password_hash):
            raise AuthenticationException("Invalid username or password")
        
        return self._generate_token(user)
    
    def _verify_password(self, plain_password: str, hashed_password: str):
        # En una aplicación real, usarías bcrypt o similar
        # Por simplicidad, asumimos una comparación directa
        return plain_password == hashed_password
    
    def _generate_token(self, user: User):
        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token
    
    def validate_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthenticationException("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationException("Invalid token")