"""
Ejecutar una sola vez para inicializar la base de datos:
    python scripts/seed_data.py

Crea:
  - El usuario administrador (admin / admin123)
  - Los 3 niveles de dificultad
  - 6 categorías
  - 75 preguntas (25 por nivel) con sus 4 opciones
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import bcrypt
from sqlmodel import Session, SQLModel
from app.database.database import crear_tablas, engine
from app.database.models.autenticacion import Usuario
from app.database.models.contenido import Categoria, NivelDificultad, Opcion, Pregunta
import app.database.models  # noqa: F401 — registra todos los modelos

# ---------------------------------------------------------------------------
# Datos de preguntas
# Formato: (enunciado, nivel_id, cat_id, [(letra, texto, es_correcta), ...])
# ---------------------------------------------------------------------------

PREGUNTAS = [
    # =====================================================================
    # FÁCIL (nivel_id=1)  — Categorías: Ciencias(1), Historia(2), Geografía(3)
    # =====================================================================
    (
        "¿Cuántos planetas tiene el sistema solar?",
        1, 1,
        [("A", "7", False), ("B", "8", True), ("C", "9", False), ("D", "10", False)],
    ),
    (
        "¿Cuál es el planeta más grande del sistema solar?",
        1, 1,
        [("A", "Saturno", False), ("B", "Neptuno", False), ("C", "Júpiter", True), ("D", "Urano", False)],
    ),
    (
        "¿Qué gas es el más abundante en la atmósfera terrestre?",
        1, 1,
        [("A", "Oxígeno", False), ("B", "Dióxido de carbono", False), ("C", "Argón", False), ("D", "Nitrógeno", True)],
    ),
    (
        "¿Cuántos lados tiene un hexágono?",
        1, 1,
        [("A", "5", False), ("B", "6", True), ("C", "7", False), ("D", "8", False)],
    ),
    (
        "¿Cuál es el símbolo químico del agua?",
        1, 1,
        [("A", "CO2", False), ("B", "NaCl", False), ("C", "H2O", True), ("D", "O2", False)],
    ),
    (
        "¿En qué año llegó el hombre a la Luna por primera vez?",
        1, 2,
        [("A", "1965", False), ("B", "1969", True), ("C", "1972", False), ("D", "1959", False)],
    ),
    (
        "¿Quién fue el primer presidente de los Estados Unidos?",
        1, 2,
        [("A", "Abraham Lincoln", False), ("B", "Thomas Jefferson", False), ("C", "George Washington", True), ("D", "John Adams", False)],
    ),
    (
        "¿En qué año comenzó la Primera Guerra Mundial?",
        1, 2,
        [("A", "1905", False), ("B", "1918", False), ("C", "1914", True), ("D", "1939", False)],
    ),
    (
        "¿Quién pintó la Mona Lisa?",
        1, 2,
        [("A", "Miguel Ángel", False), ("B", "Rafael", False), ("C", "Picasso", False), ("D", "Leonardo da Vinci", True)],
    ),
    (
        "¿En qué continente se encuentra Egipto?",
        1, 3,
        [("A", "Asia", False), ("B", "Europa", False), ("C", "África", True), ("D", "América", False)],
    ),
    (
        "¿Cuál es el océano más grande del mundo?",
        1, 3,
        [("A", "Atlántico", False), ("B", "Índico", False), ("C", "Ártico", False), ("D", "Pacífico", True)],
    ),
    (
        "¿Cuál es la capital de Francia?",
        1, 3,
        [("A", "Londres", False), ("B", "Berlín", False), ("C", "Madrid", False), ("D", "París", True)],
    ),
    (
        "¿Cuál es el río más largo del mundo?",
        1, 3,
        [("A", "Amazonas", False), ("B", "Yangtsé", False), ("C", "Nilo", True), ("D", "Misisipi", False)],
    ),
    (
        "¿Cuántos continentes hay en el mundo?",
        1, 3,
        [("A", "5", False), ("B", "6", False), ("C", "7", True), ("D", "8", False)],
    ),
    (
        "¿Cuál es el animal terrestre más rápido?",
        1, 1,
        [("A", "León", False), ("B", "Guepardo", True), ("C", "Caballo", False), ("D", "Antílope", False)],
    ),
    (
        "¿Cuántos colores tiene el arcoíris?",
        1, 1,
        [("A", "5", False), ("B", "6", False), ("C", "7", True), ("D", "8", False)],
    ),
    (
        "¿Cuál es la capital de Japón?",
        1, 3,
        [("A", "Osaka", False), ("B", "Seúl", False), ("C", "Pekín", False), ("D", "Tokio", True)],
    ),
    (
        "¿Qué instrumento mide la temperatura?",
        1, 1,
        [("A", "Barómetro", False), ("B", "Termómetro", True), ("C", "Higrómetro", False), ("D", "Anemómetro", False)],
    ),
    (
        "¿Quién escribió 'Don Quijote de la Mancha'?",
        1, 2,
        [("A", "Lope de Vega", False), ("B", "Francisco de Quevedo", False), ("C", "Miguel de Cervantes", True), ("D", "Calderón de la Barca", False)],
    ),
    (
        "¿Cuál es el metal más abundante en la corteza terrestre?",
        1, 1,
        [("A", "Hierro", False), ("B", "Cobre", False), ("C", "Aluminio", True), ("D", "Oro", False)],
    ),
    (
        "¿Cuántas horas tiene un día?",
        1, 1,
        [("A", "12", False), ("B", "24", True), ("C", "48", False), ("D", "36", False)],
    ),
    (
        "¿Cuál es el país más grande del mundo por superficie?",
        1, 3,
        [("A", "China", False), ("B", "Canadá", False), ("C", "Estados Unidos", False), ("D", "Rusia", True)],
    ),
    (
        "¿Cuántos huesos tiene el cuerpo humano adulto?",
        1, 1,
        [("A", "106", False), ("B", "186", False), ("C", "206", True), ("D", "256", False)],
    ),
    (
        "¿En qué país se encuentra la Torre Eiffel?",
        1, 3,
        [("A", "Italia", False), ("B", "España", False), ("C", "Francia", True), ("D", "Bélgica", False)],
    ),
    (
        "¿Cuántos segundos tiene un minuto?",
        1, 1,
        [("A", "30", False), ("B", "45", False), ("C", "60", True), ("D", "100", False)],
    ),

    # =====================================================================
    # MEDIO (nivel_id=2) — Categorías: Ciencias(1), Historia(2), Tecnología(4)
    # =====================================================================
    (
        "¿Cuál es la velocidad de la luz en el vacío (aproximada)?",
        2, 1,
        [("A", "150.000 km/s", False), ("B", "300.000 km/s", True), ("C", "500.000 km/s", False), ("D", "1.000.000 km/s", False)],
    ),
    (
        "¿Qué científico formuló la teoría de la relatividad?",
        2, 1,
        [("A", "Isaac Newton", False), ("B", "Nikola Tesla", False), ("C", "Albert Einstein", True), ("D", "Stephen Hawking", False)],
    ),
    (
        "¿Cuántos cromosomas tiene una célula humana normal?",
        2, 1,
        [("A", "23", False), ("B", "44", False), ("C", "46", True), ("D", "48", False)],
    ),
    (
        "¿Cuál es el elemento con número atómico 79?",
        2, 1,
        [("A", "Plata", False), ("B", "Platino", False), ("C", "Cobre", False), ("D", "Oro", True)],
    ),
    (
        "¿Qué órgano produce la insulina?",
        2, 1,
        [("A", "Hígado", False), ("B", "Riñón", False), ("C", "Páncreas", True), ("D", "Bazo", False)],
    ),
    (
        "¿En qué año cayó el Muro de Berlín?",
        2, 2,
        [("A", "1987", False), ("B", "1989", True), ("C", "1991", False), ("D", "1993", False)],
    ),
    (
        "¿Quién fue el primer secretario general de la ONU?",
        2, 2,
        [("A", "Dag Hammarskjöld", False), ("B", "Kofi Annan", False), ("C", "U Thant", False), ("D", "Trygve Lie", True)],
    ),
    (
        "¿En qué año se fundó la Organización de las Naciones Unidas?",
        2, 2,
        [("A", "1941", False), ("B", "1945", True), ("C", "1948", False), ("D", "1950", False)],
    ),
    (
        "¿Qué civilización construyó Machu Picchu?",
        2, 2,
        [("A", "Azteca", False), ("B", "Maya", False), ("C", "Inca", True), ("D", "Olmeca", False)],
    ),
    (
        "¿En qué año fue la Revolución Francesa?",
        2, 2,
        [("A", "1776", False), ("B", "1789", True), ("C", "1804", False), ("D", "1815", False)],
    ),
    (
        "¿Quién inventó el teléfono?",
        2, 4,
        [("A", "Thomas Edison", False), ("B", "Nikola Tesla", False), ("C", "Alexander Graham Bell", True), ("D", "Guglielmo Marconi", False)],
    ),
    (
        "¿En qué año fue lanzado el primer iPhone?",
        2, 4,
        [("A", "2005", False), ("B", "2006", False), ("C", "2007", True), ("D", "2008", False)],
    ),
    (
        "¿Qué lenguaje de programación creó Guido van Rossum?",
        2, 4,
        [("A", "Java", False), ("B", "Ruby", False), ("C", "Python", True), ("D", "Perl", False)],
    ),
    (
        "¿Cuántos bits tiene un byte?",
        2, 4,
        [("A", "4", False), ("B", "8", True), ("C", "16", False), ("D", "32", False)],
    ),
    (
        "¿Qué significa 'CPU' en informática?",
        2, 4,
        [("A", "Central Processing Unit", True), ("B", "Computer Power Unit", False), ("C", "Central Program Utility", False), ("D", "Core Processing Unit", False)],
    ),
    (
        "¿Cuál es la fórmula de la segunda ley de Newton?",
        2, 1,
        [("A", "E = mc²", False), ("B", "F = ma", True), ("C", "P = mv", False), ("D", "W = Fd", False)],
    ),
    (
        "¿Cuál es la tabla periódica usada actualmente?",
        2, 1,
        [("A", "Tabla de Bohr", False), ("B", "Tabla de Lavoisier", False), ("C", "Tabla de Mendeleev", True), ("D", "Tabla de Dalton", False)],
    ),
    (
        "¿Qué planeta tiene los anillos más visibles?",
        2, 1,
        [("A", "Júpiter", False), ("B", "Urano", False), ("C", "Neptuno", False), ("D", "Saturno", True)],
    ),
    (
        "¿En qué año se publicó la primera versión de Windows?",
        2, 4,
        [("A", "1981", False), ("B", "1983", False), ("C", "1985", True), ("D", "1990", False)],
    ),
    (
        "¿Cuál es el hueso más largo del cuerpo humano?",
        2, 1,
        [("A", "Húmero", False), ("B", "Tibia", False), ("C", "Fémur", True), ("D", "Radio", False)],
    ),
    (
        "¿Qué gas producen las plantas durante la fotosíntesis?",
        2, 1,
        [("A", "Dióxido de carbono", False), ("B", "Nitrógeno", False), ("C", "Hidrógeno", False), ("D", "Oxígeno", True)],
    ),
    (
        "¿Cuántas vértebras tiene la columna vertebral humana?",
        2, 1,
        [("A", "24", False), ("B", "30", False), ("C", "33", True), ("D", "36", False)],
    ),
    (
        "¿Cuál es el protocolo base de la World Wide Web?",
        2, 4,
        [("A", "FTP", False), ("B", "SMTP", False), ("C", "HTTP", True), ("D", "SSH", False)],
    ),
    (
        "¿En qué año se hundió el Titanic?",
        2, 2,
        [("A", "1910", False), ("B", "1912", True), ("C", "1914", False), ("D", "1916", False)],
    ),
    (
        "¿Cuál fue el primer satélite artificial lanzado al espacio?",
        2, 2,
        [("A", "Explorer 1", False), ("B", "Vostok 1", False), ("C", "Sputnik 1", True), ("D", "Luna 1", False)],
    ),

    # =====================================================================
    # DIFÍCIL (nivel_id=3) — Categorías: Ciencias(1), Arte(5), Economía(6)
    # =====================================================================
    (
        "¿Cuál es la constante de Planck aproximada?",
        3, 1,
        [("A", "6.626 × 10⁻³⁴ J·s", True), ("B", "3.14 × 10⁻²³ J·s", False), ("C", "9.109 × 10⁻³¹ J·s", False), ("D", "1.602 × 10⁻¹⁹ J·s", False)],
    ),
    (
        "¿Qué teorema establece que todo sistema formal suficientemente potente es incompleto?",
        3, 1,
        [("A", "Teorema de Fermat", False), ("B", "Teorema de Gödel", True), ("C", "Teorema de Bayes", False), ("D", "Teorema de Cantor", False)],
    ),
    (
        "¿Cuál es el nombre del proceso por el que una estrella colapsa en un agujero negro?",
        3, 1,
        [("A", "Fusión nuclear", False), ("B", "Supernova de tipo Ia", False), ("C", "Colapso gravitacional", True), ("D", "Nebulosa planetaria", False)],
    ),
    (
        "¿En qué año publicó Darwin 'El origen de las especies'?",
        3, 1,
        [("A", "1851", False), ("B", "1855", False), ("C", "1859", True), ("D", "1863", False)],
    ),
    (
        "¿Qué partícula subatómica tiene carga negativa?",
        3, 1,
        [("A", "Protón", False), ("B", "Neutrón", False), ("C", "Electrón", True), ("D", "Quark up", False)],
    ),
    (
        "¿Cuál es la distancia media de la Tierra al Sol en unidades astronómicas?",
        3, 1,
        [("A", "0.5 UA", False), ("B", "1 UA", True), ("C", "2 UA", False), ("D", "5 UA", False)],
    ),
    (
        "¿Quién descubrió la penicilina?",
        3, 1,
        [("A", "Louis Pasteur", False), ("B", "Robert Koch", False), ("C", "Joseph Lister", False), ("D", "Alexander Fleming", True)],
    ),
    (
        "¿Cuál es el nombre del proceso por el que el ADN se convierte en ARN?",
        3, 1,
        [("A", "Traducción", False), ("B", "Replicación", False), ("C", "Transcripción", True), ("D", "Transducción", False)],
    ),
    (
        "¿Qué pintor es conocido por el 'Período Azul' y el 'Período Rosa'?",
        3, 5,
        [("A", "Salvador Dalí", False), ("B", "Pablo Picasso", True), ("C", "Joan Miró", False), ("D", "Henri Matisse", False)],
    ),
    (
        "¿En qué ciudad se encuentra el museo del Louvre?",
        3, 5,
        [("A", "Roma", False), ("B", "Londres", False), ("C", "Madrid", False), ("D", "París", True)],
    ),
    (
        "¿Quién compuso la Novena Sinfonía siendo sordo?",
        3, 5,
        [("A", "Wolfgang Amadeus Mozart", False), ("B", "Johann Sebastian Bach", False), ("C", "Ludwig van Beethoven", True), ("D", "Franz Schubert", False)],
    ),
    (
        "¿Cómo se llama la técnica pictórica que usa puntos de color puro?",
        3, 5,
        [("A", "Impresionismo", False), ("B", "Puntillismo", True), ("C", "Cubismo", False), ("D", "Fauvismo", False)],
    ),
    (
        "¿Qué arquitecto diseñó la Sagrada Familia de Barcelona?",
        3, 5,
        [("A", "Le Corbusier", False), ("B", "Frank Lloyd Wright", False), ("C", "Antoni Gaudí", True), ("D", "Ludwig Mies van der Rohe", False)],
    ),
    (
        "¿Qué escritor ganó el Premio Nobel de Literatura en 1982?",
        3, 5,
        [("A", "Julio Cortázar", False), ("B", "Mario Vargas Llosa", False), ("C", "Gabriel García Márquez", True), ("D", "Jorge Luis Borges", False)],
    ),
    (
        "¿Cuál es el nombre de la obra de arte más cara vendida en subasta (2023)?",
        3, 5,
        [("A", "Salvator Mundi – Da Vinci", True), ("B", "Shot Sage Blue Marilyn – Warhol", False), ("C", "Les Femmes d'Alger – Picasso", False), ("D", "Interchange – de Kooning", False)],
    ),
    (
        "¿Qué economista escribió 'La riqueza de las naciones'?",
        3, 6,
        [("A", "John Maynard Keynes", False), ("B", "Karl Marx", False), ("C", "Adam Smith", True), ("D", "David Ricardo", False)],
    ),
    (
        "¿Cómo se llama el fenómeno económico de aumento generalizado de precios?",
        3, 6,
        [("A", "Deflación", False), ("B", "Recesión", False), ("C", "Estanflación", False), ("D", "Inflación", True)],
    ),
    (
        "¿Qué sigla identifica al Fondo Monetario Internacional?",
        3, 6,
        [("A", "BID", False), ("B", "BM", False), ("C", "FMI", True), ("D", "OMC", False)],
    ),
    (
        "¿Cuál es el PIB nominal de un país?",
        3, 6,
        [("A", "Valor ajustado por inflación de todos los bienes y servicios", False),
         ("B", "Valor de mercado de todos los bienes y servicios producidos en un año", True),
         ("C", "Total de exportaciones menos importaciones", False),
         ("D", "Ingreso promedio per cápita de la población", False)],
    ),
    (
        "¿Qué teoría económica defiende la intervención del Estado para regular la demanda?",
        3, 6,
        [("A", "Monetarismo", False), ("B", "Liberalismo clásico", False), ("C", "Keynesianismo", True), ("D", "Marxismo", False)],
    ),
    (
        "¿Cuál es la moneda oficial de la Unión Europea?",
        3, 6,
        [("A", "Franco", False), ("B", "Marco", False), ("C", "Euro", True), ("D", "ECU", False)],
    ),
    (
        "¿Qué indica el índice de Gini?",
        3, 6,
        [("A", "El crecimiento del PIB", False), ("B", "La desigualdad en la distribución del ingreso", True), ("C", "El nivel de desempleo", False), ("D", "La balanza comercial", False)],
    ),
    (
        "¿Cuál es la tasa de interés que cobra un banco central a los bancos comerciales?",
        3, 6,
        [("A", "Tasa de usura", False), ("B", "Tasa de descuento", True), ("C", "Tasa de cambio", False), ("D", "Tasa marginal", False)],
    ),
    (
        "¿Qué enfermedad estudia la epidemiología?",
        3, 1,
        [("A", "Solo enfermedades infecciosas", False), ("B", "Solo enfermedades crónicas", False), ("C", "Enfermedades mentales exclusivamente", False), ("D", "Distribución y determinantes de enfermedades en poblaciones", True)],
    ),
    (
        "¿Cuál es el nombre del proceso termodinámico sin intercambio de calor?",
        3, 1,
        [("A", "Isotérmico", False), ("B", "Isobárico", False), ("C", "Adiabático", True), ("D", "Isocórico", False)],
    ),
]


def seed():
    # Eliminar todas las tablas y recrearlas para partir desde cero
    SQLModel.metadata.drop_all(engine)
    crear_tablas()

    with Session(engine) as session:

        # --- Admin ---
        password_hash = bcrypt.hashpw("admin123".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        session.add(Usuario(username="admin", password_hash=password_hash))

        # --- Niveles de dificultad ---
        for nivel in [
            NivelDificultad(id=1, nombre="Fácil",   num_preguntas=10, tiempo_limite_seg=30),
            NivelDificultad(id=2, nombre="Medio",   num_preguntas=15, tiempo_limite_seg=25),
            NivelDificultad(id=3, nombre="Difícil", num_preguntas=20, tiempo_limite_seg=20),
        ]:
            session.add(nivel)

        # --- Categorías ---
        categorias_data = [
            (1, "Ciencias",    "Física, química, biología y astronomía"),
            (2, "Historia",    "Eventos y personajes históricos"),
            (3, "Geografía",   "Países, capitales, ríos y relieves"),
            (4, "Tecnología",  "Informática, internet e inventos"),
            (5, "Arte",        "Pintura, música, literatura y arquitectura"),
            (6, "Economía",    "Finanzas, macroeconomía y teoría económica"),
        ]
        for cid, nombre, desc in categorias_data:
            session.add(Categoria(id=cid, nombre=nombre, descripcion=desc))

        session.flush()  # genera los IDs antes de usarlos en preguntas

        # --- Preguntas y opciones ---
        for enunciado, nivel_id, cat_id, opciones in PREGUNTAS:
            pregunta = Pregunta(enunciado=enunciado, nivel_id=nivel_id, categoria_id=cat_id)
            session.add(pregunta)
            session.flush()
            for letra, texto, es_correcta in opciones:
                session.add(Opcion(
                    pregunta_id=pregunta.id,
                    letra=letra,
                    texto=texto,
                    es_correcta=es_correcta,
                ))

        session.commit()

        facil   = sum(1 for _, n, *_ in PREGUNTAS if n == 1)
        medio   = sum(1 for _, n, *_ in PREGUNTAS if n == 2)
        dificil = sum(1 for _, n, *_ in PREGUNTAS if n == 3)

        print("Base de datos inicializada correctamente.")
        print(f"  Categorías: {len(categorias_data)}")
        print(f"  Preguntas:  {len(PREGUNTAS)}  (Fácil: {facil}  Medio: {medio}  Difícil: {dificil})")
        print("  Usuario: admin  |  Contraseña: admin123")


if __name__ == "__main__":
    seed()