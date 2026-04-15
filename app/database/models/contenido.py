from sqlmodel import SQLModel, Field

class NivelDificultad(SQLModel, table=True):
    __tablename__ = "niveles_dificultad"

    id: int | None  = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50)
    num_preguntas: int
    tiempo_limite_seg: int


class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: int | None = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100)
    descripcion: str | None = Field(default=None, max_length=255)
    activa: bool = Field(default=True)


class Pregunta(SQLModel, table=True):
    __tablename__ = "preguntas"

    id: int | None = Field(default=None, primary_key=True)
    categoria_id: int | None = Field(default=None, foreign_key="categorias.id")
    nivel_id: int = Field(foreign_key="niveles_dificultad.id")
    enunciado: str = Field(max_length=500)
    activa: bool = Field(default=True)


class Opcion(SQLModel, table=True):
    __tablename__ = "opciones"

    id:           int | None  = Field(default=None, primary_key=True)
    pregunta_id:  int         = Field(foreign_key="preguntas.id")
    letra:        str         = Field(max_length=1)   # A, B, C o D
    texto:        str         = Field(max_length=255)
    es_correcta:  bool        = Field(default=False)
