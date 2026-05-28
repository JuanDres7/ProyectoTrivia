import customtkinter as ctk
from app.services.auth_service import AuthService
from app.config.settings import (
    COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_TEXTO, COLOR_TEXTO_SEC, COLOR_ERROR,
    FUENTE_TITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class LoginFrame(ctk.CTkFrame):

    def __init__(self, master, auth_service: AuthService, on_login_exitoso, on_volver=None):
        """Inicializa el frame de login con los callbacks de éxito y retroceso."""
        super().__init__(
            master,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=16,
            border_width=1,
            border_color=COLOR_BORDE,
        )
        self.auth_service = auth_service
        self.on_login_exitoso = on_login_exitoso
        self.on_volver = on_volver
        self._card_frame = True
        self._construir_ui()

    def _construir_ui(self):
        """Construye el formulario de usuario y contraseña con su botón de ingreso."""
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self, text="⚙",
            font=("Segoe UI", 38),
            text_color=COLOR_PRIMARIO,
        ).grid(row=0, column=0, pady=(36, 2))

        ctk.CTkLabel(
            self, text="ADMINISTRADOR",
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO,
        ).grid(row=1, column=0, pady=(0, 4))

        ctk.CTkLabel(
            self, text="Ingresa tus credenciales para continuar",
            font=FUENTE_PEQUEÑA,
            text_color=COLOR_TEXTO_SEC,
        ).grid(row=2, column=0, pady=(0, 24))

        self.entry_usuario = ctk.CTkEntry(
            self,
            placeholder_text="Usuario",
            width=300, height=44,
            font=FUENTE_NORMAL,
            fg_color=COLOR_SUPERFICIE,
            border_color=COLOR_BORDE,
            border_width=2,
        )
        self.entry_usuario.grid(row=3, column=0, pady=(0, 8))
        self.entry_usuario.bind("<FocusIn>",
            lambda e: self.entry_usuario.configure(border_color=COLOR_PRIMARIO))
        self.entry_usuario.bind("<FocusOut>",
            lambda e: self.entry_usuario.configure(border_color=COLOR_BORDE))

        self.entry_password = ctk.CTkEntry(
            self,
            placeholder_text="Contraseña",
            show="*",
            width=300, height=44,
            font=FUENTE_NORMAL,
            fg_color=COLOR_SUPERFICIE,
            border_color=COLOR_BORDE,
            border_width=2,
        )
        self.entry_password.grid(row=4, column=0, pady=0)
        self.entry_password.bind("<Return>", lambda e: self._intentar_login())
        self.entry_password.bind("<FocusIn>",
            lambda e: self.entry_password.configure(border_color=COLOR_PRIMARIO))
        self.entry_password.bind("<FocusOut>",
            lambda e: self.entry_password.configure(border_color=COLOR_BORDE))

        self.lbl_error = ctk.CTkLabel(
            self, text="", font=FUENTE_PEQUEÑA, text_color=COLOR_ERROR,
        )
        self.lbl_error.grid(row=5, column=0, pady=(6, 0))

        ctk.CTkButton(
            self,
            text="INGRESAR  ▶",
            width=300, height=48, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            command=self._intentar_login,
        ).grid(row=6, column=0, pady=(12, 8))

        if self.on_volver:
            ctk.CTkButton(
                self,
                text="← Volver",
                width=300, height=40, corner_radius=10,
                font=FUENTE_PEQUEÑA,
                fg_color="transparent",
                border_width=1,
                border_color=COLOR_BORDE,
                text_color=COLOR_TEXTO_SEC,
                hover_color=COLOR_SUPERFICIE,
                command=self.on_volver,
            ).grid(row=7, column=0, pady=(0, 36))

    def _intentar_login(self):
        """Valida los campos y delega la autenticación al servicio."""
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