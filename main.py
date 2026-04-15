from app.database.database import crear_tablas, get_session
from app.repository.usuario_repository import UsuarioRepository
from app.services.auth_service import AuthService
from app.ui.app import App

# Importar todos los modelos antes de crear tablas
import app.database.models  # noqa: F401


def main():
    crear_tablas()

    session = get_session()

    # Inyección de dependencias — capa repository
    usuario_repo = UsuarioRepository(session)

    # Inyección de dependencias — capa services
    auth_service = AuthService(usuario_repo)

    # Iniciar la aplicación
    app = App(auth_service=auth_service)
    app.mainloop()


if __name__ == "__main__":
    main()
