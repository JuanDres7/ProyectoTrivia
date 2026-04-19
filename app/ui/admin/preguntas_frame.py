import tkinter.ttk as ttk
import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.ui.dialogo import mostrar_error, mostrar_aviso, confirmar
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_SECUNDARIO, COLOR_FONDO, COLOR_FONDO_FRAME,
    COLOR_TEXTO, COLOR_ERROR, COLOR_EXITO,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class AdminPreguntasFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService,
                 on_categorias, on_niveles, on_volver):
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0,
                         width=900, height=600)
        self.contenido_service = contenido_service
        self.on_categorias = on_categorias
        self.on_niveles = on_niveles
        self.on_volver = on_volver

        self._pregunta_id_seleccionada: int | None = None
        self._opciones_vars: list[ctk.StringVar] = []
        self._correcta_var = ctk.IntVar(value=0)

        self._construir_ui()
        self._cargar_filtros()
        self._cargar_preguntas()

    # ------------------------------------------------------------------
    # Construcción de la UI
    # ------------------------------------------------------------------

    def _construir_ui(self):
        self.pack_propagate(False)

        # Top bar
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=50, corner_radius=0)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)

        ctk.CTkLabel(top, text="Gestión de Preguntas", font=FUENTE_SUBTITULO,
                     text_color=COLOR_TEXTO).pack(side="left", padx=16, pady=10)

        ctk.CTkButton(top, text="Niveles", width=90, font=FUENTE_PEQUEÑA,
                      fg_color=COLOR_SECUNDARIO, command=self.on_niveles).pack(side="right", padx=6, pady=8)
        ctk.CTkButton(top, text="Categorías", width=100, font=FUENTE_PEQUEÑA,
                      fg_color=COLOR_SECUNDARIO, command=self.on_categorias).pack(side="right", padx=6, pady=8)
        ctk.CTkButton(top, text="← Menú", width=90, font=FUENTE_PEQUEÑA,
                      fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
                      command=self.on_volver).pack(side="right", padx=6, pady=8)

        # Cuerpo
        body = ctk.CTkFrame(self, fg_color=COLOR_FONDO, corner_radius=0)
        body.pack(fill="both", expand=True)

        # Panel izquierdo — lista
        left = ctk.CTkFrame(body, fg_color=COLOR_FONDO_FRAME, corner_radius=8, width=380)
        left.pack(side="left", fill="y", padx=(10, 5), pady=10)
        left.pack_propagate(False)

        ctk.CTkLabel(left, text="Filtrar por nivel:", font=FUENTE_PEQUEÑA,
                     text_color=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10, 2))
        self._filtro_nivel = ctk.CTkOptionMenu(left, values=["Todos"], width=340,
                                                command=lambda _: self._cargar_preguntas())
        self._filtro_nivel.pack(padx=10, pady=(0, 6))

        # Treeview
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=24, font=("Roboto", 11))
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="white",
                        font=("Roboto", 11, "bold"))
        style.map("Treeview", background=[("selected", "#1f6aa5")])

        cols = ("id", "enunciado", "nivel", "estado")
        self._tree = ttk.Treeview(left, columns=cols, show="headings", height=16)
        self._tree.heading("id",       text="ID")
        self._tree.heading("enunciado", text="Enunciado")
        self._tree.heading("nivel",    text="Nivel")
        self._tree.heading("estado",   text="Estado")
        self._tree.column("id",        width=35,  anchor="center")
        self._tree.column("enunciado", width=195)
        self._tree.column("nivel",     width=55,  anchor="center")
        self._tree.column("estado",    width=70,  anchor="center")
        self._tree.tag_configure("inactiva", foreground="#777777")
        self._tree.pack(fill="both", expand=True, padx=10, pady=(0, 6))
        self._tree.bind("<<TreeviewSelect>>", self._on_seleccionar)

        btn_bar = ctk.CTkFrame(left, fg_color="transparent")
        btn_bar.pack(fill="x", padx=10, pady=(0, 10))
        ctk.CTkButton(btn_bar, text="Nueva", font=FUENTE_PEQUEÑA, width=80,
                      fg_color=COLOR_EXITO, text_color="#000000",
                      command=self._limpiar_formulario).pack(side="left")
        self._btn_toggle = ctk.CTkButton(btn_bar, text="Desactivar", font=FUENTE_PEQUEÑA, width=90,
                                          fg_color=COLOR_SECUNDARIO, state="disabled",
                                          command=self._toggle_activa)
        self._btn_toggle.pack(side="left", padx=6)
        ctk.CTkButton(btn_bar, text="Eliminar", font=FUENTE_PEQUEÑA, width=80,
                      fg_color=COLOR_ERROR, command=self._eliminar).pack(side="right")

        # Panel derecho — formulario
        right = ctk.CTkScrollableFrame(body, fg_color=COLOR_FONDO_FRAME,
                                       corner_radius=8, width=460)
        right.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        ctk.CTkLabel(right, text="Enunciado", font=FUENTE_PEQUEÑA,
                     text_color=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10, 2))
        self._entry_enunciado = ctk.CTkTextbox(right, height=70, font=FUENTE_NORMAL)
        self._entry_enunciado.pack(fill="x", padx=10)

        ctk.CTkLabel(right, text="Nivel", font=FUENTE_PEQUEÑA,
                     text_color=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10, 2))
        self._nivel_var = ctk.StringVar()
        self._opt_nivel = ctk.CTkOptionMenu(right, variable=self._nivel_var, values=[""])
        self._opt_nivel.pack(fill="x", padx=10)

        ctk.CTkLabel(right, text="Categoría (opcional)", font=FUENTE_PEQUEÑA,
                     text_color=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(10, 2))
        self._cat_var = ctk.StringVar()
        self._opt_cat = ctk.CTkOptionMenu(right, variable=self._cat_var, values=["Sin categoría"])
        self._opt_cat.pack(fill="x", padx=10)

        ctk.CTkLabel(right, text="Opciones  (marca la correcta)",
                     font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO).pack(anchor="w", padx=10, pady=(14, 4))

        self._opciones_vars = []
        letras = ["A", "B", "C", "D"]
        for i, letra in enumerate(letras):
            row = ctk.CTkFrame(right, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=3)
            ctk.CTkRadioButton(row, text=letra, variable=self._correcta_var,
                               value=i, width=40).pack(side="left")
            var = ctk.StringVar()
            ctk.CTkEntry(row, textvariable=var, placeholder_text=f"Opción {letra}",
                         font=FUENTE_NORMAL).pack(side="left", fill="x", expand=True, padx=(6, 0))
            self._opciones_vars.append(var)

        self._lbl_form_error = ctk.CTkLabel(right, text="", font=FUENTE_PEQUEÑA,
                                             text_color=COLOR_ERROR)
        self._lbl_form_error.pack(pady=(8, 0))

        ctk.CTkButton(right, text="Guardar pregunta", font=FUENTE_NORMAL,
                      fg_color=COLOR_PRIMARIO, command=self._guardar).pack(pady=(6, 16))

    # ------------------------------------------------------------------
    # Carga de datos
    # ------------------------------------------------------------------

    def _cargar_filtros(self):
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
        filtro = self._filtro_nivel.get()
        nivel_id = self._niveles_map.get(filtro) if filtro != "Todos" else None
        preguntas = self.contenido_service.listar_preguntas(nivel_id, solo_activas=False)

        niveles_por_id = {v: k for k, v in self._niveles_map.items()}

        for row in self._tree.get_children():
            self._tree.delete(row)
        for p in preguntas:
            enunciado = p.enunciado if len(p.enunciado) <= 32 else p.enunciado[:29] + "..."
            estado = "Activa" if p.activa else "Inactiva"
            tag = () if p.activa else ("inactiva",)
            self._tree.insert("", "end", iid=str(p.id),
                              values=(p.id, enunciado, niveles_por_id.get(p.nivel_id, "?"), estado),
                              tags=tag)

    # ------------------------------------------------------------------
    # Acciones
    # ------------------------------------------------------------------

    def _on_seleccionar(self, _event=None):
        sel = self._tree.selection()
        if not sel:
            return
        pregunta_id = int(sel[0])
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

    def _actualizar_btn_toggle(self, activa: bool):
        if activa:
            self._btn_toggle.configure(text="Desactivar", fg_color=COLOR_SECUNDARIO, state="normal")
        else:
            self._btn_toggle.configure(text="Activar", fg_color=COLOR_EXITO, text_color="#000000", state="normal")

    def _toggle_activa(self):
        if self._pregunta_id_seleccionada is None:
            return
        try:
            nueva_activa = self.contenido_service.toggle_activa_pregunta(self._pregunta_id_seleccionada)
            self._cargar_preguntas()
            self._actualizar_btn_toggle(nueva_activa)
        except ValueError as e:
            mostrar_error(self, str(e))

    def _limpiar_formulario(self):
        self._pregunta_id_seleccionada = None
        self._entry_enunciado.delete("1.0", "end")
        for var in self._opciones_vars:
            var.set("")
        self._correcta_var.set(0)
        self._lbl_form_error.configure(text="")
        self._btn_toggle.configure(state="disabled", text="Desactivar", fg_color=COLOR_SECUNDARIO)
        self._tree.selection_remove(self._tree.selection())

    def _guardar(self):
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
