import customtkinter as ctk
from app.config.settings import (
    COLOR_FONDO_FRAME, COLOR_TEXTO, COLOR_ERROR, COLOR_PRIMARIO,
    FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


def _base(master, titulo: str, mensaje: str, ancho: int = 360, alto: int = 160) -> ctk.CTkToplevel:
    """Crea y centra en pantalla una ventana modal con título y mensaje."""
    dialogo = ctk.CTkToplevel(master)
    dialogo.title(titulo)
    dialogo.resizable(False, False)
    dialogo.grab_set()
    dialogo.update_idletasks()
    x = (dialogo.winfo_screenwidth() - ancho) // 2
    y = (dialogo.winfo_screenheight() - alto) // 2
    dialogo.geometry(f"{ancho}x{alto}+{x}+{y}")
    ctk.CTkLabel(dialogo, text=mensaje, font=FUENTE_NORMAL, text_color=COLOR_TEXTO,
                 wraplength=ancho - 40).pack(pady=(24, 16), padx=20)
    return dialogo


def mostrar_error(master, mensaje: str) -> None:
    """Muestra un diálogo modal de error con botón Aceptar."""
    dialogo = _base(master, "Error", mensaje)
    ctk.CTkButton(dialogo, text="Aceptar", width=120, font=FUENTE_NORMAL,
                  fg_color=COLOR_ERROR, hover_color="#a93226",
                  command=dialogo.destroy).pack(pady=(0, 16))


def mostrar_aviso(master, mensaje: str) -> None:
    """Muestra un diálogo modal informativo con botón Aceptar."""
    dialogo = _base(master, "Aviso", mensaje)
    ctk.CTkButton(dialogo, text="Aceptar", width=120, font=FUENTE_NORMAL,
                  fg_color=COLOR_PRIMARIO,
                  command=dialogo.destroy).pack(pady=(0, 16))


def confirmar(master, mensaje: str, on_si) -> None:
    """Muestra un diálogo de confirmación; llama a on_si solo si el usuario acepta."""
    dialogo = _base(master, "Sistema de Trivia", mensaje, ancho=360, alto=160)
    fila = ctk.CTkFrame(dialogo, fg_color="transparent")
    fila.pack()

    def aceptar():
        dialogo.destroy()
        on_si()

    ctk.CTkButton(fila, text="Sí, continuar", width=140, font=FUENTE_NORMAL,
                  fg_color=COLOR_ERROR, hover_color="#a93226",
                  command=aceptar).pack(side="left", padx=8)
    ctk.CTkButton(fila, text="Cancelar", width=140, font=FUENTE_NORMAL,
                  fg_color=COLOR_FONDO_FRAME,
                  command=dialogo.destroy).pack(side="left", padx=8)
