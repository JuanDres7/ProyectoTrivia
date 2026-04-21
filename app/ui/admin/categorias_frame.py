import tkinter.ttk as ttk
import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.ui.otros.dialogo import mostrar_error, mostrar_aviso, confirmar
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_TEXTO,
    COLOR_ERROR, COLOR_EXITO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class AdminCategoriasFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService, on_volver):
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0, width=900, height=600)
        self.contenido_service = contenido_service
        self.on_volver = on_volver
        self._categoria_id_seleccionada: int | None = None
        self._construir_ui()
        self._cargar_categorias()

    def _construir_ui(self):
        self.pack_propagate(False)

        # Top bar
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=50, corner_radius=0)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)
        ctk.CTkLabel(top, text="Gestión de Categorías", font=FUENTE_SUBTITULO,
                     text_color=COLOR_TEXTO).pack(side="left", padx=16, pady=10)
        ctk.CTkButton(top, text="← Preguntas", width=110, font=FUENTE_PEQUEÑA,
                      fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
                      command=self.on_volver).pack(side="right", padx=12, pady=8)

        # Cuerpo
        body = ctk.CTkFrame(self, fg_color=COLOR_FONDO, corner_radius=0)
        body.pack(fill="both", expand=True)

        # Lista
        left = ctk.CTkFrame(body, fg_color=COLOR_FONDO_FRAME, corner_radius=8, width=420)
        left.pack(side="left", fill="y", padx=(10, 5), pady=10)
        left.pack_propagate(False)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=24, font=("Roboto", 11))
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="white",
                        font=("Roboto", 11, "bold"))
        style.map("Treeview", background=[("selected", "#1f6aa5")])

        cols = ("id", "nombre", "descripcion")
        self._tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
        self._tree.heading("id", text="ID")
        self._tree.heading("nombre", text="Nombre")
        self._tree.heading("descripcion", text="Descripción")
        self._tree.column("id", width=35, anchor="center")
        self._tree.column("nombre", width=150)
        self._tree.column("descripcion", width=200)
        self._tree.pack(fill="both", expand=True, padx=10, pady=10)
        self._tree.bind("<<TreeviewSelect>>", self._on_seleccionar)

        # Formulario
        right = ctk.CTkFrame(body, fg_color=COLOR_FONDO_FRAME, corner_radius=8)
        right.pack(side="left", fill="both", expand=True, padx=(5, 10), pady=10)

        ctk.CTkLabel(right, text="Nombre", font=FUENTE_PEQUEÑA,
                     text_color=COLOR_TEXTO).pack(anchor="w", padx=16, pady=(20, 2))
        self._entry_nombre = ctk.CTkEntry(right, font=FUENTE_NORMAL, width=340)
        self._entry_nombre.pack(padx=16)

        ctk.CTkLabel(right, text="Descripción (opcional)", font=FUENTE_PEQUEÑA,
                     text_color=COLOR_TEXTO).pack(anchor="w", padx=16, pady=(14, 2))
        self._entry_desc = ctk.CTkTextbox(right, height=80, font=FUENTE_NORMAL, width=340)
        self._entry_desc.pack(padx=16)

        self._lbl_error = ctk.CTkLabel(right, text="", font=FUENTE_PEQUEÑA,
                                        text_color=COLOR_ERROR)
        self._lbl_error.pack(pady=(10, 0))

        btn_row = ctk.CTkFrame(right, fg_color="transparent")
        btn_row.pack(pady=12)
        ctk.CTkButton(btn_row, text="Nueva", width=100, font=FUENTE_NORMAL,
                      fg_color=COLOR_EXITO, text_color="#000000",
                      command=self._limpiar).pack(side="left", padx=6)
        ctk.CTkButton(btn_row, text="Guardar", width=100, font=FUENTE_NORMAL,
                      fg_color=COLOR_PRIMARIO, command=self._guardar).pack(side="left", padx=6)
        ctk.CTkButton(btn_row, text="Eliminar", width=100, font=FUENTE_NORMAL,
                      fg_color=COLOR_ERROR, command=self._eliminar).pack(side="left", padx=6)

    def _cargar_categorias(self):
        categorias = self.contenido_service.listar_categorias()
        for row in self._tree.get_children():
            self._tree.delete(row)
        for c in categorias:
            desc = (c.descripcion or "")[:40]
            self._tree.insert("", "end", iid=str(c.id), values=(c.id, c.nombre, desc))

    def _on_seleccionar(self, _event=None):
        sel = self._tree.selection()
        if not sel:
            return
        self._categoria_id_seleccionada = int(sel[0])
        cat = self.contenido_service.listar_categorias(solo_activas=False)
        cat = next((c for c in cat if c.id == self._categoria_id_seleccionada), None)
        if cat is None:
            return
        self._entry_nombre.delete(0, "end")
        self._entry_nombre.insert(0, cat.nombre)
        self._entry_desc.delete("1.0", "end")
        self._entry_desc.insert("1.0", cat.descripcion or "")
        self._lbl_error.configure(text="")

    def _limpiar(self):
        self._categoria_id_seleccionada = None
        self._entry_nombre.delete(0, "end")
        self._entry_desc.delete("1.0", "end")
        self._lbl_error.configure(text="")
        self._tree.selection_remove(self._tree.selection())

    def _guardar(self):
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
