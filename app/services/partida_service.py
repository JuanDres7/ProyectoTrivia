import random
from app.repository.partida_repository import PartidaRepository
from app.repository.contenido_repository import ContenidoRepository
from app.database.models.contenido import NivelDificultad, Opcion, Pregunta
from app.database.models.partidas import Jugador, Partida, Ranking


class PartidaService:

    def __init__(self, partida_repository: PartidaRepository,
                 contenido_repository: ContenidoRepository):
        self.partida_repo = partida_repository
        self.contenido_repo = contenido_repository

    def iniciar_partida(self, nombre_jugador: str, nivel_id: int,
                        categoria_ids: list[int] | None = None) -> tuple[Jugador, Partida, list[tuple[Pregunta, list[Opcion]]]]:
        nivel = self.contenido_repo.obtener_nivel_por_id(nivel_id)
        if nivel is None:
            raise ValueError(f"No existe el nivel con id {nivel_id}.")

        jugador = self.partida_repo.obtener_o_crear_jugador(nombre_jugador.strip())
        partida = self.partida_repo.crear_partida(jugador.id, nivel_id, nivel.num_preguntas)

        preguntas = self.contenido_repo.obtener_preguntas(nivel_id=nivel_id, categoria_ids=categoria_ids)
        if len(preguntas) < nivel.num_preguntas:
            raise ValueError(
                f"No hay suficientes preguntas para el nivel '{nivel.nombre}'. "
                f"Se necesitan {nivel.num_preguntas}, hay {len(preguntas)}."
            )

        seleccionadas = random.sample(preguntas, nivel.num_preguntas)
        preguntas_con_opciones = []
        for pregunta in seleccionadas:
            opciones = self.contenido_repo.obtener_opciones_de_pregunta(pregunta.id)
            random.shuffle(opciones)
            preguntas_con_opciones.append((pregunta, opciones))

        return jugador, partida, preguntas_con_opciones

    # ------------------------------------------------------------------ #
    # Responder pregunta                                                   #
    # ------------------------------------------------------------------ #

    def responder_pregunta(self, partida_id: int, pregunta_id: int,
                           opcion_elegida_id: int) -> bool:
        """Registra la respuesta y devuelve True si es correcta."""
        opciones = self.contenido_repo.obtener_opciones_de_pregunta(pregunta_id)
        opcion = next((op for op in opciones if op.id == opcion_elegida_id), None)
        if opcion is None:
            raise ValueError("La opción elegida no pertenece a esa pregunta.")

        es_correcta = opcion.es_correcta
        self.partida_repo.registrar_respuesta(partida_id, pregunta_id, opcion_elegida_id, es_correcta)
        return es_correcta

    # ------------------------------------------------------------------ #
    # Finalizar partida                                                    #
    # ------------------------------------------------------------------ #

    def finalizar_partida(self, partida_id: int, jugador_id: int, nombre_jugador: str,
                          nivel_id: int, respuestas_correctas: int) -> dict:
        """
        Cierra la partida, actualiza el contador del jugador, registra en
        el ranking y verifica si es nuevo récord global.

        Retorna un dict con: puntaje_final, es_record_global, record_anterior.
        """
        puntaje_final = respuestas_correctas  # 1 punto por respuesta correcta

        self.partida_repo.finalizar_partida(partida_id, respuestas_correctas, puntaje_final)
        self.partida_repo.incrementar_total_partidas(jugador_id)

        record_anterior = self.partida_repo.obtener_record_global()
        entrada = self.partida_repo.registrar_en_ranking(jugador_id, nombre_jugador, nivel_id, puntaje_final)

        es_record_global = puntaje_final > record_anterior
        if es_record_global:
            self.partida_repo.marcar_record_global(entrada.id)

        return {
            "puntaje_final": puntaje_final,
            "es_record_global": es_record_global,
            "record_anterior": record_anterior,
        }

    # ------------------------------------------------------------------ #
    # Cancelar partida                                                     #
    # ------------------------------------------------------------------ #

    def cancelar_partida(self, partida_id: int) -> None:
        self.partida_repo.actualizar_estado_partida(partida_id, "cancelada")

    # ------------------------------------------------------------------ #
    # Consultas                                                            #
    # ------------------------------------------------------------------ #

    def obtener_top10(self) -> list[Ranking]:
        return self.partida_repo.obtener_top10()

    def obtener_historial_jugador(self, jugador_id: int) -> list[Partida]:
        return self.partida_repo.obtener_historial_jugador(jugador_id)

    def obtener_nivel(self, nivel_id: int) -> NivelDificultad | None:
        return self.contenido_repo.obtener_nivel_por_id(nivel_id)
