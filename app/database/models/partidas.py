from sqlmodel import SQLModel, Field
from datetime import datetime


class Jugador(SQLModel, table=True):
    __tablename__ = "jugadores"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, index=True)
    total_partidas: int = Field(default=0)


class Partida(SQLModel, table=True):
    __tablename__ = "partidas"

    id: int | None = Field(default=None, primary_key=True)
    jugador_id: int = Field(foreign_key="jugadores.id")
    nivel_id: int = Field(foreign_key="niveles_dificultad.id")
    total_preguntas: int
    respuestas_correctas: int = Field(default=0)
    puntaje_final: int  = Field(default=0)
    estado: str = Field(default="en_curso")  # en_curso | finalizada | cancelada
    fecha: datetime = Field(default_factory=datetime.now)


class Respuesta(SQLModel, table=True):
    __tablename__ = "respuestas"

    id: int | None = Field(default=None, primary_key=True)
    partida_id: int = Field(foreign_key="partidas.id")
    pregunta_id: int = Field(foreign_key="preguntas.id")
    opcion_elegida_id: int = Field(foreign_key="opciones.id")
    es_correcta: bool
    puntos_obtenidos: int = Field(default=0)


class Ranking(SQLModel, table=True):
    __tablename__ = "ranking"

    id: int | None  = Field(default=None, primary_key=True)
    jugador_id: int = Field(foreign_key="jugadores.id")
    nombre: str = Field(max_length=100)
    nivel_id: int = Field(foreign_key="niveles_dificultad.id")
    puntaje: int
    es_record_global: bool = Field(default=False)
    fecha: datetime = Field(default_factory=datetime.now)
