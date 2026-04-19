import customtkinter as ctk
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_FONDO_FRAME, COLOR_TEXTO, COLOR_ERROR,
    FUENTE_TITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class IngresoJugadorFrame(ctk.CTkFrame):

    def __init__(self, master, on_continuar, on_volver):
        super().__init__(master, fg_color=COLOR_FONDO_FRAME, corner_radius=16)
        self.on_continuar = on_continuar
        self.on_volver = on_volver
        self._construir_ui()

    def _construir_ui(self):
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="¡Bienvenido!", font=FUENTE_TITULO,
                     text_color=COLOR_TEXTO).grid(row=0, column=0, pady=(40, 4))
        ctk.CTkLabel(self, text="Ingresa tu nombre para comenzar", font=FUENTE_PEQUEÑA,
                     text_color="#aaaaaa").grid(row=1, column=0, pady=(0, 24))

        self._entry_nombre = ctk.CTkEntry(self, placeholder_text="Tu nombre", width=300,
                                           font=FUENTE_NORMAL)
        self._entry_nombre.grid(row=2, column=0, pady=8)
        self._entry_nombre.bind("<Return>", lambda e: self._continuar())

        self._lbl_error = ctk.CTkLabel(self, text="", font=FUENTE_PEQUEÑA,
                                        text_color=COLOR_ERROR)
        self._lbl_error.grid(row=3, column=0, pady=(4, 0))

        ctk.CTkButton(self, text="Continuar →", width=300, font=FUENTE_NORMAL,
                      fg_color=COLOR_PRIMARIO, command=self._continuar).grid(row=4, column=0, pady=(12, 8))

        ctk.CTkButton(self, text="← Volver", width=300, font=FUENTE_NORMAL,
                      fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
                      command=self.on_volver).grid(row=5, column=0, pady=(0, 30))

    def _continuar(self):
        nombre = self._entry_nombre.get().strip()
        if not nombre:
            self._lbl_error.configure(text="Por favor ingresa tu nombre.")
            return
        if len(nombre) > 100:
            self._lbl_error.configure(text="El nombre no puede superar 100 caracteres.")
            return
        self.on_continuar(nombre)
