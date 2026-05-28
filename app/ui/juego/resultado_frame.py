import customtkinter as ctk
from app.database.models.partidas import Ranking
from app.config.settings import (
    COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_EXITO, COLOR_ERROR, COLOR_DORADO,
    COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
    FUENTE_PUNTAJE, FUENTE_BADGE,
)


class ResultadoFrame(ctk.CTkFrame):

    def __init__(self, master, nombre_jugador: str, puntaje: int,
                 es_record: bool, record_anterior: int,
                 top10: list[Ranking], on_volver):
        """Inicializa la pantalla de resultado con el puntaje y el estado de récord."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0)
        self.nombre_jugador = nombre_jugador
        self.puntaje = puntaje
        self.es_record = es_record
        self.record_anterior = record_anterior
        self.top10 = top10
        self.on_volver = on_volver
        self._construir_ui()

    def _construir_ui(self):
        """Construye el panel de resultado del jugador y la tabla Top 10."""

        # ── Panel izquierdo — resultado personal ──────────────────────
        left = ctk.CTkFrame(
            self,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDE,
            width=360,
        )
        left.pack(side="left", fill="y", padx=(20, 10), pady=20)
        left.pack_propagate(False)
        left.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            left, text="TU RESULTADO",
            font=FUENTE_PEQUEÑA,
            text_color=COLOR_TEXTO_SEC,
        ).grid(row=0, column=0, pady=(30, 2))

        ctk.CTkLabel(
            left, text=self.nombre_jugador,
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO,
        ).grid(row=1, column=0, pady=(0, 18))

        # Puntaje con animación de conteo
        color_puntaje = COLOR_DORADO if self.es_record else COLOR_PRIMARIO
        self._lbl_puntaje = ctk.CTkLabel(
            left, text="0",
            font=FUENTE_PUNTAJE,
            text_color=color_puntaje,
        )
        self._lbl_puntaje.grid(row=2, column=0)

        ctk.CTkLabel(
            left, text="puntos",
            font=FUENTE_NORMAL,
            text_color=COLOR_TEXTO_SEC,
        ).grid(row=3, column=0, pady=(0, 16))

        # Badge de récord o mensaje de resultado
        if self.es_record:
            badge = ctk.CTkFrame(
                left,
                fg_color="#1a1508",
                corner_radius=8,
                border_width=1,
                border_color=COLOR_DORADO,
            )
            badge.grid(row=4, column=0, padx=24, pady=6, sticky="ew")
            ctk.CTkLabel(
                badge, text="⭐  ¡NUEVO RÉCORD!",
                font=FUENTE_BADGE,
                text_color=COLOR_DORADO,
            ).pack(pady=10)
        else:
            ctk.CTkLabel(
                left, text="No superaste el récord actual",
                font=FUENTE_PEQUEÑA,
                text_color=COLOR_ERROR,
            ).grid(row=4, column=0, pady=(0, 2))
            ctk.CTkLabel(
                left,
                text=f"Récord actual: {self.record_anterior} pts",
                font=FUENTE_PEQUEÑA,
                text_color=COLOR_TEXTO_SEC,
            ).grid(row=5, column=0, pady=(0, 8))

        ctk.CTkButton(
            left, text="← Volver al menú",
            width=260, height=46, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            command=self.on_volver,
        ).grid(row=6, column=0, pady=(20, 30))

        # ── Panel derecho — Top 10 ─────────────────────────────────────
        right = ctk.CTkFrame(
            self,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDE,
        )
        right.pack(side="left", fill="both", expand=True, padx=(10, 20), pady=20)

        ctk.CTkLabel(
            right, text="TOP 10 JUGADORES",
            font=FUENTE_SUBTITULO,
            text_color=COLOR_TEXTO,
        ).pack(pady=(20, 14))

        self._construir_tabla_top10(right)

        # Inicia la animación del puntaje tras renderizar
        self.after(120, self._animar_puntaje)

    def _construir_tabla_top10(self, parent: ctk.CTkFrame):
        """Construye la tabla de Top 10 con filas CTk en lugar de ttk.Treeview."""
        tabla = ctk.CTkFrame(parent, fg_color="transparent")
        tabla.pack(fill="x", padx=16)
        tabla.columnconfigure(1, weight=1)

        # Cabecera
        header = ctk.CTkFrame(tabla, fg_color=COLOR_PRIMARIO, corner_radius=8, height=34)
        header.pack(fill="x", pady=(0, 4))
        header.pack_propagate(False)
        header.columnconfigure(1, weight=1)
        ctk.CTkLabel(header, text="#", width=38, font=FUENTE_BADGE,
                     text_color="#080812").pack(side="left", padx=6)
        ctk.CTkLabel(header, text="Nombre", font=FUENTE_BADGE,
                     text_color="#080812", anchor="w").pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(header, text="Puntos", width=70, font=FUENTE_BADGE,
                     text_color="#080812").pack(side="right", padx=8)

        # Filas de datos
        for pos, entrada in enumerate(self.top10, start=1):
            es_primero = pos == 1
            fondo = "#181408" if es_primero else (COLOR_SUPERFICIE if pos % 2 == 0 else COLOR_FONDO_FRAME)
            color_txt = COLOR_DORADO if es_primero else COLOR_TEXTO
            color_pts = COLOR_DORADO if es_primero else COLOR_PRIMARIO

            fila = ctk.CTkFrame(tabla, fg_color=fondo, corner_radius=6, height=32)
            fila.pack(fill="x", pady=1)
            fila.pack_propagate(False)

            pos_bg = COLOR_DORADO if es_primero else COLOR_BORDE
            pos_fg = "#080812" if es_primero else COLOR_TEXTO_SEC
            ctk.CTkLabel(
                fila, text=str(pos), width=34,
                font=FUENTE_BADGE, fg_color=pos_bg,
                text_color=pos_fg, corner_radius=4,
            ).pack(side="left", padx=6, pady=4)

            nombre_cortado = (entrada.nombre[:22] + "…") if len(entrada.nombre) > 22 else entrada.nombre
            ctk.CTkLabel(
                fila, text=nombre_cortado,
                font=FUENTE_PEQUEÑA, text_color=color_txt, anchor="w",
            ).pack(side="left", fill="x", expand=True, padx=6)

            ctk.CTkLabel(
                fila, text=str(entrada.puntaje), width=66,
                font=FUENTE_BADGE, text_color=color_pts, anchor="e",
            ).pack(side="right", padx=8)

    # ------------------------------------------------------------------
    # Animación del puntaje
    # ------------------------------------------------------------------

    def _animar_puntaje(self, actual: int = 0):
        """Anima el puntaje contando desde 0 hasta el valor final."""
        paso = max(1, self.puntaje // 40)
        actual = min(actual + paso, self.puntaje)
        self._lbl_puntaje.configure(text=str(actual))
        if actual < self.puntaje:
            self.after(25, lambda: self._animar_puntaje(actual))