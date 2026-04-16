from sqlmodel import Session, select, col
from app.database.models.contenido import Categoria, NivelDificultad, Opcion, Pregunta


class ContenidoRepository:

    def __init__(self, session: Session):
        self.session = session

    # ------------------------------------------------------------------ #
    # Categorias                                                           #
    # ------------------------------------------------------------------ #

    def crear_categoria(self, nombre: str, descripcion: str | None = None) -> Categoria:
        categoria = Categoria(nombre=nombre, descripcion=descripcion)
        self.session.add(categoria)
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def obtener_categorias(self, solo_activas: bool = True) -> list[Categoria]:
        statement = select(Categoria)
        if solo_activas:
            statement = statement.where(Categoria.activa == True)
        return list(self.session.exec(statement).all())

    def obtener_categoria_por_id(self, categoria_id: int) -> Categoria | None:
        return self.session.get(Categoria, categoria_id)

    def actualizar_categoria(self, categoria_id: int, nombre: str, descripcion: str | None) -> Categoria | None:
        categoria = self.session.get(Categoria, categoria_id)
        if categoria is None:
            return None
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        self.session.commit()
        self.session.refresh(categoria)
        return categoria

    def desactivar_categoria(self, categoria_id: int) -> bool:
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
        return list(self.session.exec(select(NivelDificultad)).all())

    def obtener_nivel_por_id(self, nivel_id: int) -> NivelDificultad | None:
        return self.session.get(NivelDificultad, nivel_id)

    # ------------------------------------------------------------------ #
    # Preguntas                                                            #
    # ------------------------------------------------------------------ #

    def crear_pregunta(self, enunciado: str, nivel_id: int, opciones: list[dict],
                       categoria_id: int | None = None) -> Pregunta:
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
        statement = select(Pregunta)
        if solo_activas:
            statement = statement.where(Pregunta.activa == True)
        if nivel_id is not None:
            statement = statement.where(Pregunta.nivel_id == nivel_id)
        if categoria_ids is not None:
            statement = statement.where(col(Pregunta.categoria_id).in_(categoria_ids))
        return list(self.session.exec(statement).all())

    def obtener_pregunta_por_id(self, pregunta_id: int) -> Pregunta | None:
        return self.session.get(Pregunta, pregunta_id)

    def obtener_opciones_de_pregunta(self, pregunta_id: int) -> list[Opcion]:
        statement = select(Opcion).where(Opcion.pregunta_id == pregunta_id)
        return list(self.session.exec(statement).all())

    def actualizar_pregunta(self, pregunta_id: int, enunciado: str, nivel_id: int,
                            opciones: list[dict], categoria_id: int | None = None) -> Pregunta | None:
        pregunta = self.session.get(Pregunta, pregunta_id)
        if pregunta is None:
            return None

        pregunta.enunciado = enunciado
        pregunta.nivel_id = nivel_id
        pregunta.categoria_id = categoria_id

        # Eliminar opciones viejas y recrear
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
        pregunta = self.session.get(Pregunta, pregunta_id)
        if pregunta is None:
            return False
        pregunta.activa = False
        self.session.commit()
        return True

    def existe_enunciado(self, enunciado: str, excluir_id: int | None = None) -> bool:
        statement = select(Pregunta).where(Pregunta.enunciado == enunciado)
        if excluir_id is not None:
            statement = statement.where(Pregunta.id != excluir_id)
        return self.session.exec(statement).first() is not None
