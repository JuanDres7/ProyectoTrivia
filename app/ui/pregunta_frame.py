import customtkinter as ctk
from app.database.models.contenido import Opcion, Pregunta
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_TEXTO, COLOR_ERROR,
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

        self._lbl_timer = ctk.CTkLabel(top, text=f"⏱ {self._tiempo_restante}s",
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

        for i, opcion in enumerate(self.opciones):
            row, col = divmod(i, 2)
            opcion_id = opcion.id
            btn = ctk.CTkButton(
                opciones_frame,
                text=f"  {opcion.letra}.  {opcion.texto}",
                font=FUENTE_NORMAL,
                fg_color=COLOR_FONDO_FRAME,
                hover_color=COLOR_PRIMARIO,
                text_color=COLOR_TEXTO,
                anchor="w",
                height=56,
                corner_radius=8,
                command=lambda oid=opcion_id: self._responder(oid),
            )
            btn.grid(row=row, column=col, padx=6, pady=6, sticky="ew")

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
        self._lbl_timer.configure(text=f"⏱ {self._tiempo_restante}s")
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
        # Respuesta incorrecta automática: usamos la primera opción como placeholder
        self.on_respuesta(self.opciones[0].id if self.opciones else -1)

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _responder(self, opcion_id: int):
        if self._respondida:
            return
        self._respondida = True
        if self._timer_id:
            self.after_cancel(self._timer_id)
        self.on_respuesta(opcion_id)

    def _confirmar_cancelar(self):
        from tkinter import messagebox
        if messagebox.askyesno("Cancelar", "¿Seguro que quieres abandonar la partida?"):
            self._respondida = True
            if self._timer_id:
                self.after_cancel(self._timer_id)
            self.on_cancelar()
