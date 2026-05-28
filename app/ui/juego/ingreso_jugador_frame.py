import customtkinter as ctk
from app.config.settings import (
    COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_TEXTO, COLOR_TEXTO_SEC, COLOR_ERROR,
    FUENTE_TITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class IngresoJugadorFrame(ctk.CTkFrame):

    def __init__(self, master, on_continuar, on_volver):
        """Inicializa el formulario de ingreso del nombre del jugador."""
        super().__init__(
            master,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDE,
        )
        self.on_continuar = on_continuar
        self.on_volver = on_volver
        self._card_frame = True
        self._construir_ui()

    def _construir_ui(self):
        """Construye el campo de nombre con validación y botones de continuar/volver."""
        self.columnconfigure(0, weight=1, minsize=350)

        ctk.CTkLabel(
            self, text="⚡",
            font=("Segoe UI", 38),
            text_color=COLOR_PRIMARIO,
        ).grid(row=0, column=0, pady=(36, 2))

        ctk.CTkLabel(
            self, text="¡A JUGAR!",
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO,
        ).grid(row=1, column=0, pady=(0, 4))

        ctk.CTkLabel(
            self, text="Ingresa tu nombre para comenzar",
            font=FUENTE_PEQUEÑA,
            text_color=COLOR_TEXTO_SEC,
        ).grid(row=2, column=0, pady=(0, 24))

        self._entry_nombre = ctk.CTkEntry(
            self,
            placeholder_text="Tu nombre",
            width=250, height=44,
            font=FUENTE_NORMAL,
            fg_color=COLOR_SUPERFICIE,
            border_color=COLOR_BORDE,
            border_width=2,
        )
        self._entry_nombre.grid(row=3, column=0, pady=0)
        self._entry_nombre.bind("<Return>", lambda e: self._continuar())
        self._entry_nombre.bind(
            "<FocusIn>",
            lambda e: self._entry_nombre.configure(border_color=COLOR_PRIMARIO),
        )
        self._entry_nombre.bind(
            "<FocusOut>",
            lambda e: self._entry_nombre.configure(border_color=COLOR_BORDE),
        )

        self._lbl_error = ctk.CTkLabel(
            self, text="", font=FUENTE_PEQUEÑA, text_color=COLOR_ERROR,
        )
        self._lbl_error.grid(row=4, column=0, pady=(4, 0))

        ctk.CTkButton(
            self,
            text="CONTINUAR  ▶",
            width=250, height=48, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            command=self._continuar,
        ).grid(row=5, column=0, pady=(14, 8))

        ctk.CTkButton(
            self,
            text="← Volver",
            width=250, height=40, corner_radius=10,
            font=FUENTE_PEQUEÑA,
            fg_color="transparent",
            border_width=1,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO_SEC,
            hover_color=COLOR_SUPERFICIE,
            command=self.on_volver,
        ).grid(row=6, column=0, pady=(0, 36))

    def _continuar(self):
        """Valida el nombre ingresado y dispara el callback de continuar."""
        nombre = self._entry_nombre.get().strip()
        if not nombre:
            self._lbl_error.configure(text="Por favor ingresa tu nombre.")
            return
        if len(nombre) > 100:
            self._lbl_error.configure(text="El nombre no puede superar 100 caracteres.")
            return
        self.on_continuar(nombre)