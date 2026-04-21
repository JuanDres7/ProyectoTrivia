import tkinter.ttk as ttk
import customtkinter as ctk
from app.database.models.partidas import Ranking
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_FONDO, COLOR_FONDO_FRAME, COLOR_TEXTO,
    COLOR_EXITO, FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA, COLOR_ERROR,
)


class ResultadoFrame(ctk.CTkFrame):

    def __init__(self, master, nombre_jugador: str, puntaje: int,
                 es_record: bool, record_anterior: int,
                 top10: list[Ranking], on_volver):
        """Inicializa la pantalla de resultado con el puntaje y el estado de récord."""
        super().__init__(master, fg_color=COLOR_FONDO, corner_radius=0, width=900, height=600)
        self.nombre_jugador = nombre_jugador
        self.puntaje = puntaje
        self.es_record = es_record
        self.record_anterior = record_anterior
        self.top10 = top10
        self.on_volver = on_volver
        self._construir_ui()

    def _construir_ui(self):
        """Construye el panel de resultado del jugador y la tabla del top 10 junto a él."""
        self.pack_propagate(False)

        # Panel izquierdo — resultado
        left = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, corner_radius=12, width=380)
        left.pack(side="left", fill="y", padx=(20, 10), pady=20)
        left.pack_propagate(False)
        left.columnconfigure(0, weight=1)

        ctk.CTkLabel(left, text="Resultado", font=FUENTE_SUBTITULO,
                     text_color="#aaaaaa").grid(row=0, column=0, pady=(30, 4))

        ctk.CTkLabel(left, text=self.nombre_jugador, font=FUENTE_TITULO,
                     text_color=COLOR_TEXTO).grid(row=1, column=0, pady=(0, 16))

        ctk.CTkLabel(left, text=str(self.puntaje), font=("Roboto", 64, "bold"),
                     text_color=COLOR_EXITO).grid(row=2, column=0)
        ctk.CTkLabel(left, text="puntos", font=FUENTE_NORMAL,
                     text_color="#aaaaaa").grid(row=3, column=0, pady=(0, 20))

        if self.es_record:
            ctk.CTkLabel(left, text="¡Nuevo récord alcanzado!",
                         font=FUENTE_SUBTITULO, text_color="#f1c40f").grid(row=4, column=0, pady=8)
        else:
            ctk.CTkLabel(left, text="No superaste el record actual" + "\nIntenta nuevamente",
                         font=FUENTE_SUBTITULO, text_color=COLOR_ERROR).grid(row=4, column=0, pady=8)
            ctk.CTkLabel(
                left,
                text=f"Récord actual: {self.record_anterior} pts",
                font=FUENTE_PEQUEÑA, text_color="#888888",
            ).grid(row=5, column=0, pady=8)

        ctk.CTkButton(left, text="Volver al menú", width=260, font=FUENTE_NORMAL,
                      fg_color=COLOR_PRIMARIO, command=self.on_volver).grid(row=6, column=0, pady=(20, 30))

        # Panel derecho — Top 10
        right = ctk.CTkFrame(self, fg_color=COLOR_FONDO_FRAME, corner_radius=12)
        right.pack(side="left", fill="both", expand=True, padx=(10, 20), pady=20)

        ctk.CTkLabel(right, text="Top 10 Jugadores", font=FUENTE_SUBTITULO,
                     text_color=COLOR_TEXTO).pack(pady=(16, 10))

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=26, font=("Roboto", 11))
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="white",
                        font=("Roboto", 11, "bold"))
        style.map("Treeview", background=[("selected", "#2b2b2b")])

        cols = ("pos", "jugador_id", "nombre", "puntaje")
        tree = ttk.Treeview(right, columns=cols, show="headings", height=10, selectmode="none")
        tree.heading("pos", text="#")
        tree.heading("jugador_id", text="Jugador ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("puntaje", text="Puntaje")
        tree.column("pos", width=40, anchor="center")
        tree.column("jugador_id", width=80, anchor="center")
        tree.column("nombre", width=120, anchor="w")
        tree.column("puntaje", width=70, anchor="center")
        tree.tag_configure("top1", foreground="#f1c40f")
        tree.pack(padx=16, pady=(0, 16), fill="both", expand=True)

        for pos, entrada in enumerate(self.top10, start=1):
            tag = ("top1",) if pos == 1 else ()
            tree.insert("", "end", values=(pos, entrada.jugador_id, entrada.nombre, entrada.puntaje), tags=tag)
