import customtkinter as ctk
from app.database.models.contenido import Opcion, Pregunta
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_TEXTO, COLOR_ERROR, COLOR_EXITO,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class PreguntaFrame(ctk.CTkFrame):

    def __init__(self, master, pregunta: Pregunta, opciones: list[Opcion],
                 numero: int, total: int, tiempo_limite: int,
                 on_respuesta, on_cancelar):
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0, width=900, height=600)
        self.pregunta = pregunta
        self.opciones = opciones
        self.numero = numero
        self.total = total
        self.tiempo_limite = tiempo_limite
        self.on_respuesta = on_respuesta
        self.on_cancelar = on_cancelar

        self._tiempo_restante = tiempo_limite
        self._respondida = False
        self._timer_id = None

        self._construir_ui()
        self._iniciar_timer()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _construir_ui(self):
        self.pack_propagate(False)

        # Top bar: progreso + timer
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=50, corner_radius=0)
        top.pack(fill="x")
        top.pack_propagate(False)

        ctk.CTkLabel(top, text=f"Pregunta {self.numero} de {self.total}",
                     font=FUENTE_NORMAL, text_color=COLOR_TEXTO).pack(side="left", padx=16, pady=12)

        self._lbl_timer = ctk.CTkLabel(top, text=f"{self._tiempo_restante}s",
                                        font=FUENTE_SUBTITULO, text_color=COLOR_TEXTO)
        self._lbl_timer.pack(side="right", padx=16, pady=12)

        # Barra de progreso
        bar = ctk.CTkProgressBar(self, progress_color=COLOR_PRIMARIO, height=6, corner_radius=0)
        bar.set(self.numero / self.total)
        bar.pack(fill="x")

        # Enunciado
        enunciado_frame = ctk.CTkFrame(self, fg_color="transparent")
        enunciado_frame.pack(fill="x", padx=40, pady=(30, 20))
        ctk.CTkLabel(enunciado_frame, text=self.pregunta.enunciado,
                     font=FUENTE_SUBTITULO, text_color=COLOR_TEXTO,
                     wraplength=820, justify="left").pack(anchor="w")

        # Opciones
        opciones_frame = ctk.CTkFrame(self, fg_color="transparent")
        opciones_frame.pack(fill="x", padx=40)
        opciones_frame.columnconfigure(0, weight=1)
        opciones_frame.columnconfigure(1, weight=1)

        self._botones = {}
        for i, opcion in enumerate(self.opciones):
            fila, columna = divmod(i, 2)
            opcion_id = opcion.id
            boton = ctk.CTkButton(
                opciones_frame,
                text=f"  {opcion.texto}",
                font=FUENTE_NORMAL,
                fg_color=COLOR_FONDO_FRAME,
                hover_color=COLOR_PRIMARIO,
                text_color=COLOR_TEXTO,
                text_color_disabled="white",
                anchor="w",
                height=56,
                corner_radius=8,
                command=lambda id_opcion_actual=opcion_id: self._responder(id_opcion_actual),
            )
            boton.grid(row=fila, column=columna, padx=6, pady=6, sticky="ew")
            self._botones[opcion_id] = boton

        # Botón cancelar
        ctk.CTkButton(self, text="Cancelar partida", width=200, font=FUENTE_PEQUEÑA,
                      fg_color="transparent", border_width=1, text_color=COLOR_ERROR,
                      hover_color="#3a1a1a", command=self._confirmar_cancelar).pack(pady=(20, 10))

    # ------------------------------------------------------------------
    # Timer
    # ------------------------------------------------------------------

    def _iniciar_timer(self):
        self._tick()

    def _tick(self):
        if self._respondida:
            return
        self._lbl_timer.configure(text=f"{self._tiempo_restante}s")
        if self._tiempo_restante <= 5:
            self._lbl_timer.configure(text_color=COLOR_ERROR)
        if self._tiempo_restante <= 0:
            self._tiempo_agotado()
            return
        self._tiempo_restante -= 1
        self._timer_id = self.after(1000, self._tick)

    def _tiempo_agotado(self):
        if self._respondida:
            return
        self._respondida = True

        opcion_correcta = next(o for o in self.opciones if o.es_correcta)
        for boton in self._botones.values():
            boton.configure(state="disabled", hover_color=boton.cget("fg_color"), text_color="white")
        self._botones[opcion_correcta.id].configure(fg_color=COLOR_EXITO, text_color="white")

        self.after(1500, lambda: self.on_respuesta(-1))

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _responder(self, opcion_id: int):
        if self._respondida:
            return
        self._respondida = True
        if self._timer_id:
            self.after_cancel(self._timer_id)

        opcion_correcta = next(o for o in self.opciones if o.es_correcta)

        for id_opcion, boton in self._botones.items():
            boton.configure(state="disabled", hover_color=boton.cget("fg_color"), text_color="white")

        if opcion_id == opcion_correcta.id:
            self._botones[opcion_id].configure(fg_color=COLOR_EXITO, text_color="white")
        else:
            self._botones[opcion_id].configure(fg_color=COLOR_ERROR, text_color="white")
            self._botones[opcion_correcta.id].configure(fg_color=COLOR_EXITO, text_color="white")

        self.after(1500, lambda: self.on_respuesta(opcion_id))

    def _confirmar_cancelar(self):
        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Cancelar partida")
        dialogo.resizable(False, False)
        dialogo.grab_set()
        dialogo.update_idletasks()
        ancho, alto = 340, 150
        x = (dialogo.winfo_screenwidth() - ancho) // 2
        y = (dialogo.winfo_screenheight() - alto) // 2
        dialogo.geometry(f"{ancho}x{alto}+{x}+{y}")

        ctk.CTkLabel(dialogo, text="¿Seguro que quieres abandonar la partida?",
                     font=FUENTE_NORMAL, text_color=COLOR_TEXTO,
                     wraplength=300).pack(pady=(24, 16))

        botones_frame = ctk.CTkFrame(dialogo, fg_color="transparent")
        botones_frame.pack()

        def confirmar():
            dialogo.destroy()
            self._respondida = True
            if self._timer_id:
                self.after_cancel(self._timer_id)
            self.on_cancelar()

        ctk.CTkButton(botones_frame, text="Sí, abandonar", width=140,
                      fg_color=COLOR_ERROR, hover_color="#a93226",
                      command=confirmar).pack(side="left", padx=8)

        ctk.CTkButton(botones_frame, text="No, continuar", width=140,
                      fg_color=COLOR_FONDO_FRAME,
                      command=dialogo.destroy).pack(side="left", padx=8)
