import bcrypt
from app.repository.usuario_repository import UsuarioRepository


class AuthService:

    def __init__(self, usuario_repository: UsuarioRepository):
        self.usuario_repository = usuario_repository

    def autenticar(self, username: str, password: str) -> bool:
        usuario = self.usuario_repository.obtener_por_username(username)
        if usuario is None:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), usuario.password_hash.encode("utf-8"))
