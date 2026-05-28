import customtkinter as ctk
from app.config.settings import (
    COLOR_FONDO, COLOR_SUPERFICIE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_SECUNDARIO,
    COLOR_BORDE, COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class MenuFrame(ctk.CTkFrame):

    def __init__(self, master, on_gestionar_preguntas, on_iniciar_juego, on_mostrar_ranking):
        """Inicializa el menú principal con los tres callbacks de navegación."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0)
        self.on_gestionar_preguntas = on_gestionar_preguntas
        self.on_iniciar_juego = on_iniciar_juego
        self.on_mostrar_ranking = on_mostrar_ranking
        self._construir_ui()

    def _construir_ui(self):
        """Construye la pantalla de menú principal con estilo Neon Quiz."""
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=3)
        self.rowconfigure(7, weight=2)

        ctk.CTkLabel(
            self, text="⚡",
            font=("Segoe UI", 52),
            text_color=COLOR_PRIMARIO,
        ).grid(row=1, column=0, pady=(0, 2))

        ctk.CTkLabel(
            self, text="SAPIENTIA",
            font=("Segoe UI", 44, "bold"),
            text_color=COLOR_TEXTO,
        ).grid(row=2, column=0, pady=(0, 6))

        ctk.CTkLabel(
            self, text="El desafío del conocimiento",
            font=FUENTE_PEQUEÑA,
            text_color=COLOR_TEXTO_SEC,
        ).grid(row=3, column=0, pady=(0, 36))

        self._btn_jugar = ctk.CTkButton(
            self,
            text="▶   INICIAR JUEGO",
            width=300, height=52, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            command=self.on_iniciar_juego,
        )
        self._btn_jugar.grid(row=4, column=0, pady=7)

        self._btn_ranking = ctk.CTkButton(
            self,
            text="◆   VER RANKING",
            width=300, height=52, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color="transparent",
            border_width=2,
            border_color=COLOR_SECUNDARIO,
            text_color=COLOR_SECUNDARIO,
            hover_color="#1a0520",
            command=self.on_mostrar_ranking,
        )
        self._btn_ranking.grid(row=5, column=0, pady=7)

        self._btn_admin = ctk.CTkButton(
            self,
            text="⚙   ADMINISTRAR",
            width=300, height=44, corner_radius=10,
            font=FUENTE_PEQUEÑA,
            fg_color="transparent",
            border_width=1,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO_SEC,
            hover_color=COLOR_SUPERFICIE,
            command=self.on_gestionar_preguntas,
        )
        self._btn_admin.grid(row=6, column=0, pady=(7, 0))

        self.after(60, self._animar_entrada)

    # ------------------------------------------------------------------
    # Animación de entrada
    # ------------------------------------------------------------------

    def _animar_entrada(self):
        """Inicia el slide-up escalonado de los tres botones al aparecer el menú."""
        for btn in (self._btn_jugar, self._btn_ranking, self._btn_admin):
            btn.grid_configure(pady=(67, 7))
        self._slide_btn(self._btn_jugar, 60, 0)
        self.after(100, lambda: self._slide_btn(self._btn_ranking, 60, 0))
        self.after(200, lambda: self._slide_btn(self._btn_admin, 60, 0))

    def _slide_btn(self, btn: ctk.CTkButton, start_offset: int, step: int):
        """Anima el deslizamiento vertical de un botón desde abajo hasta su posición natural."""
        MAX = 10
        if step > MAX:
            btn.grid_configure(pady=7)
            return
        t = step / MAX
        ease = 1 - (1 - t) ** 3
        offset = int(start_offset * (1 - ease))
        btn.grid_configure(pady=(offset + 7, 7))
        self.after(25, lambda: self._slide_btn(btn, start_offset, step + 1))
