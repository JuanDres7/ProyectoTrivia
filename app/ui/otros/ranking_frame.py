import customtkinter as ctk
from app.database.models.partidas import Ranking
from app.config.settings import (
    COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_DORADO, COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_TITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA, FUENTE_BADGE,
)


class RankingFrame(ctk.CTkFrame):

    def __init__(self, master, top10: list[tuple[Ranking, str]], on_volver):
        """Inicializa el frame con la lista de los 10 mejores puntajes."""
        super().__init__(
            master,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDE,
        )
        self.top10 = top10
        self.on_volver = on_volver
        self._card_frame = True
        self._construir_ui()

    def _construir_ui(self):
        """Construye la tabla personalizada con posición, nombre y puntaje de cada jugador."""
        self.columnconfigure(0, weight=1, minsize=460)

        ctk.CTkLabel(
            self, text="TOP 10 JUGADORES",
            font=FUENTE_TITULO, text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, pady=(32, 4))

        ctk.CTkLabel(
            self, text="Mejores puntajes de todos los tiempos",
            font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
        ).grid(row=1, column=0, pady=(0, 20))

        tabla = ctk.CTkFrame(self, fg_color="transparent")
        tabla.grid(row=2, column=0, padx=28, pady=(0, 12), sticky="ew")

        self._construir_tabla(tabla)

        ctk.CTkButton(
            self,
            text="← Volver al menú",
            width=240, height=46, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            command=self.on_volver,
        ).grid(row=3, column=0, pady=(4, 32))

    def _construir_tabla(self, parent: ctk.CTkFrame):
        """Construye la cabecera y las filas de datos o el estado vacío."""
        # Cabecera
        header = ctk.CTkFrame(parent, fg_color=COLOR_PRIMARIO, corner_radius=8, height=36)
        header.pack(fill="x", pady=(0, 4))
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="#", width=38,
            font=FUENTE_BADGE, text_color="#080812",
        ).pack(side="left", padx=6)
        ctk.CTkLabel(
            header, text="Nombre",
            font=FUENTE_BADGE, text_color="#080812", anchor="w",
        ).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            header, text="Puntos", width=72,
            font=FUENTE_BADGE, text_color="#080812",
        ).pack(side="right", padx=8)

        if not self.top10:
            vacio = ctk.CTkFrame(parent, fg_color=COLOR_SUPERFICIE, corner_radius=8, height=200)
            vacio.pack(fill="x")
            vacio.pack_propagate(False)
            ctk.CTkLabel(
                vacio, text="🏆",
                font=("Segoe UI", 32), text_color=COLOR_BORDE,
            ).pack(expand=True)
            ctk.CTkLabel(
                vacio, text="Aún no hay partidas registradas",
                font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
            ).pack(pady=(0, 20))
            return

        for pos, entrada in enumerate(self.top10, start=1):
            es_primero = pos == 1
            fondo = "#181408" if es_primero else (COLOR_SUPERFICIE if pos % 2 == 0 else COLOR_FONDO_FRAME)
            color_txt = COLOR_DORADO if es_primero else COLOR_TEXTO
            color_pts = COLOR_DORADO if es_primero else COLOR_PRIMARIO

            fila = ctk.CTkFrame(parent, fg_color=fondo, corner_radius=6, height=34)
            fila.pack(fill="x", pady=1)
            fila.pack_propagate(False)

            pos_bg = COLOR_DORADO if es_primero else COLOR_BORDE
            pos_fg = "#080812" if es_primero else COLOR_TEXTO_SEC
            ctk.CTkLabel(
                fila, text=str(pos), width=34,
                font=FUENTE_BADGE, fg_color=pos_bg,
                text_color=pos_fg, corner_radius=4,
            ).pack(side="left", padx=6, pady=4)

            nombre = (entrada.nombre[:24] + "…") if len(entrada.nombre) > 24 else entrada.nombre
            ctk.CTkLabel(
                fila, text=nombre,
                font=FUENTE_PEQUEÑA, text_color=color_txt, anchor="w",
            ).pack(side="left", fill="x", expand=True, padx=6)

            ctk.CTkLabel(
                fila, text=str(entrada.puntaje), width=66,
                font=FUENTE_BADGE, text_color=color_pts, anchor="e",
            ).pack(side="right", padx=8)
