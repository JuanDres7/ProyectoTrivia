import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.ui.otros.dialogo import mostrar_error, mostrar_aviso, confirmar
from app.config.settings import (
    COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_SECUNDARIO, COLOR_SECUNDARIO_HOVER,
    COLOR_EXITO, COLOR_ERROR,
    COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA, FUENTE_BADGE,
)


class AdminPreguntasFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService,
                 on_categorias, on_niveles, on_volver):
        """Inicializa el panel de preguntas y carga filtros y lista inicial."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0)
        self.contenido_service = contenido_service
        self.on_categorias = on_categorias
        self.on_niveles = on_niveles
        self.on_volver = on_volver

        self._pregunta_id_seleccionada: int | None = None
        self._fila_widgets: dict[int, ctk.CTkFrame] = {}
        self._filas_activa: dict[int, bool] = {}
        self._opciones_vars: list[ctk.StringVar] = []
        self._correcta_var = ctk.IntVar(value=0)

        self._construir_ui()
        self._cargar_filtros()
        self._cargar_preguntas()

    # ------------------------------------------------------------------
    # Construcción de la UI
    # ------------------------------------------------------------------

    def _construir_ui(self):
        """Construye la barra superior, el listado con filtro y el formulario de pregunta."""
        # ── Top bar ───────────────────────────────────────────────────
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=54, corner_radius=0)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        ctk.CTkLabel(
            top, text="⚙  GESTIÓN DE PREGUNTAS",
            font=FUENTE_SUBTITULO, text_color=COLOR_TEXTO,
        ).pack(side="left", padx=20)

        for texto, cmd in [
            ("← Menú", self.on_volver),
            ("Categorías", self.on_categorias),
            ("Niveles", self.on_niveles),
        ]:
            ctk.CTkButton(
                top, text=texto,
                width=100, height=34, corner_radius=8,
                font=FUENTE_PEQUEÑA,
                fg_color="transparent",
                border_width=1, border_color=COLOR_BORDE,
                text_color=COLOR_TEXTO_SEC,
                hover_color=COLOR_SUPERFICIE,
                command=cmd,
            ).pack(side="right", padx=5, pady=10)

        ctk.CTkFrame(self, height=1, fg_color=COLOR_BORDE, corner_radius=0).pack(fill="x")

        # ── Cuerpo ────────────────────────────────────────────────────
        body = ctk.CTkFrame(self, fg_color="transparent", corner_radius=0)
        body.pack(fill="both", expand=True)

        # ── Panel izquierdo — lista ───────────────────────────────────
        left = ctk.CTkFrame(
            body,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDE,
            width=360,
        )
        left.pack(side="left", fill="y", padx=(12, 6), pady=12)
        left.pack_propagate(False)

        # Filtro por nivel
        ctk.CTkLabel(
            left, text="Filtrar por nivel",
            font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
        ).pack(anchor="w", padx=14, pady=(12, 3))

        self._filtro_nivel = ctk.CTkOptionMenu(
            left, values=["Todos"],
            fg_color=COLOR_SUPERFICIE,
            button_color=COLOR_FONDO_FRAME,
            button_hover_color=COLOR_PRIMARIO,
            dropdown_fg_color=COLOR_FONDO_FRAME,
            dropdown_text_color=COLOR_TEXTO,
            dropdown_hover_color=COLOR_SUPERFICIE,
            text_color=COLOR_TEXTO,
            command=lambda _: self._cargar_preguntas(),
        )
        self._filtro_nivel.pack(fill="x", padx=10, pady=(0, 8))

        # Cabecera de tabla
        header = ctk.CTkFrame(left, fg_color=COLOR_PRIMARIO, corner_radius=8, height=30)
        header.pack(fill="x", padx=10, pady=(0, 2))
        header.pack_propagate(False)
        ctk.CTkLabel(header, text="#", width=28, font=FUENTE_BADGE, text_color="#080812").pack(side="left", padx=4)
        ctk.CTkLabel(header, text="Enunciado", font=FUENTE_BADGE, text_color="#080812", anchor="w").pack(side="left", fill="x", expand=True)
        ctk.CTkLabel(header, text="Nivel", width=68, font=FUENTE_BADGE, text_color="#080812").pack(side="left")
        ctk.CTkLabel(header, text="●", width=24, font=FUENTE_BADGE, text_color="#080812").pack(side="right", padx=4)

        # Scrollable con las filas
        self._lista_scroll = ctk.CTkScrollableFrame(
            left, fg_color="transparent", corner_radius=0,
        )
        self._lista_scroll.pack(fill="both", expand=True, padx=10, pady=(0, 8))

        # Botones de acción de lista
        btn_bar = ctk.CTkFrame(left, fg_color="transparent")
        btn_bar.pack(fill="x", padx=10, pady=(0, 10))

        ctk.CTkButton(
            btn_bar, text="Nueva",
            width=76, height=34, corner_radius=8,
            font=FUENTE_PEQUEÑA,
            fg_color=COLOR_EXITO, hover_color="#1db358",
            text_color="#080812",
            command=self._limpiar_formulario,
        ).pack(side="left")

        self._btn_toggle = ctk.CTkButton(
            btn_bar, text="Desactivar",
            width=90, height=34, corner_radius=8,
            font=FUENTE_PEQUEÑA,
            fg_color=COLOR_SECUNDARIO, hover_color=COLOR_SECUNDARIO_HOVER,
            text_color=COLOR_TEXTO,
            state="disabled",
            command=self._toggle_activa,
        )
        self._btn_toggle.pack(side="left", padx=5)

        ctk.CTkButton(
            btn_bar, text="Eliminar",
            width=76, height=34, corner_radius=8,
            font=FUENTE_PEQUEÑA,
            fg_color=COLOR_ERROR, hover_color="#c53030",
            text_color=COLOR_TEXTO,
            command=self._eliminar,
        ).pack(side="right")

        # ── Panel derecho — formulario ────────────────────────────────
        right = ctk.CTkScrollableFrame(
            body,
            fg_color=COLOR_FONDO_FRAME,
            corner_radius=10,
            border_width=1,
            border_color=COLOR_BORDE,
        )
        right.pack(side="left", fill="both", expand=True, padx=(6, 12), pady=12)

        def _label_campo(texto):
            ctk.CTkLabel(
                right, text=texto,
                font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
            ).pack(anchor="w", padx=14, pady=(14, 3))

        _label_campo("Enunciado *")
        self._entry_enunciado = ctk.CTkTextbox(
            right, height=80, font=FUENTE_NORMAL,
            fg_color=COLOR_SUPERFICIE,
            border_color=COLOR_BORDE, border_width=2,
            text_color=COLOR_TEXTO,
        )
        self._entry_enunciado.pack(fill="x", padx=14)

        _label_campo("Nivel *")
        self._nivel_var = ctk.StringVar()
        self._opt_nivel = ctk.CTkOptionMenu(
            right, variable=self._nivel_var, values=[""],
            fg_color=COLOR_SUPERFICIE,
            button_color=COLOR_FONDO_FRAME,
            button_hover_color=COLOR_PRIMARIO,
            dropdown_fg_color=COLOR_FONDO_FRAME,
            dropdown_text_color=COLOR_TEXTO,
            dropdown_hover_color=COLOR_SUPERFICIE,
            text_color=COLOR_TEXTO,
        )
        self._opt_nivel.pack(fill="x", padx=14)

        _label_campo("Categoría  (opcional)")
        self._cat_var = ctk.StringVar()
        self._opt_cat = ctk.CTkOptionMenu(
            right, variable=self._cat_var, values=["Sin categoría"],
            fg_color=COLOR_SUPERFICIE,
            button_color=COLOR_FONDO_FRAME,
            button_hover_color=COLOR_PRIMARIO,
            dropdown_fg_color=COLOR_FONDO_FRAME,
            dropdown_text_color=COLOR_TEXTO,
            dropdown_hover_color=COLOR_SUPERFICIE,
            text_color=COLOR_TEXTO,
        )
        self._opt_cat.pack(fill="x", padx=14)

        _label_campo("Opciones  (marca la correcta ◉)")

        self._opciones_vars = []
        for i, letra in enumerate(["A", "B", "C", "D"]):
            fila = ctk.CTkFrame(right, fg_color="transparent")
            fila.pack(fill="x", padx=14, pady=3)
            ctk.CTkRadioButton(
                fila, text=letra,
                variable=self._correcta_var, value=i,
                width=40,
                fg_color=COLOR_PRIMARIO,
                hover_color=COLOR_PRIMARIO_HOVER,
                text_color=COLOR_TEXTO,
                border_color=COLOR_BORDE,
            ).pack(side="left")
            var = ctk.StringVar()
            ctk.CTkEntry(
                fila, textvariable=var,
                placeholder_text=f"Opción {letra}",
                font=FUENTE_NORMAL,
                fg_color=COLOR_SUPERFICIE,
                border_color=COLOR_BORDE, border_width=2,
                text_color=COLOR_TEXTO,
            ).pack(side="left", fill="x", expand=True, padx=(8, 0))
            self._opciones_vars.append(var)

        self._lbl_form_error = ctk.CTkLabel(
            right, text="", font=FUENTE_PEQUEÑA, text_color=COLOR_ERROR,
        )
        self._lbl_form_error.pack(pady=(10, 0))

        ctk.CTkButton(
            right, text="Guardar pregunta",
            height=44, corner_radius=10,
            font=FUENTE_NORMAL,
            fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO_HOVER,
            text_color="#030712",
            command=self._guardar,
        ).pack(fill="x", padx=14, pady=(8, 20))

    # ------------------------------------------------------------------
    # Carga de datos
    # ------------------------------------------------------------------

    def _cargar_filtros(self):
        """Rellena los desplegables de nivel y categoría con los datos del servicio."""
        niveles = self.contenido_service.listar_niveles()
        self._niveles_map = {n.nombre: n.id for n in niveles}
        self._filtro_nivel.configure(values=["Todos"] + list(self._niveles_map.keys()))

        categorias = self.contenido_service.listar_categorias()
        self._categorias_map = {"Sin categoría": None}
        for c in categorias:
            self._categorias_map[c.nombre] = c.id
        self._opt_nivel.configure(values=list(self._niveles_map.keys()))
        if niveles:
            self._nivel_var.set(niveles[0].nombre)
        self._opt_cat.configure(values=list(self._categorias_map.keys()))
        self._cat_var.set("Sin categoría")

    def _cargar_preguntas(self):
        """Reconstruye las filas de la lista con el filtro de nivel activo."""
        filtro = self._filtro_nivel.get()
        nivel_id = self._niveles_map.get(filtro) if filtro != "Todos" else None
        preguntas = self.contenido_service.listar_preguntas(nivel_id, solo_activas=False)
        niveles_por_id = {v: k for k, v in self._niveles_map.items()}

        for fila in self._fila_widgets.values():
            fila.destroy()
        self._fila_widgets.clear()
        self._filas_activa.clear()

        for p in preguntas:
            self._filas_activa[p.id] = p.activa
            fondo = COLOR_SUPERFICIE if p.activa else COLOR_FONDO_FRAME
            color_txt = COLOR_TEXTO if p.activa else COLOR_TEXTO_SEC

            fila = ctk.CTkFrame(
                self._lista_scroll,
                fg_color=fondo,
                corner_radius=6,
                cursor="hand2",
            )
            fila.pack(fill="x", pady=1)

            enunciado = (p.enunciado[:30] + "…") if len(p.enunciado) > 30 else p.enunciado
            nivel_txt = niveles_por_id.get(p.nivel_id, "?")

            ctk.CTkLabel(fila, text=str(p.id), width=28, font=FUENTE_BADGE,
                         text_color=COLOR_TEXTO_SEC).pack(side="left", padx=4, pady=6)
            ctk.CTkLabel(fila, text=enunciado, font=FUENTE_PEQUEÑA,
                         text_color=color_txt, anchor="w").pack(side="left", fill="x", expand=True, padx=2)
            ctk.CTkLabel(fila, text=nivel_txt, width=68, font=FUENTE_BADGE,
                         text_color=COLOR_PRIMARIO if p.activa else COLOR_TEXTO_SEC).pack(side="left")
            ctk.CTkLabel(fila, text="●", width=22, font=("Segoe UI", 10),
                         text_color=COLOR_EXITO if p.activa else COLOR_ERROR).pack(side="right", padx=4)

            handler = lambda e, pid=p.id: self._on_click_fila(pid)
            fila.bind("<Button-1>", handler)
            for child in fila.winfo_children():
                child.bind("<Button-1>", handler)

            self._fila_widgets[p.id] = fila

    # ------------------------------------------------------------------
    # Selección interactiva
    # ------------------------------------------------------------------

    def _on_click_fila(self, pregunta_id: int):
        """Resalta la fila seleccionada y carga sus datos en el formulario."""
        self._deseleccionar_filas()
        fila = self._fila_widgets.get(pregunta_id)
        if fila:
            fila.configure(fg_color="#051520", border_width=1, border_color=COLOR_PRIMARIO)
        self._pregunta_id_seleccionada = pregunta_id
        try:
            pregunta, opciones = self.contenido_service.obtener_pregunta_con_opciones(pregunta_id)
        except ValueError:
            return

        self._entry_enunciado.delete("1.0", "end")
        self._entry_enunciado.insert("1.0", pregunta.enunciado)

        nivel_nombre = next((k for k, v in self._niveles_map.items() if v == pregunta.nivel_id), "")
        self._nivel_var.set(nivel_nombre)

        cat_nombre = next((k for k, v in self._categorias_map.items() if v == pregunta.categoria_id), "Sin categoría")
        self._cat_var.set(cat_nombre)

        for i, op in enumerate(sorted(opciones, key=lambda o: o.letra)):
            if i < 4:
                self._opciones_vars[i].set(op.texto)
                if op.es_correcta:
                    self._correcta_var.set(i)

        self._lbl_form_error.configure(text="")
        self._actualizar_btn_toggle(pregunta.activa)

    def _deseleccionar_filas(self):
        """Quita el resaltado de selección de todas las filas."""
        for pid, fila in self._fila_widgets.items():
            activa = self._filas_activa.get(pid, True)
            fondo = COLOR_SUPERFICIE if activa else COLOR_FONDO_FRAME
            fila.configure(fg_color=fondo, border_width=0)

    def _actualizar_btn_toggle(self, activa: bool):
        """Actualiza el texto y color del botón activar/desactivar según el estado."""
        if activa:
            self._btn_toggle.configure(
                text="Desactivar",
                fg_color=COLOR_SECUNDARIO, hover_color=COLOR_SECUNDARIO_HOVER,
                text_color=COLOR_TEXTO, state="normal",
            )
        else:
            self._btn_toggle.configure(
                text="Activar",
                fg_color=COLOR_EXITO, hover_color="#1db358",
                text_color="#080812", state="normal",
            )

    # ------------------------------------------------------------------
    # Acciones del formulario
    # ------------------------------------------------------------------

    def _limpiar_formulario(self):
        """Vacía todos los campos del formulario y deselecciona la tabla."""
        self._pregunta_id_seleccionada = None
        self._entry_enunciado.delete("1.0", "end")
        for var in self._opciones_vars:
            var.set("")
        self._correcta_var.set(0)
        self._lbl_form_error.configure(text="")
        self._btn_toggle.configure(
            state="disabled", text="Desactivar",
            fg_color=COLOR_SECUNDARIO, text_color=COLOR_TEXTO,
        )
        self._deseleccionar_filas()

    def _toggle_activa(self):
        """Activa o desactiva la pregunta seleccionada y refresca la lista."""
        if self._pregunta_id_seleccionada is None:
            return
        try:
            nueva_activa = self.contenido_service.toggle_activa_pregunta(self._pregunta_id_seleccionada)
            self._cargar_preguntas()
            self._actualizar_btn_toggle(nueva_activa)
        except ValueError as e:
            mostrar_error(self, str(e))

    def _guardar(self):
        """Crea o actualiza la pregunta con sus opciones según si hay una seleccionada."""
        enunciado = self._entry_enunciado.get("1.0", "end").strip()
        nivel_id = self._niveles_map.get(self._nivel_var.get())
        cat_id = self._categorias_map.get(self._cat_var.get())
        letras = ["A", "B", "C", "D"]
        opciones = [
            {"letra": letras[i], "texto": self._opciones_vars[i].get().strip(),
             "es_correcta": (i == self._correcta_var.get())}
            for i in range(4)
        ]
        try:
            if self._pregunta_id_seleccionada is None:
                self.contenido_service.crear_pregunta(enunciado, nivel_id, opciones, cat_id)
            else:
                self.contenido_service.actualizar_pregunta(
                    self._pregunta_id_seleccionada, enunciado, nivel_id, opciones, cat_id
                )
            self._lbl_form_error.configure(text="Guardado correctamente.", text_color=COLOR_EXITO)
            self._cargar_preguntas()
            self._limpiar_formulario()
        except ValueError as e:
            self._lbl_form_error.configure(text=str(e), text_color=COLOR_ERROR)

    def _eliminar(self):
        """Solicita confirmación y elimina la pregunta seleccionada."""
        if self._pregunta_id_seleccionada is None:
            mostrar_aviso(self, "Selecciona una pregunta primero.")
            return

        def ejecutar():
            try:
                self.contenido_service.eliminar_pregunta(self._pregunta_id_seleccionada)
                self._limpiar_formulario()
                self._cargar_preguntas()
            except ValueError as e:
                mostrar_error(self, str(e))

        confirmar(self, "¿Eliminar la pregunta seleccionada?", ejecutar)
