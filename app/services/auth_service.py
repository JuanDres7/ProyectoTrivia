import bcrypt
from app.repository.auth_repository import AuthRepository

class AuthService:

    def __init__(self, auth_repository: AuthRepository):
        self.auth_repository = auth_repository

    def autenticar(self, username: str, password: str) -> bool:
        usuario = self.auth_repository.obtener_por_username(username)
        if usuario is None:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), usuario.password_hash.encode("utf-8"))
