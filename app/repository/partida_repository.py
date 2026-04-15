from sqlmodel import Session, select
from app.database.models.partidas import Jugador, Partida, Ranking, Respuesta


class PartidaRepository:

    def __init__(self, session: Session):
        self.session = session

    # ------------------------------------------------------------------ #
    # Jugadores                                                            #
    # ------------------------------------------------------------------ #

    def obtener_o_crear_jugador(self, nombre: str) -> Jugador:
        jugador = self.session.exec(
            select(Jugador).where(Jugador.nombre == nombre)
        ).first()
        if jugador is None:
            jugador = Jugador(nombre=nombre)
            self.session.add(jugador)
            self.session.commit()
            self.session.refresh(jugador)
        return jugador

    def incrementar_total_partidas(self, jugador_id: int) -> None:
        jugador = self.session.get(Jugador, jugador_id)
        if jugador:
            jugador.total_partidas += 1
            self.session.commit()

    # ------------------------------------------------------------------ #
    # Partidas                                                             #
    # ------------------------------------------------------------------ #

    def crear_partida(self, jugador_id: int, nivel_id: int, total_preguntas: int) -> Partida:
        partida = Partida(
            jugador_id=jugador_id,
            nivel_id=nivel_id,
            total_preguntas=total_preguntas,
            estado="en_curso",
        )
        self.session.add(partida)
        self.session.commit()
        self.session.refresh(partida)
        return partida

    def actualizar_estado_partida(self, partida_id: int, estado: str) -> None:
        partida = self.session.get(Partida, partida_id)
        if partida:
            partida.estado = estado
            self.session.commit()

    def finalizar_partida(self, partida_id: int, respuestas_correctas: int, puntaje_final: int) -> None:
        partida = self.session.get(Partida, partida_id)
        if partida:
            partida.respuestas_correctas = respuestas_correctas
            partida.puntaje_final = puntaje_final
            partida.estado = "finalizada"
            self.session.commit()

    # ------------------------------------------------------------------ #
    # Respuestas                                                           #
    # ------------------------------------------------------------------ #

    def registrar_respuesta(self, partida_id: int, pregunta_id: int,
                            opcion_elegida_id: int, es_correcta: bool) -> Respuesta:
        respuesta = Respuesta(
            partida_id=partida_id,
            pregunta_id=pregunta_id,
            opcion_elegida_id=opcion_elegida_id,
            es_correcta=es_correcta,
            puntos_obtenidos=1 if es_correcta else 0,
        )
        self.session.add(respuesta)
        self.session.commit()
        return respuesta

    # ------------------------------------------------------------------ #
    # Ranking                                                              #
    # ------------------------------------------------------------------ #

    def registrar_en_ranking(self, jugador_id: int, nivel_id: int, puntaje: int) -> Ranking:
        entrada = Ranking(jugador_id=jugador_id, nivel_id=nivel_id, puntaje=puntaje)
        self.session.add(entrada)
        self.session.commit()
        self.session.refresh(entrada)
        return entrada

    def obtener_record_global(self) -> int:
        """Devuelve el puntaje más alto de toda la historia, en cualquier nivel."""
        resultados = self.session.exec(select(Ranking)).all()
        if not resultados:
            return 0
        return max(r.puntaje for r in resultados)

    def marcar_record_global(self, ranking_id: int) -> None:
        # Quita el flag anterior
        anteriores = self.session.exec(
            select(Ranking).where(Ranking.es_record_global == True)
        ).all()
        for r in anteriores:
            r.es_record_global = False

        nuevo = self.session.get(Ranking, ranking_id)
        if nuevo:
            nuevo.es_record_global = True

        self.session.commit()

    def obtener_top10(self) -> list[Ranking]:
        statement = select(Ranking).order_by(Ranking.puntaje.desc()).limit(10)  # type: ignore[attr-defined]
        return list(self.session.exec(statement).all())

    def obtener_historial_jugador(self, jugador_id: int) -> list[Partida]:
        statement = select(Partida).where(Partida.jugador_id == jugador_id)
        return list(self.session.exec(statement).all())
