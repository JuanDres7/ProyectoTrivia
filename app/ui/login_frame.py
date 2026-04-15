import customtkinter as ctk
from app.services.auth_service import AuthService
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_FONDO_FRAME, COLOR_TEXTO, COLOR_ERROR,
    FUENTE_TITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA
)


class LoginFrame(ctk.CTkFrame):

    def __init__(self, master, auth_service: AuthService, on_login_exitoso, on_volver=None):
        super().__init__(master, fg_color=COLOR_FONDO_FRAME, corner_radius=16)
        self.auth_service = auth_service
        self.on_login_exitoso = on_login_exitoso
        self.on_volver = on_volver
        self._construir_ui()

    def _construir_ui(self):
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Panel de Administrador", font=FUENTE_TITULO, text_color=COLOR_TEXTO).grid(
            row=0, column=0, pady=(40, 4)
        )
        ctk.CTkLabel(self, text="Ingresa tus credenciales para continuar", font=FUENTE_PEQUEÑA, text_color="#aaaaaa").grid(
            row=1, column=0, pady=(0, 30)
        )

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", width=280, font=FUENTE_NORMAL)
        self.entry_usuario.grid(row=2, column=0, pady=8)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*", width=280, font=FUENTE_NORMAL)
        self.entry_password.grid(row=3, column=0, pady=8)
        self.entry_password.bind("<Return>", lambda e: self._intentar_login())

        self.lbl_error = ctk.CTkLabel(self, text="", font=FUENTE_PEQUEÑA, text_color=COLOR_ERROR)
        self.lbl_error.grid(row=4, column=0, pady=(4, 0))

        ctk.CTkButton(
            self, text="Ingresar", width=280, font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO, command=self._intentar_login
        ).grid(row=5, column=0, pady=(12, 8))

        if self.on_volver:
            ctk.CTkButton(
                self, text="← Volver", width=280, font=FUENTE_NORMAL,
                fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
                command=self.on_volver
            ).grid(row=6, column=0, pady=(0, 30))

    def _intentar_login(self):
        username = self.entry_usuario.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            self.lbl_error.configure(text="Completa todos los campos.")
            return

        if self.auth_service.autenticar(username, password):
            self.lbl_error.configure(text="")
            self.on_login_exitoso()
        else:
            self.lbl_error.configure(text="Usuario o contraseña incorrectos.")
            self.entry_password.delete(0, "end")
