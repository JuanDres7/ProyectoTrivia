import customtkinter as ctk
from app.config.settings import ANCHO_VENTANA, ALTO_VENTANA, TITULO_APP, COLOR_FONDO
from app.services.auth_service import AuthService


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self, auth_service: AuthService):
        super().__init__()
        self.auth_service = auth_service
        self.title(TITULO_APP)
        self.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_FONDO)

        self._frame_actual = None
        self._callbacks_juego = {}
        self._callbacks_admin = {}

        self.mostrar_login()

    # ------------------------------------------------------------------
    # Registro de callbacks externos (los otros integrantes los inyectan)
    # ------------------------------------------------------------------

    def registrar_callbacks_admin(self, on_gestionar_preguntas):
        """Persona 2 llama a este método para registrar su pantalla."""
        self._callbacks_admin["gestionar_preguntas"] = on_gestionar_preguntas

    def registrar_callbacks_juego(self, on_iniciar_juego):
        """Persona 3 llama a este método para registrar su pantalla."""
        self._callbacks_juego["iniciar_juego"] = on_iniciar_juego

    # ------------------------------------------------------------------
    # Navegación
    # ------------------------------------------------------------------

    def _cambiar_frame(self, nuevo_frame: ctk.CTkFrame):
        if self._frame_actual is not None:
            self._frame_actual.destroy()
        self._frame_actual = nuevo_frame
        self._frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    def mostrar_login(self):
        from app.ui.login_frame import LoginFrame
        frame = LoginFrame(
            master=self,
            auth_service=self.auth_service,
            on_login_exitoso=self.mostrar_menu
        )
        self._cambiar_frame(frame)

    def mostrar_menu(self):
        from app.ui.menu_frame import MenuFrame
        frame = MenuFrame(
            master=self,
            on_gestionar_preguntas=self._ir_gestionar_preguntas,
            on_iniciar_juego=self._ir_iniciar_juego,
            on_cerrar_sesion=self.mostrar_login
        )
        self._cambiar_frame(frame)

    def _ir_gestionar_preguntas(self):
        callback = self._callbacks_admin.get("gestionar_preguntas")
        if callback:
            callback()

    def _ir_iniciar_juego(self):
        callback = self._callbacks_juego.get("iniciar_juego")
        if callback:
            callback()
