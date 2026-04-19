from sqlmodel import Session, select, col
from app.database.models.contenido import Categoria, NivelDificultad, Opcion, Pregunta


class ContenidoRepository:

    def __init__(self, session: Session):
        self.session = session

    # ------------------------------------------------------------------ #
    # Categorias                                                           #
    # ------------------------------------------------------------------ #

    def crear_categoria(self, nombre: str, descripcion: str | None = None) -> Categoria:
        """Crea y persiste una nueva categoría en la base de datos."""
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        self.session.add(categoria)
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def obtener_categorias(self, solo_activas: bool = True) -> list[Categoria]:
        """Devuelve todas las categorías, opcionalmente filtrando solo las activas."""
        statement = select(Categoria)
        if solo_activas:
            statement = statement.where(Categoria.activa == True)
        return list(self.session.exec(statement).all())

    def obtener_categoria_por_id(self, categoria_id: int) -> Categoria | None:
        """Devuelve una categoría por su id, o None si no existe."""
        return self.session.get(Categoria, categoria_id)

    def actualizar_categoria(self, categoria_id: int, nombre: str, descripcion: str | None) -> Categoria | None:
        """Actualiza el nombre y descripción de una categoría. Devuelve None si no existe."""
        categoria = self.session.get(Categoria, categoria_id)
        if categoria is None:
            return None
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def desactivar_categoria(self, categoria_id: int) -> bool:
        """Marca la categoría como inactiva. Devuelve False si no existe."""
        categoria = self.session.get(Categoria, categoria_id)
        if categoria is None:
            return False
        categoria.activa = False
        self.session.commit()
        return True

    # ------------------------------------------------------------------ #
    # Niveles                                                              #
    # ------------------------------------------------------------------ #

    def obtener_niveles(self) -> list[NivelDificultad]:
        """Devuelve todos los niveles de dificultad registrados."""
        return list(self.session.exec(select(NivelDificultad)).all())

    def obtener_nivel_por_id(self, nivel_id: int) -> NivelDificultad | None:
        """Devuelve un nivel por su id, o None si no existe."""
        return self.session.get(NivelDificultad, nivel_id)

    # ------------------------------------------------------------------ #
    # Preguntas                                                            #
    # ------------------------------------------------------------------ #

    def crear_pregunta(self, enunciado: str, nivel_id: int, opciones: list[dict],
                       categoria_id: int | None = None) -> Pregunta:
        """Crea una pregunta y sus cuatro opciones de respuesta en una sola transacción."""
        pregunta = Pregunta(enunciado=enunciado, nivel_id=nivel_id, categoria_id=categoria_id)
        self.session.add(pregunta)
        self.session.flush()  # obtiene el id sin hacer commit aún

        for op in opciones:
            self.session.add(Opcion(
                pregunta_id=pregunta.id,
                letra=op["letra"],
                texto=op["texto"],
                es_correcta=op["es_correcta"],
            ))

        self.session.commit()
        self.session.refresh(pregunta)
        return pregunta

    def obtener_preguntas(self, nivel_id: int | None = None,
                          categoria_ids: list[int] | None = None,
                          solo_activas: bool = True) -> list[Pregunta]:
        """Devuelve preguntas con filtros opcionales de nivel, categorías y estado activo."""
        statement = select(Pregunta)
        if solo_activas:
            statement = statement.where(Pregunta.activa == True)
        if nivel_id is not None:
            statement = statement.where(Pregunta.nivel_id == nivel_id)
        if categoria_ids is not None:
            statement = statement.where(col(Pregunta.categoria_id).in_(categoria_ids))
        return list(self.session.exec(statement).all())

    def obtener_pregunta_por_id(self, pregunta_id: int) -> Pregunta | None:
        """Devuelve una pregunta por su id, o None si no existe."""
        return self.session.get(Pregunta, pregunta_id)

    def obtener_opciones_de_pregunta(self, pregunta_id: int) -> list[Opcion]:
        """Devuelve todas las opciones de respuesta de una pregunta."""
        statement = select(Opcion).where(Opcion.pregunta_id == pregunta_id)
        return list(self.session.exec(statement).all())

    def actualizar_pregunta(self, pregunta_id: int, enunciado: str, nivel_id: int,
                            opciones: list[dict], categoria_id: int | None = None) -> Pregunta | None:
        """Actualiza una pregunta reemplazando sus opciones anteriores. Devuelve None si no existe."""
        pregunta = self.session.get(Pregunta, pregunta_id)
        if pregunta is None:
            return None

        pregunta.enunciado = enunciado
        pregunta.nivel_id = nivel_id
        pregunta.categoria_id = categoria_id

        viejas = self.session.exec(select(Opcion).where(Opcion.pregunta_id == pregunta_id)).all()
        for op in viejas:
            self.session.delete(op)
        self.session.flush()

        for op in opciones:
            self.session.add(Opcion(
                pregunta_id=pregunta_id,
                letra=op["letra"],
                texto=op["texto"],
                es_correcta=op["es_correcta"],
            ))

        self.session.commit()
        self.session.refresh(pregunta)
        return pregunta

    def desactivar_pregunta(self, pregunta_id: int) -> bool:
        """Marca la pregunta como inactiva para que no aparezca en partidas. Devuelve False si no existe."""
        pregunta = self.session.get(Pregunta, pregunta_id)
        if pregunta is None:
            return False
        pregunta.activa = False
        self.session.commit()
        return True

    def existe_enunciado(self, enunciado: str, excluir_id: int | None = None) -> bool:
        """Verifica si ya existe una pregunta con ese enunciado, excluyendo opcionalmente un id."""
        statement = select(Pregunta).where(Pregunta.enunciado == enunciado)
        if excluir_id is not None:
            statement = statement.where(Pregunta.id != excluir_id)
        return self.session.exec(statement).first() is not None
