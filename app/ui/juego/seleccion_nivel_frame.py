import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.config.settings import (
    COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_EXITO, COLOR_SECUNDARIO,
    COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
    ANCHO_VENTANA, ALTO_VENTANA,
)

# Colores neón para los tres niveles: verde → cian → magenta
_COLORES_NIVEL = [COLOR_EXITO, COLOR_PRIMARIO, COLOR_SECUNDARIO]
# Fondo oscuro teñido del color de nivel cuando la tarjeta está seleccionada
_FONDOS_NIVEL_SEL = ["#061a0e", "#051520", "#18051e"]


class SeleccionNivelFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService,
                 nombre_jugador: str, on_nivel_elegido, on_volver):
        """Inicializa la pantalla de configuración de partida con niveles y categorías."""
        super().__init__(
            master,
            fg_color=COLOR_FONDO,
            corner_radius=0,
            width=ANCHO_VENTANA,
            height=ALTO_VENTANA,
        )
        self.grid_propagate(False)
        self.contenido_service = contenido_service
        self.nombre_jugador = nombre_jugador
        self.on_nivel_elegido = on_nivel_elegido
        self.on_volver = on_volver

        self._nivel_seleccionado: int | None = None
        self._nivel_cards: dict = {}       # nivel_id -> (card_frame, color, fondo_sel)
        self._categoria_vars: dict = {}    # categoria_id -> BooleanVar
        self._var_todas: ctk.BooleanVar | None = None

        self._construir_ui()

    # ------------------------------------------------------------------
    # Construcción de la interfaz
    # ------------------------------------------------------------------

    def _construir_ui(self):
        """Construye la cabecera, los dos paneles (niveles y categorías) y los botones de acción."""
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text=f"Hola, {self.nombre_jugador}",
            font=FUENTE_TITULO,
            text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, pady=(28, 2))

        ctk.CTkLabel(
            self,
            text="Elige el nivel y las categorías antes de jugar",
            font=FUENTE_PEQUEÑA,
            text_color=COLOR_TEXTO_SEC,
        ).grid(row=1, column=0, pady=(0, 20))

        # ── Contenedor de dos paneles ─────────────────────────────────
        contenedor = ctk.CTkFrame(self, fg_color="transparent")
        contenedor.grid(row=2, column=0, padx=40)
        contenedor.columnconfigure(0, weight=1)
        contenedor.columnconfigure(1, weight=0)
        contenedor.columnconfigure(2, weight=1)

        panel_izq = ctk.CTkFrame(contenedor, fg_color="transparent")
        panel_izq.grid(row=0, column=0, padx=(0, 16), sticky="n")

        ctk.CTkFrame(
            contenedor, width=1, fg_color=COLOR_BORDE,
        ).grid(row=0, column=1, sticky="ns", padx=4)

        panel_der = ctk.CTkFrame(contenedor, fg_color="transparent")
        panel_der.grid(row=0, column=2, padx=(16, 0), sticky="n")

        self._construir_panel_niveles(panel_izq)
        self._construir_panel_categorias(panel_der)

        # ── Botones inferiores ────────────────────────────────────────
        btn_bar = ctk.CTkFrame(self, fg_color="transparent")
        btn_bar.grid(row=3, column=0, pady=(20, 28))

        self._btn_jugar = ctk.CTkButton(
            btn_bar,
            text="▶   JUGAR",
            width=200, height=48, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            state="disabled",
            command=self._jugar,
        )
        self._btn_jugar.grid(row=0, column=0, padx=10)

        ctk.CTkButton(
            btn_bar,
            text="← Volver",
            width=160, height=48, corner_radius=10,
            font=FUENTE_PEQUEÑA,
            fg_color="transparent",
            border_width=1,
            border_color=COLOR_BORDE,
            text_color=COLOR_TEXTO_SEC,
            hover_color=COLOR_FONDO_FRAME,
            command=self.on_volver,
        ).grid(row=0, column=1, padx=10)

    # ------------------------------------------------------------------
    # Panel de niveles
    # ------------------------------------------------------------------

    def _construir_panel_niveles(self, parent: ctk.CTkFrame):
        """Renderiza una tarjeta seleccionable por cada nivel disponible."""
        parent.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            parent,
            text="Nivel de dificultad",
            font=FUENTE_SUBTITULO,
            text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, pady=(0, 12), sticky="w")

        niveles = self.contenido_service.listar_niveles()
        for i, nivel in enumerate(niveles):
            color = _COLORES_NIVEL[i % len(_COLORES_NIVEL)]
            fondo_sel = _FONDOS_NIVEL_SEL[i % len(_FONDOS_NIVEL_SEL)]

            card = ctk.CTkFrame(
                parent,
                fg_color=COLOR_SUPERFICIE,
                corner_radius=10,
                border_width=2,
                border_color=COLOR_BORDE,
                cursor="hand2",
                width=280,
            )
            card.grid(row=1 + i, column=0, pady=5, sticky="ew")
            card.columnconfigure(0, weight=1)

            ctk.CTkLabel(
                card,
                text=f"●  {nivel.nombre.upper()}",
                font=FUENTE_SUBTITULO,
                text_color=color,
                anchor="w",
            ).grid(row=0, column=0, padx=16, pady=(14, 2), sticky="w")

            ctk.CTkLabel(
                card,
                text=f"{nivel.num_preguntas} preguntas  ·  {nivel.tiempo_limite_seg} s / pregunta",
                font=FUENTE_PEQUEÑA,
                text_color=COLOR_TEXTO_SEC,
                anchor="w",
            ).grid(row=1, column=0, padx=16, pady=(0, 14), sticky="w")

            nivel_id = nivel.id
            self._nivel_cards[nivel_id] = (card, color, fondo_sel)
            self._bind_card(card, nivel_id, color, fondo_sel)

    def _bind_card(self, card: ctk.CTkFrame, nivel_id: int, color: str, fondo_sel: str):
        """Vincula el evento de clic a la tarjeta y a todos sus widgets hijos."""
        handler = lambda e, nid=nivel_id, c=card, col=color, fs=fondo_sel: \
            self._seleccionar_nivel(nid, c, col, fs)
        card.bind("<Button-1>", handler)
        for child in card.winfo_children():
            child.bind("<Button-1>", handler)

    def _seleccionar_nivel(self, nivel_id: int, card: ctk.CTkFrame, color: str, fondo_sel: str):
        """Resalta la tarjeta elegida, deselecciona las demás y habilita el botón jugar."""
        for _, (c, _, _) in self._nivel_cards.items():
            c.configure(fg_color=COLOR_SUPERFICIE, border_color=COLOR_BORDE)
        card.configure(fg_color=fondo_sel, border_color=color)
        self._nivel_seleccionado = nivel_id
        self._actualizar_boton_jugar()

    # ------------------------------------------------------------------
    # Panel de categorías
    # ------------------------------------------------------------------

    def _construir_panel_categorias(self, parent: ctk.CTkFrame):
        """Renderiza un checkbox por cada categoría disponible más la opción de seleccionar todas."""
        parent.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            parent,
            text="Categorías",
            font=FUENTE_SUBTITULO,
            text_color=COLOR_TEXTO,
        ).grid(row=0, column=0, pady=(0, 12), sticky="w")

        categorias = self.contenido_service.listar_categorias()

        self._var_todas = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            parent,
            text="Seleccionar todas",
            variable=self._var_todas,
            font=FUENTE_NORMAL,
            text_color=COLOR_TEXTO,
            fg_color=COLOR_PRIMARIO,
            hover_color=COLOR_PRIMARIO_HOVER,
            command=self._toggle_todas,
        ).grid(row=1, column=0, pady=(0, 6), sticky="w")

        ctk.CTkFrame(
            parent, height=1, fg_color=COLOR_BORDE,
        ).grid(row=2, column=0, sticky="ew", pady=(2, 10))

        for i, cat in enumerate(categorias):
            var = ctk.BooleanVar(value=True)
            self._categoria_vars[cat.id] = var
            ctk.CTkCheckBox(
                parent,
                text=cat.nombre,
                variable=var,
                font=FUENTE_NORMAL,
                text_color=COLOR_TEXTO,
                fg_color=COLOR_PRIMARIO,
                hover_color=COLOR_PRIMARIO_HOVER,
                command=self._on_categoria_cambio,
            ).grid(row=3 + i, column=0, pady=5, sticky="w")

    def _toggle_todas(self):
        """Marca o desmarca todas las categorías en bloque."""
        val = self._var_todas.get()
        for var in self._categoria_vars.values():
            var.set(val)
        self._actualizar_boton_jugar()

    def _on_categoria_cambio(self):
        """Sincroniza el checkbox 'Seleccionar todas' según el estado individual de cada categoría."""
        todas = all(v.get() for v in self._categoria_vars.values())
        self._var_todas.set(todas)
        self._actualizar_boton_jugar()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _actualizar_boton_jugar(self):
        """Habilita el botón Jugar solo si hay nivel elegido y al menos una categoría activa."""
        nivel_ok = self._nivel_seleccionado is not None
        cats_ok = any(v.get() for v in self._categoria_vars.values())
        self._btn_jugar.configure(state="normal" if (nivel_ok and cats_ok) else "disabled")

    def _jugar(self):
        """Recopila nivel y categorías seleccionadas y dispara el callback de inicio de partida."""
        todas = all(v.get() for v in self._categoria_vars.values())
        categoria_ids = None if todas else [
            cid for cid, var in self._categoria_vars.items() if var.get()
        ]
        self.on_nivel_elegido(self.nombre_jugador, self._nivel_seleccionado, categoria_ids)
