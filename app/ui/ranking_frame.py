import tkinter.ttk as ttk
import customtkinter as ctk
from app.database.models.partidas import Ranking
from app.config.settings import (
    COLOR_PRIMARIO, COLOR_FONDO_FRAME, COLOR_TEXTO,
    FUENTE_TITULO, FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


class RankingFrame(ctk.CTkFrame):

    def __init__(self, master, top10: list[tuple[Ranking, str]], on_volver):
        super().__init__(master, fg_color=COLOR_FONDO_FRAME, corner_radius=16)
        self.top10 = top10
        self.on_volver = on_volver
        self._construir_ui()

    def _construir_ui(self):
        self.columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Top 10 Jugadores", font=FUENTE_TITULO,
                     text_color=COLOR_TEXTO).grid(row=0, column=0, pady=(32, 4))
        ctk.CTkLabel(self, text="Mejores puntajes de todos los tiempos", font=FUENTE_PEQUEÑA,
                     text_color="#aaaaaa").grid(row=1, column=0, pady=(0, 20))

        # ── Tabla ─────────────────────────────────────────────────────
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#2b2b2b", foreground="white",
                        fieldbackground="#2b2b2b", rowheight=28, font=("Roboto", 11))
        style.configure("Treeview.Heading", background="#1f6aa5", foreground="white",
                        font=("Roboto", 11, "bold"))
        style.map("Treeview", background=[("selected", "#2b2b2b")])

        cols = ("pos", "jugador_id", "nombre", "puntaje", "record")
        tree = ttk.Treeview(self, columns=cols, show="headings", height=10, selectmode="none")
        tree.heading("pos",        text="#")
        tree.heading("jugador_id", text="Jugador ID")
        tree.heading("nombre",     text="Nombre")
        tree.heading("puntaje",    text="Puntaje")
        tree.heading("record",     text="Récord")
        tree.column("pos",        width=50,  anchor="center")
        tree.column("jugador_id", width=90,  anchor="center")
        tree.column("nombre",     width=180, anchor="w")
        tree.column("puntaje",    width=90,  anchor="center")
        tree.column("record",     width=70,  anchor="center")
        tree.grid(row=2, column=0, padx=40, pady=(0, 8), sticky="ew")

        if self.top10:
            for pos, entrada in enumerate(self.top10, start=1):
                record_txt = "Record" if entrada.es_record_global else ""
                tree.insert("", "end", values=(pos, entrada.jugador_id, entrada.nombre, entrada.puntaje, record_txt))
        else:
            tree.insert("", "end", values=("—", "—", "Aún no hay partidas", "—", ""))

        # ── Volver ────────────────────────────────────────────────────
        ctk.CTkButton(self, text="Volver al menú", width=220, font=FUENTE_NORMAL,
                      fg_color="transparent", border_width=1, text_color=COLOR_TEXTO,
                      command=self.on_volver).grid(row=3, column=0, pady=(12, 32))
