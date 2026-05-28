import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.ui.otros.dialogo import mostrar_error, mostrar_aviso, confirmar
from app.config.settings import (
    COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_EXITO, COLOR_ERROR,
    COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA, FUENTE_BADGE,
)


class AdminCategoriasFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService, on_volver):
        """Inicializa el frame de gestión de categorías y carga el listado inicial."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0)
        self.contenido_service = contenido_service
        self.on_volver = on_volver
        self._categoria_id_seleccionada: int | None = None
        self._fila_widgets: dict[int, ctk.CTkFrame] = {}
        self._construir_ui()
        self._cargar_categorias()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _construir_ui(self):
        """Construye la barra superior, la tabla de categorías y el formulario de edición."""

        # ── Top bar ───────────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=54, corner_radius=0)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        ctk.CTkLabel(
            top, text="⚙  GESTIÓN DE CATEGORÍAS",
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

        ctk.CTkFrame(self, height=1, fg_color=COLOR_BORDE, corner_radius=0).pack(fill="x")

        # ── Cuerpo ────────────────────────────────────────────────────
        body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        body.pack(fill="both", expand=True)

        # Panel izquierdo — tabla
        left = ctk.CTkFrame(
            body,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDE,
            width=440,
        )
        left.pack(side="left", fill="y", padx=(12, 6), pady=12)
        left.pack_propagate(False)

        ctk.CTkLabel(
            left, text="Categorías registradas",
            font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
        ).pack(anchor="w", padx=14, pady=(12, 6))

        # Cabecera de tabla
        header = ctk.CTkFrame(left, fg_color=COLOR_PRIMARIO, corner_radius=8, height=32)
        header.pack(fill="x", padx=10, pady=(0, 3))
        header.pack_propagate(False)
        ctk.CTkLabel(
            header, text="#", width=32,
            font=FUENTE_BADGE, text_color="#080812",
        ).pack(side="left", padx=6)
        ctk.CTkLabel(
            header, text="Nombre",
            font=FUENTE_BADGE, text_color="#080812", anchor="w",
        ).pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(
            header, text="Descripción", width=120,
            font=FUENTE_BADGE, text_color="#080812",
        ).pack(side="right", padx=8)

        # Scrollable para las filas
        self._lista_scroll = ctk.CTkScrollableFrame(
            left, fg_color="transparent", corner_radius=0,
        )
        self._lista_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Panel derecho — formulario
        right = ctk.CTkFrame(
            body,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDE,
        )
        right.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        ctk.CTkLabel(
            right, text="Nombre *",
            font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
        ).pack(anchor="w", padx=20, pady=(24, 4))

        self._entry_nombre = ctk.CTkEntry(
            right, font=FUENTE_NORMAL,
            fg_color=COLOR_SUPERFICIE,
            border_color=COLOR_BORDE,
            border_width=2,
        )
        self._entry_nombre.pack(fill="x", padx=20)
        self._entry_nombre.bind("<FocusIn>",
            lambda e: self._entry_nombre.configure(border_color=COLOR_PRIMARIO))
        self._entry_nombre.bind("<FocusOut>",
            lambda e: self._entry_nombre.configure(border_color=COLOR_BORDE))

        ctk.CTkLabel(
            right, text="Descripción  (opcional)",
            font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
        ).pack(anchor="w", padx=20, pady=(16, 4))

        self._entry_desc = ctk.CTkTextbox(
            right, height=90, font=FUENTE_NORMAL,
            fg_color=COLOR_SUPERFICIE,
            border_color=COLOR_BORDE,
            border_width=2,
            text_color=COLOR_TEXTO,
        )
        self._entry_desc.pack(fill="x", padx=20)

        self._lbl_error = ctk.CTkLabel(
            right, text="", font=FUENTE_PEQUEÑA, text_color=COLOR_ERROR,
        )
        self._lbl_error.pack(pady=(10, 0))

        btn_row = ctk.CTkFrame(right, fg_color="transparent")
        btn_row.pack(pady=14)

        ctk.CTkButton(
            btn_row, text="Nueva",
            width=100, height=38, corner_radius=8,
            font=FUENTE_NORMAL,
            fg_color=COLOR_EXITO, hover_color="#1db358",
            text_color="#080812",
            command=self._limpiar,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_row, text="Guardar",
            width=100, height=38, corner_radius=8,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            command=self._guardar,
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_row, text="Eliminar",
            width=100, height=38, corner_radius=8,
            font=FUENTE_NORMAL,
            fg_color=COLOR_ERROR, hover_color="#c53030",
            text_color=COLOR_TEXTO,
            command=self._eliminar,
        ).pack(side="left", padx=5)

    # ------------------------------------------------------------------
    # Tabla
    # ------------------------------------------------------------------

    def _cargar_categorias(self):
        """Recarga las filas de la tabla con las categorías actuales."""
        for fila in self._fila_widgets.values():
            fila.destroy()
        self._fila_widgets.clear()

        categorias = self.contenido_service.listar_categorias()
        for i, c in enumerate(categorias):
            fondo = COLOR_SUPERFICIE if i % 2 == 0 else COLOR_FONDO_FRAME
            fila = ctk.CTkFrame(
                self._lista_scroll,
                fg_color=fondo,
                corner_radius=6,
                cursor="hand2",
            )
            fila.pack(fill="x", pady=1)

            ctk.CTkLabel(
                fila, text=str(c.id), width=32,
                font=FUENTE_BADGE, text_color=COLOR_TEXTO_SEC,
            ).pack(side="left", padx=6, pady=6)

            ctk.CTkLabel(
                fila, text=c.nombre,
                font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO, anchor="w",
            ).pack(side="left", fill="x", expand=True, padx=4)

            desc_corta = ((c.descripcion or "")[:20] + "…") if len(c.descripcion or "") > 20 else (c.descripcion or "—")
            ctk.CTkLabel(
                fila, text=desc_corta, width=100,
                font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC, anchor="e",
            ).pack(side="right", padx=8)

            handler = lambda e, cid=c.id: self._on_click_fila(cid)
            fila.bind("<Button-1>", handler)
            for child in fila.winfo_children():
                child.bind("<Button-1>", handler)

            self._fila_widgets[c.id] = fila

    def _on_click_fila(self, categoria_id: int):
        """Resalta la fila seleccionada y carga los datos en el formulario."""
        self._deseleccionar_filas()
        fila = self._fila_widgets.get(categoria_id)
        if fila:
            fila.configure(fg_color="#051520", border_width=1, border_color=COLOR_PRIMARIO)
        self._categoria_id_seleccionada = categoria_id

        cats = self.contenido_service.listar_categorias(solo_activas=False)
        cat = next((c for c in cats if c.id == categoria_id), None)
        if cat is None:
            return
        self._entry_nombre.delete(0, "end")
        self._entry_nombre.insert(0, cat.nombre)
        self._entry_desc.delete("1.0", "end")
        self._entry_desc.insert("1.0", cat.descripcion or "")
        self._lbl_error.configure(text="")

    def _deseleccionar_filas(self):
        """Quita el resaltado de selección de todas las filas."""
        for i, (cid, fila) in enumerate(self._fila_widgets.items()):
            fondo = COLOR_SUPERFICIE if i % 2 == 0 else COLOR_FONDO_FRAME
            fila.configure(fg_color=fondo, border_width=0)

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _limpiar(self):
        """Resetea el formulario y deselecciona la fila activa."""
        self._categoria_id_seleccionada = None
        self._entry_nombre.delete(0, "end")
        self._entry_desc.delete("1.0", "end")
        self._lbl_error.configure(text="")
        self._deseleccionar_filas()

    def _guardar(self):
        """Crea o actualiza la categoría según si hay una seleccionada."""
        nombre = self._entry_nombre.get().strip()
        desc = self._entry_desc.get("1.0", "end").strip() or None
        try:
            if self._categoria_id_seleccionada is None:
                self.contenido_service.crear_categoria(nombre, desc)
            else:
                self.contenido_service.actualizar_categoria(
                    self._categoria_id_seleccionada, nombre, desc
                )
            self._lbl_error.configure(text="Guardado correctamente.", text_color=COLOR_EXITO)
            self._cargar_categorias()
            self._limpiar()
        except ValueError as e:
            self._lbl_error.configure(text=str(e), text_color=COLOR_ERROR)

    def _eliminar(self):
        """Solicita confirmación y elimina la categoría seleccionada."""
        if self._categoria_id_seleccionada is None:
            mostrar_aviso(self, "Selecciona una categoría primero.")
            return

        def ejecutar():
            try:
                self.contenido_service.eliminar_categoria(self._categoria_id_seleccionada)
                self._limpiar()
                self._cargar_categorias()
            except ValueError as e:
                mostrar_error(self, str(e))

        confirmar(self, "¿Eliminar la categoría seleccionada?", ejecutar)
