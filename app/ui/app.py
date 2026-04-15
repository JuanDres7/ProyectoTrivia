import customtkinter as ctk
from app.config.settings import ANCHO_VENTANA, ALTO_VENTANA, TITULO_APP, COLOR_FONDO
from app.services.auth_service import AuthService
from app.services.contenido_service import ContenidoService
from app.services.partida_service import PartidaService


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    def __init__(self, auth_service: AuthService,
                 contenido_service: ContenidoService,
                 partida_service: PartidaService):
        super().__init__()
        self.auth_service = auth_service
        self.contenido_service = contenido_service
        self.partida_service = partida_service
        self.title(TITULO_APP)
        self.geometry(f"{ANCHO_VENTANA}x{ALTO_VENTANA}")
        self.resizable(False, False)
        self.configure(fg_color=COLOR_FONDO)

        self._frame_actual = None
        self.mostrar_menu()

    # ------------------------------------------------------------------
    # Navegación interna
    # ------------------------------------------------------------------

    def _cambiar_frame(self, nuevo_frame: ctk.CTkFrame):
        if self._frame_actual is not None:
            self._frame_actual.destroy()
        self._frame_actual = nuevo_frame
        self._frame_actual.place(relx=0.5, rely=0.5, anchor="center")

    # ---- Auth --------------------------------------------------------

    def mostrar_login(self):
        from app.ui.login_frame import LoginFrame
        self._cambiar_frame(LoginFrame(
            master=self,
            auth_service=self.auth_service,
            on_login_exitoso=self.mostrar_menu,
        ))

    def mostrar_menu(self):
        from app.ui.menu_frame import MenuFrame
        self._cambiar_frame(MenuFrame(
            master=self,
            on_gestionar_preguntas=self.mostrar_login_admin,
            on_iniciar_juego=self.mostrar_ingreso_jugador,
        ))

    # ---- Admin -------------------------------------------------------

    def mostrar_login_admin(self):
        from app.ui.login_frame import LoginFrame
        self._cambiar_frame(LoginFrame(
            master=self,
            auth_service=self.auth_service,
            on_login_exitoso=self.mostrar_admin_preguntas,
            on_volver=self.mostrar_menu,
        ))

    def mostrar_admin_preguntas(self):
        from app.ui.admin_preguntas_frame import AdminPreguntasFrame
        self._cambiar_frame(AdminPreguntasFrame(
            master=self,
            contenido_service=self.contenido_service,
            on_categorias=self.mostrar_admin_categorias,
            on_niveles=self.mostrar_admin_niveles,
            on_volver=self.mostrar_menu,
        ))

    def mostrar_admin_categorias(self):
        from app.ui.admin_categorias_frame import AdminCategoriasFrame
        self._cambiar_frame(AdminCategoriasFrame(
            master=self,
            contenido_service=self.contenido_service,
            on_volver=self.mostrar_admin_preguntas,
        ))

    def mostrar_admin_niveles(self):
        from app.ui.admin_niveles_frame import AdminNivelesFrame
        self._cambiar_frame(AdminNivelesFrame(
            master=self,
            contenido_service=self.contenido_service,
            on_volver=self.mostrar_admin_preguntas,
        ))

    # ---- Juego -------------------------------------------------------

    def mostrar_ingreso_jugador(self):
        from app.ui.ingreso_jugador_frame import IngresoJugadorFrame
        self._cambiar_frame(IngresoJugadorFrame(
            master=self,
            on_continuar=self.mostrar_seleccion_nivel,
            on_volver=self.mostrar_menu,
        ))

    def mostrar_seleccion_nivel(self, nombre_jugador: str):
        from app.ui.seleccion_nivel_frame import SeleccionNivelFrame
        self._cambiar_frame(SeleccionNivelFrame(
            master=self,
            contenido_service=self.contenido_service,
            nombre_jugador=nombre_jugador,
            on_nivel_elegido=self._iniciar_partida,
            on_volver=self.mostrar_ingreso_jugador,
        ))

    def _iniciar_partida(self, nombre_jugador: str, nivel_id: int):
        from tkinter import messagebox
        try:
            jugador, partida, preguntas = self.partida_service.iniciar_partida(nombre_jugador, nivel_id)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return
        self.mostrar_pregunta(jugador, partida, preguntas, index=0, correctas=0)

    def mostrar_pregunta(self, jugador, partida, preguntas, index: int, correctas: int):
        from app.ui.pregunta_frame import PreguntaFrame

        def on_respuesta(opcion_id: int):
            es_correcta = self.partida_service.responder_pregunta(
                partida.id, preguntas[index][0].id, opcion_id
            )
            nuevas_correctas = correctas + (1 if es_correcta else 0)
            siguiente = index + 1
            if siguiente < len(preguntas):
                self.mostrar_pregunta(jugador, partida, preguntas, siguiente, nuevas_correctas)
            else:
                resultado = self.partida_service.finalizar_partida(
                    partida.id, jugador.id, partida.nivel_id, nuevas_correctas
                )
                self.mostrar_resultado(nombre_jugador=jugador.nombre, resultado=resultado)

        def on_cancelar():
            self.partida_service.cancelar_partida(partida.id)
            self.mostrar_menu()

        nivel = self.partida_service.obtener_nivel(partida.nivel_id)
        pregunta, opciones = preguntas[index]

        self._cambiar_frame(PreguntaFrame(
            master=self,
            pregunta=pregunta,
            opciones=opciones,
            numero=index + 1,
            total=len(preguntas),
            tiempo_limite=nivel.tiempo_limite_seg,
            on_respuesta=on_respuesta,
            on_cancelar=on_cancelar,
        ))

    def mostrar_resultado(self, nombre_jugador: str, resultado: dict):
        from app.ui.resultado_frame import ResultadoFrame
        self._cambiar_frame(ResultadoFrame(
            master=self,
            nombre_jugador=nombre_jugador,
            puntaje=resultado["puntaje_final"],
            es_record=resultado["es_record_global"],
            record_anterior=resultado["record_anterior"],
            top10=self.partida_service.obtener_top10(),
            on_volver=self.mostrar_menu,
        ))
