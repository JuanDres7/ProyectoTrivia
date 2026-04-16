from sqlmodel import Session, select
from app.database.models.autenticacion import Usuario

class AuthRepository:

    def __init__(self, session: Session):
        self.session = session

    def obtener_por_username(self, username: str) -> Usuario | None:
        statement = select(Usuario).where(Usuario.username == username)
        return self.session.exec(statement).first()
