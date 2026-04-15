import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_FONDO_FRAME, COLOR_TEXTO,
    FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class SeleccionNivelFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService,
                 nombre_jugador: str, on_nivel_elegido, on_volver):
        super().__init__(master, fg_color=COLOR_FONDO_FRAME, corner_radius=16)
        self.contenido_service = contenido_service
        self.nombre_jugador = nombre_jugador
        self.on_nivel_elegido = on_nivel_elegido
        self.on_volver = on_volver
        self._construir_ui()

    def _construir_ui(self):
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text=f"Hola, {self.nombre_jugador}!", font=FUENTE_TITULO,
                     text_color=COLOR_TEXTO).grid(row=0, column=0, pady=(36, 4))
        ctk.CTkLabel(self, text="Elige un nivel de dificultad", font=FUENTE_PEQUEÑA,
                     text_color="#aaaaaa").grid(row=1, column=0, pady=(0, 20))

        niveles = self.contenido_service.listar_niveles()
        colores = [COLOR_EXITO := "#2ecc71", COLOR_PRIMARIO, "#e67e22"]

        for i, nivel in enumerate(niveles):
            btn_frame = ctk.CTkFrame(self, fg_color="#333333", corner_radius=10, width=340)
            btn_frame.grid(row=2 + i, column=0, pady=6, padx=30)
            btn_frame.columnconfigure(0, weight=1)

            ctk.CTkLabel(btn_frame, text=nivel.nombre, font=FUENTE_SUBTITULO,
                         text_color=COLOR_TEXTO).grid(row=0, column=0, pady=(10, 2))
            ctk.CTkLabel(
                btn_frame,
                text=f"{nivel.num_preguntas} preguntas  ·  {nivel.tiempo_limite_seg} seg / pregunta",
                font=FUENTE_PEQUEÑA, text_color="#aaaaaa",
            ).grid(row=1, column=0, pady=(0, 10))

            nivel_id = nivel.id
            ctk.CTkButton(
                btn_frame, text="Jugar", width=140, font=FUENTE_NORMAL,
                fg_color=colores[i % len(colores)], text_color="#000000",
                command=lambda nid=nivel_id: self.on_nivel_elegido(self.nombre_jugador, nid),
            ).grid(row=2, column=0, pady=(0, 12))

        ctk.CTkButton(self, text="← Volver", width=200, font=FUENTE_NORMAL,
                      fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
                      command=self.on_volver).grid(row=2 + len(niveles), column=0, pady=(16, 24))
