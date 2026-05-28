import customtkinter as ctk
from app.config.settings import (
    COLOR_FONDO_FRAME, COLOR_SUPERFICIE, COLOR_BORDE,
    COLOR_PRIMARIO, COLOR_PRIMARIO_HOVER,
    COLOR_ERROR, COLOR_DORADO,
    COLOR_TEXTO, COLOR_TEXTO_SEC,
    FUENTE_SUBTITULO, FUENTE_NORMAL, FUENTE_PEQUEÑA,
)


def _base(
    master, titulo: str, mensaje: str,
    accent_color: str, icono: str,
    ancho: int = 370, alto: int = 200,
) -> ctk.CTkToplevel:
    """Crea y centra una ventana modal con barra de acento semántica, ícono y mensaje."""
    dialogo = ctk.CTkToplevel(master)
    dialogo.title(titulo)
    dialogo.resizable(False, False)
    dialogo.grab_set()
    dialogo.configure(fg_color=COLOR_FONDO_FRAME)
    dialogo.update_idletasks()
    x = (dialogo.winfo_screenwidth() - ancho) // 2
    y = (dialogo.winfo_screenheight() - alto) // 2
    dialogo.geometry(f"{ancho}x{alto}+{x}+{y}")

    # Barra de acento superior (4 px del color semántico del tipo de diálogo)
    ctk.CTkFrame(dialogo, height=4, corner_radius=0, fg_color=accent_color).pack(fill="x")

    # Fila con ícono + título
    header = ctk.CTkFrame(dialogo, fg_color="transparent")
    header.pack(fill="x", padx=20, pady=(14, 0))
    ctk.CTkLabel(
        header, text=icono,
        font=("Segoe UI", 20), text_color=accent_color,
    ).pack(side="left")
    ctk.CTkLabel(
        header, text=f"  {titulo}",
        font=FUENTE_SUBTITULO, text_color=COLOR_TEXTO,
    ).pack(side="left")

    # Separador
    ctk.CTkFrame(dialogo, height=1, fg_color=COLOR_BORDE).pack(fill="x", padx=20, pady=(10, 0))

    # Mensaje
    ctk.CTkLabel(
        dialogo, text=mensaje,
        font=FUENTE_PEQUEÑA, text_color=COLOR_TEXTO_SEC,
        wraplength=ancho - 40, justify="left",
    ).pack(pady=(12, 14), padx=20, anchor="w")

    return dialogo


def mostrar_error(master, mensaje: str) -> None:
    """Muestra un diálogo modal de error con barra de acento roja."""
    dialogo = _base(master, "Error", mensaje, accent_color=COLOR_ERROR, icono="✕")
    ctk.CTkButton(
        dialogo, text="Aceptar",
        width=130, height=38, corner_radius=8,
        font=FUENTE_NORMAL,
        fg_color=COLOR_ERROR, hover_color="#c53030",
        text_color=COLOR_TEXTO,
        command=dialogo.destroy,
    ).pack(pady=(0, 16))


def mostrar_aviso(master, mensaje: str) -> None:
    """Muestra un diálogo modal informativo con barra de acento cian."""
    dialogo = _base(master, "Aviso", mensaje, accent_color=COLOR_PRIMARIO, icono="ℹ")
    ctk.CTkButton(
        dialogo, text="Aceptar",
        width=130, height=38, corner_radius=8,
        font=FUENTE_NORMAL,
        fg_color=COLOR_PRIMARIO, hover_color=COLOR_PRIMARIO_HOVER,
        text_color="#030712",
        command=dialogo.destroy,
    ).pack(pady=(0, 16))


def confirmar(master, mensaje: str, on_si) -> None:
    """Muestra un diálogo de confirmación con barra dorada; llama a on_si solo si el usuario acepta."""
    dialogo = _base(
        master, "Confirmar acción", mensaje,
        accent_color=COLOR_DORADO, icono="⚠",
        ancho=380, alto=212,
    )

    fila = ctk.CTkFrame(dialogo, fg_color="transparent")
    fila.pack(pady=(0, 16))

    def aceptar():
        dialogo.destroy()
        on_si()

    ctk.CTkButton(
        fila, text="Sí, continuar",
        width=150, height=38, corner_radius=8,
        font=FUENTE_NORMAL,
        fg_color=COLOR_ERROR, hover_color="#c53030",
        text_color=COLOR_TEXTO,
        command=aceptar,
    ).pack(side="left", padx=6)

    ctk.CTkButton(
        fila, text="Cancelar",
        width=150, height=38, corner_radius=8,
        font=FUENTE_NORMAL,
        fg_color="transparent",
        border_width=1, border_color=COLOR_BORDE,
        text_color=COLOR_TEXTO_SEC,
        hover_color=COLOR_SUPERFICIE,
        command=dialogo.destroy,
    ).pack(side="left", padx=6)
