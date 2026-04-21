import customtkinter as ctk
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_FONDO_FRAME, COLOR_TEXTO,
    FUENTE_TITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA
)


class MenuFrame(ctk.CTkFrame):

    def __init__(self, master, on_gestionar_preguntas, on_iniciar_juego, on_mostrar_ranking):
        """Inicializa el menú principal con los tres callbacks de navegación."""
        super().__init__(master, fg_color=COLOR_FONDO_FRAME, corner_radius=16, width=400, height=300)
        self.grid_propagate(False)
        self.on_gestionar_preguntas = on_gestionar_preguntas
        self.on_iniciar_juego = on_iniciar_juego
        self.on_mostrar_ranking = on_mostrar_ranking
        self._construir_ui()

    def _construir_ui(self):
        """Construye los tres botones de acceso: jugar, ranking y gestionar preguntas."""
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Sistema de Trivia", font=FUENTE_TITULO, text_color=COLOR_TEXTO).grid(
            row=0, column=0, pady=(40, 8)
        )
        ctk.CTkLabel(self, text="¿Qué deseas hacer?", font=FUENTE_PEQUEÑA, text_color="#aaaaaa").grid(
            row=1, column=0, pady=(0, 30)
        )

        ctk.CTkButton(
            self, text="Iniciar Juego", width=220, font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO, command=self.on_iniciar_juego
        ).grid(row=2, column=0, pady=10)

        ctk.CTkButton(
            self, text="Ver Ranking", width=220, font=FUENTE_NORMAL,
            fg_color=COLOR_SECUNDARIO, text_color=COLOR_TEXTO,
            command=self.on_mostrar_ranking
        ).grid(row=3, column=0, pady=10)

        ctk.CTkButton(
            self, text="Gestionar Preguntas", width=220, font=FUENTE_NORMAL,
            fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
            command=self.on_gestionar_preguntas
        ).grid(row=4, column=0, pady=(10, 40))
