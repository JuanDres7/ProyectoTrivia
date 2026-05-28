import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.config.settings import (
    COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_EXITO, COLOR_SECUNDARIO,
    COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA, FUENTE_BADGE,
)

# Colores neón para los tres niveles (verde / cian / magenta)
_COLORES_NIVEL = [COLOR_EXITO, COLOR_PRIMARIO, COLOR_SECUNDARIO]


class AdminNivelesFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService, on_volver):
        """Inicializa la pantalla de niveles y carga la tabla."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0)
        self.contenido_service = contenido_service
        self.on_volver = on_volver
        self._construir_ui()
        self._cargar_niveles()

    def _construir_ui(self):
        """Construye la barra superior y la tabla estática con los niveles de dificultad."""

        # ── Top bar ───────────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=54, corner_radius=0)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        ctk.CTkLabel(
            top, text="⚙  NIVELES DE DIFICULTAD",
            font=FUENTE_SUBTITULO, text_color=COLOR_TEXTO,
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            top, text="← Preguntas",
            width=120, height=34, corner_radius=8,
            font=FUENTE_PEQUEÑA,
            fg_color="transparent",
            border_width=1, border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO_SEC,
            hover_color=COLOR_SUPERFICIE,
            command=self.on_volver,
        ).pack(side="right", padx=16, pady=10)

        # Separador inferior del top bar
        ctk.CTkFrame(self, height=1, fg_color=COLOR_BORDE, corner_radius=0).pack(fill="x")

        # ── Tarjeta de tabla ──────────────────────────────────────────
        card = ctk.CTkFrame(
            self,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=12,
            border_width=1,
            border_color=COLOR_BORDE,
        )
        card.place(relx=0.5, rely=0.55, anchor="center")

        tabla = ctk.CTkFrame(card, fg_color="transparent")
        tabla.pack(padx=24, pady=24)

        # Cabecera
        header = ctk.CTkFrame(tabla, fg_color=COLOR_PRIMARIO, corner_radius=8, height=36)
        header.pack(fill="x", pady=(0, 4))
        header.pack_propagate(False)
        for texto, ancho in [("#", 40), ("Nivel", 140), ("Preguntas", 110), ("Tiempo / preg.", 140)]:
            ctk.CTkLabel(
                header, text=texto, width=ancho,
                font=FUENTE_BADGE, text_color="#080812",
            ).pack(side="left", padx=4)

        # Almacenamos el frame de tabla para agregar filas después
        self._tabla = tabla

    def _cargar_niveles(self):
        """Rellena la tabla con los niveles obtenidos del servicio."""
        niveles = self.contenido_service.listar_niveles()
        for i, nivel in enumerate(niveles):
            color = _COLORES_NIVEL[i % len(_COLORES_NIVEL)]
            fondo = COLOR_SUPERFICIE if i % 2 == 0 else COLOR_FONDO_FRAME

            fila = ctk.CTkFrame(self._tabla, fg_color=fondo, corner_radius=6, height=40)
            fila.pack(fill="x", pady=1)
            fila.pack_propagate(False)

            ctk.CTkLabel(
                fila, text=str(nivel.id), width=40,
                font=FUENTE_BADGE, text_color=COLOR_TEXTO_SEC,
            ).pack(side="left", padx=4)

            ctk.CTkLabel(
                fila, text=f"●  {nivel.nombre}", width=140,
                font=FUENTE_NORMAL, text_color=color, anchor="w",
            ).pack(side="left", padx=4)

            ctk.CTkLabel(
                fila, text=str(nivel.num_preguntas), width=110,
                font=FUENTE_BADGE, text_color=COLOR_TEXTO,
            ).pack(side="left", padx=4)

            ctk.CTkLabel(
                fila, text=f"{nivel.tiempo_limite_seg} s", width=140,
                font=FUENTE_BADGE, text_color=COLOR_TEXTO,
            ).pack(side="left", padx=4)