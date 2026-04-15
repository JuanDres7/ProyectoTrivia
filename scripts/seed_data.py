"""
Ejecutar una sola vez para inicializar la base de datos:
    python scripts/seed_data.py

Crea:
  - El usuario administrador (admin / admin123)
  - Los 3 niveles de dificultad
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import bcrypt
from sqlmodel import Session
from app.database.database import crear_tablas, engine
from app.database.models.autenticacion import Usuario
from app.database.models.contenido import NivelDificultad
import app.database.models  # noqa: F401 — registra todos los modelos


def seed():
    crear_tablas()

    with Session(engine) as session:
        # --- Admin ---
        password_hash = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        admin = Usuario(username="admin", password_hash=password_hash)
        session.add(admin)

        # --- Niveles de dificultad ---
        niveles = [
            NivelDificultad(id=1, nombre="Fácil",   num_preguntas=10, tiempo_limite_seg=30),
            NivelDificultad(id=2, nombre="Medio",   num_preguntas=15, tiempo_limite_seg=25),
            NivelDificultad(id=3, nombre="Difícil", num_preguntas=20, tiempo_limite_seg=20),
        ]
        for nivel in niveles:
            session.add(nivel)

        session.commit()
        print("Base de datos inicializada correctamente.")
        print("  Usuario: admin")
        print("  Contraseña: admin123")


if __name__ == "__main__":
    seed()