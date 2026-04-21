import tkinter.ttk as ttk
import customtkinter as ctk
from app.services.contenido_service import ContenidoService
from app.config.settings import (
    COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_TEXTO,
    FUENTE_SUBTITULO, FUENTE_PEQUEÑA,
)


class AdminNivelesFrame(ctk.CTkFrame):

    def __init__(self, master, contenido_service: ContenidoService, on_volver):
        """Inicializa la pantalla de niveles y carga la tabla."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0, width=900, height=600)
        self.contenido_service = contenido_service
        self.on_volver = on_volver
        self._construir_ui()
        self._cargar_niveles()

    def _construir_ui(self):
        """Construye la barra superior y la tabla de solo lectura con los niveles."""
        self.pack_propagate(False)

        # Top bar
        top = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, height=50, corner_radius=0)
        top.pack(fill="x", side="top")
        top.pack_propagate(False)
        ctk.CTkLabel(top, text="Niveles de Dificultad", font=FUENTE_SUBTITULO,
                     text_color=COLOR_TEXTO).pack(side="left", padx=16, pady=10)
        ctk.CTkButton(top, text="← Preguntas", width=110, font=FUENTE_PEQUEÑA,
                      fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
                      command=self.on_volver).pack(side="right", padx=12, pady=8)

        # Tabla
        container = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, corner_radius=8, width=600)
        container.pack(pady=10)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=28, font=("Roboto", 12))
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="white",
                        font=("Roboto", 12, "bold"))
        style.map("Treeview", background=[("selected", "#2b2b2b")])

        cols = ("id", "nombre", "preguntas", "tiempo")
        self._tree = ttk.Treeview(container, columns=cols, show="headings",
                                  height=5, selectmode="none")
        self._tree.heading("id", text="ID")
        self._tree.heading("nombre", text="Nivel")
        self._tree.heading("preguntas", text="N° Preguntas")
        self._tree.heading("tiempo", text="Tiempo / Pregunta (seg)")
        self._tree.column("id", width=50, anchor="center")
        self._tree.column("nombre", width=150, anchor="center")
        self._tree.column("preguntas", width=150, anchor="center")
        self._tree.column("tiempo", width=200, anchor="center")
        self._tree.pack(padx=10, pady=10)

    def _cargar_niveles(self):
        """Rellena la tabla con los niveles obtenidos del servicio."""
        niveles = self.contenido_service.listar_niveles()
        for n in niveles:
            self._tree.insert("", "end", values=(n.id, n.nombre, n.num_preguntas, n.tiempo_limite_seg))
