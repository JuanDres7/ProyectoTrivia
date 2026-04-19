from app.database.models.contenido import Opcion, Pregunta
from app.database.models.partidas import Jugador, Partida


class SesionPartida:
    """Encapsula el estado de una partida en curso: pregunta actual, avance e índice de correctas."""

    def __init__(self, jugador: Jugador, partida: Partida,
                 preguntas: list[tuple[Pregunta, list[Opcion]]]):
        self.jugador = jugador
        self.partida = partida
        self._preguntas = preguntas
        self._indice = 0
        self._correctas = 0

    @property
    def numero_actual(self) -> int:
        """Número de la pregunta actual (empieza en 1)."""
        return self._indice + 1

    @property
    def total_preguntas(self) -> int:
        """Total de preguntas de la partida."""
        return len(self._preguntas)

    @property
    def correctas(self) -> int:
        """Cantidad de respuestas correctas acumuladas hasta ahora."""
        return self._correctas

    def pregunta_actual(self) -> tuple[Pregunta, list[Opcion]]:
        """Devuelve la pregunta y sus opciones correspondientes al turno actual."""
        return self._preguntas[self._indice]

    def hay_siguiente(self) -> bool:
        """Indica si todavía quedan preguntas por responder."""
        return self._indice < len(self._preguntas) - 1

    def avanzar(self) -> None:
        """Pasa a la siguiente pregunta."""
        self._indice += 1

    def registrar_correcta(self) -> None:
        """Suma una respuesta correcta al contador interno."""
        self._correctas += 1
