from app.repository.contenido_repository import ContenidoRepository
from app.database.models.contenido import Categoria, NivelDificultad, Opcion, Pregunta


class ContenidoService:

    def __init__(self, contenido_repository: ContenidoRepository):
        self.repo = contenido_repository

    # ------------------------------------------------------------------ #
    # Categorias                                                           #
    # ------------------------------------------------------------------ #

    def crear_categoria(self, nombre: str, descripcion: str | None = None) -> Categoria:
        """Crea una nueva categoría validando que el nombre no esté vacío."""
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        return self.repo.crear_categoria(nombre, descripcion)

    def listar_categorias(self, solo_activas: bool = True) -> list[Categoria]:
        """Devuelve todas las categorías, por defecto solo las activas."""
        return self.repo.obtener_categorias(solo_activas)

    def actualizar_categoria(self, categoria_id: int, nombre: str,
                             descripcion: str | None = None) -> Categoria:
        """Actualiza el nombre y descripción de una categoría existente."""
        nombre = nombre.strip()
        if not nombre:
            raise ValueError("El nombre de la categoría no puede estar vacío.")
        categoria = self.repo.actualizar_categoria(categoria_id, nombre, descripcion)
        if categoria is None:
            raise ValueError(f"No existe la categoría con id {categoria_id}.")
        return categoria

    def eliminar_categoria(self, categoria_id: int) -> None:
        """Desactiva una categoría para que no aparezca en el juego."""
        if not self.repo.desactivar_categoria(categoria_id):
            raise ValueError(f"No existe la categoría con id {categoria_id}.")

    # ------------------------------------------------------------------ #
    # Niveles                                                              #
    # ------------------------------------------------------------------ #

    def listar_niveles(self) -> list[NivelDificultad]:
        """Devuelve todos los niveles de dificultad disponibles."""
        return self.repo.obtener_niveles()

    def obtener_nivel(self, nivel_id: int) -> NivelDificultad:
        """Devuelve un nivel por su id o lanza ValueError si no existe."""
        nivel = self.repo.obtener_nivel_por_id(nivel_id)
        if nivel is None:
            raise ValueError(f"No existe el nivel con id {nivel_id}.")
        return nivel

    # ------------------------------------------------------------------ #
    # Preguntas                                                            #
    # ------------------------------------------------------------------ #

    def crear_pregunta(self, enunciado: str, nivel_id: int, opciones: list[dict],
                       categoria_id: int | None = None) -> Pregunta:
        """Valida y crea una nueva pregunta con sus cuatro opciones de respuesta."""
        self._validar_pregunta(enunciado, opciones)
        if self.repo.existe_enunciado(enunciado):
            raise ValueError("Ya existe una pregunta con ese enunciado.")
        return self.repo.crear_pregunta(enunciado, nivel_id, opciones, categoria_id)

    def listar_preguntas(self, nivel_id: int | None = None) -> list[Pregunta]:
        """Devuelve todas las preguntas, opcionalmente filtradas por nivel."""
        return self.repo.obtener_preguntas(nivel_id)

    def obtener_pregunta_con_opciones(self, pregunta_id: int) -> tuple[Pregunta, list[Opcion]]:
        """Devuelve una pregunta junto con su lista de opciones de respuesta."""
        pregunta = self.repo.obtener_pregunta_por_id(pregunta_id)
        if pregunta is None:
            raise ValueError(f"No existe la pregunta con id {pregunta_id}.")
        opciones = self.repo.obtener_opciones_de_pregunta(pregunta_id)
        return pregunta, opciones

    def actualizar_pregunta(self, pregunta_id: int, enunciado: str, nivel_id: int,
                            opciones: list[dict], categoria_id: int | None = None) -> Pregunta:
        """Actualiza el enunciado, nivel, categoría y opciones de una pregunta existente."""
        self._validar_pregunta(enunciado, opciones)
        if self.repo.existe_enunciado(enunciado, excluir_id=pregunta_id):
            raise ValueError("Ya existe otra pregunta con ese enunciado.")
        pregunta = self.repo.actualizar_pregunta(pregunta_id, enunciado, nivel_id, opciones, categoria_id)
        if pregunta is None:
            raise ValueError(f"No existe la pregunta con id {pregunta_id}.")
        return pregunta

    def eliminar_pregunta(self, pregunta_id: int) -> None:
        """Desactiva una pregunta para que no aparezca en las partidas."""
        if not self.repo.desactivar_pregunta(pregunta_id):
            raise ValueError(f"No existe la pregunta con id {pregunta_id}.")

    # ------------------------------------------------------------------ #
    # Validaciones internas                                                #
    # ------------------------------------------------------------------ #

    def _validar_pregunta(self, enunciado: str, opciones: list[dict]) -> None:
        """Verifica que el enunciado no esté vacío y que haya exactamente una opción correcta."""
        if not enunciado.strip():
            raise ValueError("El enunciado no puede estar vacío.")
        if len(opciones) != 4:
            raise ValueError("La pregunta debe tener exactamente 4 opciones.")
        correctas = sum(1 for op in opciones if op.get("es_correcta"))
        if correctas != 1:
            raise ValueError("Exactamente una opción debe ser la correcta.")
