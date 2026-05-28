import customtkinter as ctk
from app.database.models.contenido import Opcion, Pregunta
from app.ui.otros.dialogo import confirmar
from app.config.settings import (
    COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_SECUNDARIO,
    COLOR_EXITO, COLOR_ERROR, COLOR_DORADO,
    COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA, FUENTE_TIMER, FUENTE_BADGE,
)

_LETRAS = ["A", "B", "C", "D"]
# Un color neón distinto para el badge de cada opción
_COLORES_BADGE = [COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_EXITO, COLOR_DORADO]


class PreguntaFrame(ctk.CTkFrame):

    def __init__(self, master, pregunta: Pregunta, opciones: list[Opcion],
                 numero: int, total: int, tiempo_limite: int,
                 on_respuesta, on_cancelar):
        """Inicializa el frame con la pregunta actual, el contador de tiempo y las opciones."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0)
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
        # opcion_id -> {'frame': CTkFrame, 'badge': CTkLabel, 'texto': CTkLabel, 'color_badge': str}
        self._opciones_ui: dict = {}

        self._construir_ui()
        self._iniciar_timer()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _construir_ui(self):
        """Construye la barra superior, el enunciado, las opciones y el botón de cancelar."""

        # ── Top bar ───────────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=54, corner_radius=0)
        top.pack(fill="x")
        top.pack_propagate(False)

        ctk.CTkLabel(
            top,
            text=f"Pregunta  {self.numero} / {self.total}",
            font=FUENTE_NORMAL,
            text_color=COLOR_TEXTO_SEC,
        ).pack(side="left", padx=20)

        # Timer con borde dinámico que cambia de color según la urgencia
        self._timer_pill = ctk.CTkFrame(
            top,
            fg_color=COLOR_FONDO,
            corner_radius=20,
            border_width=2,
            border_color=COLOR_PRIMARIO,
        )
        self._timer_pill.pack(side="right", padx=20, pady=9)
        self._lbl_timer = ctk.CTkLabel(
            self._timer_pill,
            text=str(self._tiempo_restante),
            font=FUENTE_TIMER,
            text_color=COLOR_PRIMARIO,
        )
        self._lbl_timer.pack(padx=18, pady=2)

        # ── Barra de progreso de preguntas ────────────────────────────
        barra = ctk.CTkProgressBar(self, progress_color=COLOR_PRIMARIO, height=4, corner_radius=0)
        barra.set(self.numero / self.total)
        barra.pack(fill="x")

        # ── Enunciado ─────────────────────────────────────────────────
        enunciado_outer = ctk.CTkFrame(self, fg_color="transparent")
        enunciado_outer.pack(fill="x", padx=40, pady=(26, 14))
        ctk.CTkLabel(
            enunciado_outer,
            text=self.pregunta.enunciado,
            font=FUENTE_SUBTITULO,
            text_color=COLOR_TEXTO,
            wraplength=820,
            justify="left",
        ).pack(anchor="w")

        # ── Opciones (grid 2 × 2) ─────────────────────────────────────
        opciones_outer = ctk.CTkFrame(self, fg_color="transparent")
        opciones_outer.pack(fill="x", padx=40)
        opciones_outer.columnconfigure(0, weight=1)
        opciones_outer.columnconfigure(1, weight=1)

        for i, opcion in enumerate(self.opciones):
            fila, columna = divmod(i, 2)
            frame, badge, lbl = self._crear_opcion_widget(
                opciones_outer,
                letra=_LETRAS[i],
                color_badge=_COLORES_BADGE[i],
                texto=opcion.texto,
                opcion_id=opcion.id,
            )
            frame.grid(row=fila, column=columna, padx=6, pady=6, sticky="ew")
            self._opciones_ui[opcion.id] = {
                "frame": frame,
                "badge": badge,
                "texto": lbl,
                "color_badge": _COLORES_BADGE[i],
            }

        # ── Botón cancelar ────────────────────────────────────────────
        ctk.CTkButton(
            self,
            text="✕  Cancelar partida",
            width=200, height=34,
            font=FUENTE_PEQUEÑA,
            fg_color="transparent",
            border_width=1,
            border_color="#3a1010",
            text_color=COLOR_ERROR,
            hover_color="#160606",
            corner_radius=8,
            command=self._confirmar_cancelar,
        ).pack(pady=(14, 0))

    def _crear_opcion_widget(
        self,
        parent: ctk.CTkFrame,
        letra: str,
        color_badge: str,
        texto: str,
        opcion_id: int,
    ) -> tuple:
        """Crea un widget compuesto (badge de letra + texto) para una opción de respuesta."""
        frame = ctk.CTkFrame(
            parent,
            fg_color=COLOR_SUPERFICIE,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDE,
            cursor="hand2",
        )
        frame.columnconfigure(1, weight=1)

        badge = ctk.CTkLabel(
            frame,
            text=letra,
            width=34, height=34,
            font=FUENTE_BADGE,
            fg_color=color_badge,
            text_color="#080812",
            corner_radius=6,
        )
        badge.grid(row=0, column=0, padx=(14, 10), pady=14)

        lbl = ctk.CTkLabel(
            frame,
            text=texto,
            font=FUENTE_NORMAL,
            text_color=COLOR_TEXTO,
            anchor="w",
            justify="left",
            wraplength=300,
        )
        lbl.grid(row=0, column=1, padx=(0, 14), pady=10, sticky="ew")

        click_handler = lambda e: self._responder(opcion_id)
        frame.bind("<Button-1>", click_handler)
        badge.bind("<Button-1>", click_handler)
        lbl.bind("<Button-1>", click_handler)

        def on_enter(e, f=frame, cb=color_badge):
            if not self._respondida:
                f.configure(border_color=cb)

        def on_leave(e, f=frame):
            if not self._respondida:
                f.configure(border_color=COLOR_BORDE)

        for widget in (frame, badge, lbl):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

        return frame, badge, lbl

    # ------------------------------------------------------------------
    # Timer
    # ------------------------------------------------------------------

    def _iniciar_timer(self):
        """Arranca el contador regresivo llamando al primer tick."""
        self._tick()

    def _tick(self):
        """Decrementa el tiempo cada segundo y cambia el color del timer según la urgencia."""
        if self._respondida:
            return

        if self._tiempo_restante > 10:
            color = COLOR_PRIMARIO
        elif self._tiempo_restante > 5:
            color = COLOR_DORADO
        else:
            color = COLOR_ERROR

        self._lbl_timer.configure(text=str(self._tiempo_restante), text_color=color)
        self._timer_pill.configure(border_color=color)

        if self._tiempo_restante == 5:
            self._pulsar_timer()

        if self._tiempo_restante <= 0:
            self._tiempo_agotado()
            return

        self._tiempo_restante -= 1
        self._timer_id = self.after(1000, self._tick)

    def _tiempo_agotado(self):
        """Marca la opción correcta, bloquea las interacciones y avanza como respuesta incorrecta."""
        if self._respondida:
            return
        self._respondida = True

        opcion_correcta = next(o for o in self.opciones if o.es_correcta)
        self._aplicar_feedback_correcto(opcion_correcta.id)

        opcion_incorrecta = next((o for o in self.opciones if not o.es_correcta), self.opciones[0])
        self.after(1500, lambda: self.on_respuesta(opcion_incorrecta.id))

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _responder(self, opcion_id: int):
        """Registra la respuesta, aplica feedback visual y avanza tras 1,5 s."""
        if self._respondida:
            return
        self._respondida = True
        if self._timer_id:
            self.after_cancel(self._timer_id)

        opcion_correcta = next(o for o in self.opciones if o.es_correcta)

        if opcion_id == opcion_correcta.id:
            self._aplicar_feedback_correcto(opcion_id)
        else:
            self._aplicar_feedback_incorrecto(opcion_id, opcion_correcta.id)

        self.after(1500, lambda: self.on_respuesta(opcion_id))

    def _aplicar_feedback_correcto(self, opcion_id: int):
        """Colorea la opción correcta en verde, atenúa el resto y lanza pulso de confirmación."""
        for oid, ui in self._opciones_ui.items():
            if oid == opcion_id:
                ui["frame"].configure(fg_color="#061a0e", border_color=COLOR_EXITO)
                ui["badge"].configure(fg_color=COLOR_EXITO, text_color="#080812")
                ui["texto"].configure(text_color=COLOR_EXITO)
            else:
                ui["frame"].configure(fg_color=COLOR_FONDO, border_color=COLOR_FONDO)
                ui["badge"].configure(fg_color="#1a1a30", text_color="#3a3a5c")
                ui["texto"].configure(text_color="#3a3a5c")
        self._pulsar_correcto(opcion_id)

    def _aplicar_feedback_incorrecto(self, opcion_incorrecta_id: int, opcion_correcta_id: int):
        """Colorea en rojo la selección incorrecta, muestra la correcta en verde y lanza el shake."""
        for oid, ui in self._opciones_ui.items():
            if oid == opcion_incorrecta_id:
                ui["frame"].configure(fg_color="#1a0606", border_color=COLOR_ERROR)
                ui["badge"].configure(fg_color=COLOR_ERROR, text_color="#080812")
                ui["texto"].configure(text_color=COLOR_ERROR)
            elif oid == opcion_correcta_id:
                ui["frame"].configure(fg_color="#061a0e", border_color=COLOR_EXITO)
                ui["badge"].configure(fg_color=COLOR_EXITO, text_color="#080812")
                ui["texto"].configure(text_color=COLOR_EXITO)
            else:
                ui["frame"].configure(fg_color=COLOR_FONDO, border_color=COLOR_FONDO)
                ui["badge"].configure(fg_color="#1a1a30", text_color="#3a3a5c")
                ui["texto"].configure(text_color="#3a3a5c")
        self._shake_opcion(opcion_incorrecta_id)

    # ------------------------------------------------------------------
    # Animaciones
    # ------------------------------------------------------------------

    def _pulsar_timer(self, iteracion: int = 0):
        """Pulsa el borde del timer mientras quedan ≤5 segundos."""
        if self._respondida or self._tiempo_restante > 5:
            return
        try:
            bw = 4 if iteracion % 2 == 0 else 2
            self._timer_pill.configure(border_width=bw)
            self.after(300, lambda: self._pulsar_timer(iteracion + 1))
        except Exception:
            pass

    def _pulsar_correcto(self, opcion_id: int, iteracion: int = 0):
        """Destella el borde blanco/verde de la opción correcta al acertar."""
        try:
            if iteracion >= 4:
                self._opciones_ui[opcion_id]["frame"].configure(border_color=COLOR_EXITO)
                return
            color = "#ffffff" if iteracion % 2 == 0 else COLOR_EXITO
            self._opciones_ui[opcion_id]["frame"].configure(border_color=color)
            self.after(80, lambda: self._pulsar_correcto(opcion_id, iteracion + 1))
        except Exception:
            pass

    def _shake_opcion(self, opcion_id: int, iteracion: int = 0):
        """Sacude horizontalmente la opción incorrecta oscilando su margen (padx siempre ≥ 0)."""
        try:
            if iteracion >= 8:
                self._opciones_ui[opcion_id]["frame"].grid_configure(padx=6)
                return
            offset = 6 if iteracion % 2 == 0 else -6
            padx_l = max(0, 6 + offset)
            padx_r = max(0, 6 - offset)
            self._opciones_ui[opcion_id]["frame"].grid_configure(padx=(padx_l, padx_r))
            self.after(50, lambda: self._shake_opcion(opcion_id, iteracion + 1))
        except Exception:
            pass

    def _confirmar_cancelar(self):
        """Muestra el diálogo de confirmación antes de abandonar la partida."""
        def ejecutar():
            self._respondida = True
            if self._timer_id:
                self.after_cancel(self._timer_id)
            self.on_cancelar()

        confirmar(self, "¿Seguro que quieres abandonar la partida?", ejecutar)