from app.database.database import crear_tablas, get_session, engine
from app.repository.auth_repository import AuthRepository
from app.repository.contenido_repository import ContenidoRepository
from app.repository.partida_repository import PartidaRepository
from app.services.auth_service import AuthService
from app.services.contenido_service import ContenidoService
from app.services.partida_service import PartidaService
from app.ui.app import App

# Importar todos los modelos antes de crear tablas
import app.database.models  # noqa: F401

_NIVELES = [
    {"id": 1, "nombre": "Fácil",   "num_preguntas": 10, "tiempo_limite_seg": 30},
    {"id": 2, "nombre": "Medio",   "num_preguntas": 15, "tiempo_limite_seg": 25},
    {"id": 3, "nombre": "Difícil", "num_preguntas": 20, "tiempo_limite_seg": 20},
]

def _inicializar_niveles():
    from sqlmodel import Session
    from app.database.models.contenido import NivelDificultad
    with Session(engine) as session:
        for datos in _NIVELES:
            if not session.get(NivelDificultad, datos["id"]):
                session.add(NivelDificultad(**datos))
        session.commit()


def main():
    crear_tablas()
    _inicializar_niveles()

    session = get_session()

    # Inyección de dependencias — capa repository
    auth_repo = AuthRepository(session)
    contenido_repo = ContenidoRepository(session)
    partida_repo = PartidaRepository(session)

    # Inyección de dependencias — capa services
    auth_service = AuthService(auth_repo)
    contenido_service = ContenidoService(contenido_repo)
    partida_service = PartidaService(partida_repo, contenido_repo)

    # Iniciar la aplicación
    app = App(
        auth_service=auth_service,
        contenido_service=contenido_service,
        partida_service=partida_service,
    )
    app.mainloop()


if __name__ == "__main__":
    main()
