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

PREGUNTAS_ADICIONALES = [
    # =====================================================================
    # FÁCIL — Historia (cat 2) — +8
    # =====================================================================
    (
        "¿En qué año terminó la Segunda Guerra Mundial?",
        1, 2,
        [("A", "1941", False), ("B", "1943", False), ("C", "1945", True), ("D", "1947", False)],
    ),
    (
        "¿Qué civilización construyó las pirámides de Giza?",
        1, 2,
        [("A", "Griega", False), ("B", "Romana", False), ("C", "Mesopotámica", False), ("D", "Egipcia", True)],
    ),
    (
        "¿En qué país nació Simón Bolívar?",
        1, 2,
        [("A", "Colombia", False), ("B", "Venezuela", True), ("C", "Perú", False), ("D", "Ecuador", False)],
    ),
    (
        "¿Quién fue el primer hombre en orbitar la Tierra?",
        1, 2,
        [("A", "Neil Armstrong", False), ("B", "Buzz Aldrin", False), ("C", "Yuri Gagarin", True), ("D", "Alan Shepard", False)],
    ),
    (
        "¿En qué año llegó Cristóbal Colón a América?",
        1, 2,
        [("A", "1488", False), ("B", "1490", False), ("C", "1492", True), ("D", "1498", False)],
    ),
    (
        "¿En qué año cayó Constantinopla ante los otomanos?",
        1, 2,
        [("A", "1389", False), ("B", "1415", False), ("C", "1453", True), ("D", "1492", False)],
    ),
    (
        "¿Cuál fue el imperio conocido como 'el imperio en el que no se ponía el sol'?",
        1, 2,
        [("A", "Imperio Romano", False), ("B", "Imperio Español", False), ("C", "Imperio Mongol", False), ("D", "Imperio Británico", True)],
    ),
    (
        "¿Quién fue el último faraón del Antiguo Egipto?",
        1, 2,
        [("A", "Tutankamón", False), ("B", "Ramsés II", False), ("C", "Cleopatra", True), ("D", "Nefertiti", False)],
    ),

    # =====================================================================
    # FÁCIL — Geografía (cat 3) — +4
    # =====================================================================
    (
        "¿Cuál es la montaña más alta del mundo?",
        1, 3,
        [("A", "K2", False), ("B", "Mont Blanc", False), ("C", "Kilimanjaro", False), ("D", "Everest", True)],
    ),
    (
        "¿Cuál es el desierto más grande del mundo?",
        1, 3,
        [("A", "Gobi", False), ("B", "Sahara", True), ("C", "Atacama", False), ("D", "Kalahari", False)],
    ),
    (
        "¿Cuál es la capital de España?",
        1, 3,
        [("A", "Barcelona", False), ("B", "Sevilla", False), ("C", "Valencia", False), ("D", "Madrid", True)],
    ),
    (
        "¿Cuál es la capital de Italia?",
        1, 3,
        [("A", "Milán", False), ("B", "Nápoles", False), ("C", "Roma", True), ("D", "Florencia", False)],
    ),

    # =====================================================================
    # FÁCIL — Tecnología (cat 4) — +12
    # =====================================================================
    (
        "¿Qué empresa desarrolló el sistema operativo Windows?",
        1, 4,
        [("A", "Apple", False), ("B", "Google", False), ("C", "Microsoft", True), ("D", "IBM", False)],
    ),
    (
        "¿Qué significa 'USB'?",
        1, 4,
        [("A", "Universal Software Bus", False), ("B", "Unified Serial Board", False), ("C", "Universal Serial Bus", True), ("D", "Unique System Bridge", False)],
    ),
    (
        "¿Qué significa 'PDF'?",
        1, 4,
        [("A", "Personal Data File", False), ("B", "Portable Document Format", True), ("C", "Print Display Format", False), ("D", "Program Data File", False)],
    ),
    (
        "¿Qué significa 'RAM' en informática?",
        1, 4,
        [("A", "Random Access Memory", True), ("B", "Read-only Array Module", False), ("C", "Rapid Application Mode", False), ("D", "Remote Access Management", False)],
    ),
    (
        "¿Qué empresa creó el iPhone?",
        1, 4,
        [("A", "Samsung", False), ("B", "Google", False), ("C", "Apple", True), ("D", "Huawei", False)],
    ),
    (
        "¿Qué significa 'GPS'?",
        1, 4,
        [("A", "General Processing System", False), ("B", "Global Positioning System", True), ("C", "Graphic Processing Software", False), ("D", "Ground Patrol Signal", False)],
    ),
    (
        "¿Para qué sirve un antivirus?",
        1, 4,
        [("A", "Acelerar la computadora", False), ("B", "Editar documentos", False), ("C", "Proteger contra software malicioso", True), ("D", "Mejorar la pantalla", False)],
    ),
    (
        "¿Cuántos colores primarios tiene una pantalla RGB?",
        1, 4,
        [("A", "2", False), ("B", "3", True), ("C", "4", False), ("D", "7", False)],
    ),
    (
        "¿Qué atajo de teclado deshace una acción en la mayoría de programas?",
        1, 4,
        [("A", "Ctrl+Z", True), ("B", "Ctrl+X", False), ("C", "Ctrl+D", False), ("D", "Alt+F4", False)],
    ),
    (
        "¿Qué significa 'Wi-Fi'?",
        1, 4,
        [("A", "Wired Fidelity", False), ("B", "Wide Frequency", False), ("C", "Wireless Fidelity", True), ("D", "Web Interface", False)],
    ),
    (
        "¿Cuál es el sistema operativo de Apple para computadoras?",
        1, 4,
        [("A", "Windows", False), ("B", "Linux", False), ("C", "Android", False), ("D", "macOS", True)],
    ),
    (
        "¿Qué dispositivo conecta una red doméstica a internet?",
        1, 4,
        [("A", "Impresora", False), ("B", "Escáner", False), ("C", "Módem", True), ("D", "Monitor", False)],
    ),

    # =====================================================================
    # FÁCIL — Arte (cat 5) — +12
    # =====================================================================
    (
        "¿Quién pintó 'La noche estrellada'?",
        1, 5,
        [("A", "Picasso", False), ("B", "Monet", False), ("C", "Van Gogh", True), ("D", "Dalí", False)],
    ),
    (
        "¿Cuántas cuerdas tiene una guitarra estándar?",
        1, 5,
        [("A", "4", False), ("B", "5", False), ("C", "6", True), ("D", "7", False)],
    ),
    (
        "¿Quién escribió 'Romeo y Julieta'?",
        1, 5,
        [("A", "Dickens", False), ("B", "Shakespeare", True), ("C", "Cervantes", False), ("D", "Dante", False)],
    ),
    (
        "¿Cuántas notas tiene la escala musical?",
        1, 5,
        [("A", "5", False), ("B", "6", False), ("C", "7", True), ("D", "8", False)],
    ),
    (
        "¿Quién esculpió 'El David' en Florencia?",
        1, 5,
        [("A", "Rafael", False), ("B", "Leonardo da Vinci", False), ("C", "Donatello", False), ("D", "Miguel Ángel", True)],
    ),
    (
        "¿Cuántos músicos forman un cuarteto?",
        1, 5,
        [("A", "2", False), ("B", "3", False), ("C", "4", True), ("D", "5", False)],
    ),
    (
        "¿En qué país se encuentra el Coliseo Romano?",
        1, 5,
        [("A", "Grecia", False), ("B", "España", False), ("C", "Francia", False), ("D", "Italia", True)],
    ),
    (
        "¿Qué color se obtiene mezclando rojo y azul?",
        1, 5,
        [("A", "Verde", False), ("B", "Naranja", False), ("C", "Morado", True), ("D", "Marrón", False)],
    ),
    (
        "¿Cuántas líneas tiene un soneto?",
        1, 5,
        [("A", "10", False), ("B", "12", False), ("C", "14", True), ("D", "16", False)],
    ),
    (
        "¿Qué instrumento toca un violinista?",
        1, 5,
        [("A", "Viola", False), ("B", "Violín", True), ("C", "Cello", False), ("D", "Contrabajo", False)],
    ),
    (
        "¿Qué museo alberga la Mona Lisa?",
        1, 5,
        [("A", "Museo del Prado", False), ("B", "British Museum", False), ("C", "Louvre", True), ("D", "Uffizi", False)],
    ),
    (
        "¿Qué instrumento de viento-madera es este: flauta?",
        1, 5,
        [("A", "Trompeta", False), ("B", "Trombón", False), ("C", "Flauta", True), ("D", "Tuba", False)],
    ),

    # =====================================================================
    # FÁCIL — Economía (cat 6) — +12
    # =====================================================================
    (
        "¿Cuál es la moneda de Estados Unidos?",
        1, 6,
        [("A", "Euro", False), ("B", "Libra", False), ("C", "Dólar", True), ("D", "Peso", False)],
    ),
    (
        "¿Qué es un banco?",
        1, 6,
        [("A", "Empresa de transporte", False), ("B", "Institución que guarda y presta dinero", True), ("C", "Organismo del gobierno", False), ("D", "Tienda de valores", False)],
    ),
    (
        "¿Qué es el ahorro?",
        1, 6,
        [("A", "Dinero que se gasta hoy", False), ("B", "Dinero invertido en bolsa", False), ("C", "Dinero reservado para el futuro", True), ("D", "Dinero prestado", False)],
    ),
    (
        "¿Qué significa exportar?",
        1, 6,
        [("A", "Comprar productos del extranjero", False), ("B", "Vender productos a otros países", True), ("C", "Consumir bienes locales", False), ("D", "Importar materias primas", False)],
    ),
    (
        "¿Qué significa 'IVA'?",
        1, 6,
        [("A", "Índice de Valor Acumulado", False), ("B", "Impuesto al Valor Agregado", True), ("C", "Inversión en Valor Añadido", False), ("D", "Índice de Ventas Anuales", False)],
    ),
    (
        "¿Cuál es la moneda de México?",
        1, 6,
        [("A", "Sol", False), ("B", "Bolívar", False), ("C", "Peso", True), ("D", "Quetzal", False)],
    ),
    (
        "¿Qué es el desempleo?",
        1, 6,
        [("A", "Trabajar tiempo parcial", False), ("B", "No poder trabajar por enfermedad", False), ("C", "Buscar trabajo y no encontrarlo", True), ("D", "Trabajar informalmente", False)],
    ),
    (
        "¿Qué es un impuesto?",
        1, 6,
        [("A", "Donación voluntaria al gobierno", False), ("B", "Pago obligatorio al Estado", True), ("C", "Préstamo del banco", False), ("D", "Inversión pública", False)],
    ),
    (
        "¿Cuál es la moneda de la Unión Europea?",
        1, 6,
        [("A", "Franco", False), ("B", "Marco", False), ("C", "Corona", False), ("D", "Euro", True)],
    ),
    (
        "¿Qué es el salario?",
        1, 6,
        [("A", "Beneficio de vender", False), ("B", "Pago recibido por trabajo realizado", True), ("C", "Impuesto al trabajador", False), ("D", "Préstamo del empleador", False)],
    ),
    (
        "¿Qué ocurre con el precio cuando sube la demanda y la oferta no cambia?",
        1, 6,
        [("A", "El precio baja", False), ("B", "El precio sube", True), ("C", "El precio queda igual", False), ("D", "La empresa cierra", False)],
    ),
    (
        "¿Qué es una empresa?",
        1, 6,
        [("A", "Solo una tienda física", False), ("B", "Organización que produce bienes o servicios", True), ("C", "Agencia del gobierno", False), ("D", "Banco privado", False)],
    ),

    # =====================================================================
    # MEDIO — Ciencias (cat 1) — +6
    # =====================================================================
    (
        "¿Cuál es el punto de ebullición del agua a nivel del mar?",
        2, 1,
        [("A", "80 °C", False), ("B", "90 °C", False), ("C", "100 °C", True), ("D", "120 °C", False)],
    ),
    (
        "¿Qué partícula tiene carga positiva en el núcleo atómico?",
        2, 1,
        [("A", "Electrón", False), ("B", "Neutrón", False), ("C", "Positrón", False), ("D", "Protón", True)],
    ),
    (
        "¿Cuál es la unidad de medida de la corriente eléctrica?",
        2, 1,
        [("A", "Voltio", False), ("B", "Amperio", True), ("C", "Ohmio", False), ("D", "Vatio", False)],
    ),
    (
        "¿Qué tipo de ondas son la luz visible y los rayos X?",
        2, 1,
        [("A", "Mecánicas", False), ("B", "Sonoras", False), ("C", "Electromagnéticas", True), ("D", "Gravitacionales", False)],
    ),
    (
        "¿Cuál es el número atómico del carbono?",
        2, 1,
        [("A", "4", False), ("B", "6", True), ("C", "8", False), ("D", "12", False)],
    ),
    (
        "¿Qué proceso convierte la glucosa en energía dentro de las células?",
        2, 1,
        [("A", "Fotosíntesis", False), ("B", "Fermentación alcohólica", False), ("C", "Respiración celular", True), ("D", "Osmosis", False)],
    ),

    # =====================================================================
    # MEDIO — Historia (cat 2) — +10
    # =====================================================================
    (
        "¿En qué año comenzó la Segunda Guerra Mundial?",
        2, 2,
        [("A", "1935", False), ("B", "1937", False), ("C", "1939", True), ("D", "1941", False)],
    ),
    (
        "¿Qué fue la Guerra Fría?",
        2, 2,
        [("A", "Conflicto armado entre EE.UU. y la URSS", False), ("B", "Tensión política e ideológica entre EE.UU. y la URSS sin combate directo", True), ("C", "Guerra entre países europeos por colonias", False), ("D", "Conflicto militar en el Ártico", False)],
    ),
    (
        "¿Quién lideró la India hacia la independencia mediante resistencia pacífica?",
        2, 2,
        [("A", "Nehru", False), ("B", "Gandhi", True), ("C", "Jinnah", False), ("D", "Tagore", False)],
    ),
    (
        "¿En qué año terminó la Primera Guerra Mundial?",
        2, 2,
        [("A", "1916", False), ("B", "1917", False), ("C", "1918", True), ("D", "1919", False)],
    ),
    (
        "¿Qué fue el Plan Marshall?",
        2, 2,
        [("A", "Plan para invadir la URSS", False), ("B", "Estrategia militar de la OTAN", False), ("C", "Ayuda económica de EE.UU. para reconstruir Europa tras la Segunda Guerra Mundial", True), ("D", "Tratado de paz de la Segunda Guerra Mundial", False)],
    ),
    (
        "¿Quién fue Nelson Mandela?",
        2, 2,
        [("A", "Líder de la Revolución Cubana", False), ("B", "Primer ministro de India", False), ("C", "Presidente sudafricano que luchó contra el apartheid", True), ("D", "Secretario general de la ONU", False)],
    ),
    (
        "¿En qué año se firmó la Declaración de Independencia de Estados Unidos?",
        2, 2,
        [("A", "1773", False), ("B", "1776", True), ("C", "1781", False), ("D", "1789", False)],
    ),
    (
        "¿Qué país lanzó las bombas atómicas sobre Hiroshima y Nagasaki?",
        2, 2,
        [("A", "Reino Unido", False), ("B", "URSS", False), ("C", "Estados Unidos", True), ("D", "Francia", False)],
    ),
    (
        "¿Quién fue Napoleón Bonaparte?",
        2, 2,
        [("A", "Rey de España", False), ("B", "Primer ministro inglés", False), ("C", "Zar ruso", False), ("D", "Emperador francés y brillante estratega militar", True)],
    ),
    (
        "¿Qué fue la Revolución Industrial?",
        2, 2,
        [("A", "Revolución política en Francia", False), ("B", "Transformación de una economía agrícola a una industrial", True), ("C", "Guerra entre potencias industriales", False), ("D", "Movimiento obrero del siglo XX", False)],
    ),

    # =====================================================================
    # MEDIO — Geografía (cat 3) — +17
    # =====================================================================
    (
        "¿Cuál es la capital de Brasil?",
        2, 3,
        [("A", "São Paulo", False), ("B", "Río de Janeiro", False), ("C", "Brasilia", True), ("D", "Belo Horizonte", False)],
    ),
    (
        "¿Cuál es el país más pequeño del mundo?",
        2, 3,
        [("A", "Mónaco", False), ("B", "San Marino", False), ("C", "Vaticano", True), ("D", "Liechtenstein", False)],
    ),
    (
        "¿Cuál es la capital de Australia?",
        2, 3,
        [("A", "Sídney", False), ("B", "Melbourne", False), ("C", "Brisbane", False), ("D", "Canberra", True)],
    ),
    (
        "¿En cuántos husos horarios se divide la Tierra?",
        2, 3,
        [("A", "12", False), ("B", "18", False), ("C", "24", True), ("D", "36", False)],
    ),
    (
        "¿Cuál es la cordillera más larga del mundo?",
        2, 3,
        [("A", "Himalayas", False), ("B", "Los Andes", True), ("C", "Montañas Rocosas", False), ("D", "Los Alpes", False)],
    ),
    (
        "¿Cuántos países tiene el continente africano?",
        2, 3,
        [("A", "44", False), ("B", "49", False), ("C", "54", True), ("D", "60", False)],
    ),
    (
        "¿Qué océano separa Europa de América?",
        2, 3,
        [("A", "Índico", False), ("B", "Pacífico", False), ("C", "Atlántico", True), ("D", "Ártico", False)],
    ),
    (
        "¿Cuál es la capital de Alemania?",
        2, 3,
        [("A", "Múnich", False), ("B", "Hamburgo", False), ("C", "Fráncfort", False), ("D", "Berlín", True)],
    ),
    (
        "¿Cuál es la capital de Rusia?",
        2, 3,
        [("A", "San Petersburgo", False), ("B", "Moscú", True), ("C", "Vladivostok", False), ("D", "Novosibirsk", False)],
    ),
    (
        "¿Cuál es el país con mayor superficie en América del Sur?",
        2, 3,
        [("A", "Argentina", False), ("B", "Colombia", False), ("C", "Brasil", True), ("D", "Perú", False)],
    ),
    (
        "¿Cuál es el estrecho que une el mar Mediterráneo con el océano Atlántico?",
        2, 3,
        [("A", "Estrecho de Magallanes", False), ("B", "Estrecho de Ormuz", False), ("C", "Estrecho de Gibraltar", True), ("D", "Canal de Suez", False)],
    ),
    (
        "¿Cuál es el punto más alto de América del Sur?",
        2, 3,
        [("A", "Monte Roraima", False), ("B", "Huascarán", False), ("C", "Aconcagua", True), ("D", "Chimborazo", False)],
    ),
    (
        "¿Cuál es la capital de China?",
        2, 3,
        [("A", "Shanghái", False), ("B", "Pekín", True), ("C", "Cantón", False), ("D", "Chongqing", False)],
    ),
    (
        "¿En qué continente se encuentra la mayor parte de la selva amazónica?",
        2, 3,
        [("A", "África", False), ("B", "Asia", False), ("C", "América del Norte", False), ("D", "América del Sur", True)],
    ),
    (
        "¿Cuál es el país más poblado de América Latina?",
        2, 3,
        [("A", "México", False), ("B", "Argentina", False), ("C", "Colombia", False), ("D", "Brasil", True)],
    ),
    (
        "¿Qué mar separa la Península Ibérica de África?",
        2, 3,
        [("A", "Mar Negro", False), ("B", "Mar Rojo", False), ("C", "Mar Mediterráneo", True), ("D", "Mar del Norte", False)],
    ),
    (
        "¿Cuál es el río más caudaloso del mundo?",
        2, 3,
        [("A", "Nilo", False), ("B", "Amazonas", True), ("C", "Yangtsé", False), ("D", "Misisipi", False)],
    ),

    # =====================================================================
    # MEDIO — Tecnología (cat 4) — +10
    # =====================================================================
    (
        "¿Qué es un algoritmo?",
        2, 4,
        [("A", "Tipo de virus informático", False), ("B", "Lenguaje de programación", False), ("C", "Secuencia de pasos para resolver un problema", True), ("D", "Sistema operativo", False)],
    ),
    (
        "¿Qué lenguaje se usa principalmente para estructurar páginas web?",
        2, 4,
        [("A", "Python", False), ("B", "Java", False), ("C", "HTML", True), ("D", "SQL", False)],
    ),
    (
        "¿Qué significa 'IP' en redes informáticas?",
        2, 4,
        [("A", "Internal Program", False), ("B", "Internet Protocol", True), ("C", "Input Process", False), ("D", "Integrated Platform", False)],
    ),
    (
        "¿Cuál es la función principal de un sistema operativo?",
        2, 4,
        [("A", "Navegar por internet", False), ("B", "Editar videos", False), ("C", "Gestionar los recursos del hardware", True), ("D", "Proteger contra virus", False)],
    ),
    (
        "¿Qué significa 'URL'?",
        2, 4,
        [("A", "Universal Remote Login", False), ("B", "Uniform Resource Locator", True), ("C", "Unique Reference Link", False), ("D", "User Resource Library", False)],
    ),
    (
        "¿Quién cofundó Apple junto con Steve Jobs?",
        2, 4,
        [("A", "Bill Gates", False), ("B", "Steve Wozniak", True), ("C", "Elon Musk", False), ("D", "Mark Zuckerberg", False)],
    ),
    (
        "¿Qué es el código binario?",
        2, 4,
        [("A", "Sistema numérico en base 10", False), ("B", "Código secreto de cifrado", False), ("C", "Sistema numérico en base 2 (0 y 1)", True), ("D", "Tipo de cifrado asimétrico", False)],
    ),
    (
        "¿Qué empresa desarrolló el sistema operativo Android?",
        2, 4,
        [("A", "Apple", False), ("B", "Microsoft", False), ("C", "Samsung", False), ("D", "Google", True)],
    ),
    (
        "¿Qué es la computación en la nube?",
        2, 4,
        [("A", "Usar internet sin cables", False), ("B", "Almacenar y procesar datos en servidores remotos", True), ("C", "Un tipo de antivirus", False), ("D", "Computadora portátil ultraligera", False)],
    ),
    (
        "¿Qué es una base de datos relacional?",
        2, 4,
        [("A", "Base de datos sin estructura", False), ("B", "Sistema de archivos plano", False), ("C", "Base de datos organizada en tablas vinculadas entre sí", True), ("D", "Red social de datos", False)],
    ),

    # =====================================================================
    # MEDIO — Arte (cat 5) — +16
    # =====================================================================
    (
        "¿Quién pintó 'El Guernica'?",
        2, 5,
        [("A", "Dalí", False), ("B", "Miró", False), ("C", "Picasso", True), ("D", "Velázquez", False)],
    ),
    (
        "¿En qué ciudad se encuentra el Museo del Prado?",
        2, 5,
        [("A", "Barcelona", False), ("B", "Madrid", True), ("C", "Sevilla", False), ("D", "Valencia", False)],
    ),
    (
        "¿Quién compuso 'Las cuatro estaciones'?",
        2, 5,
        [("A", "Bach", False), ("B", "Mozart", False), ("C", "Beethoven", False), ("D", "Vivaldi", True)],
    ),
    (
        "¿Quién escribió 'Cien años de soledad'?",
        2, 5,
        [("A", "Cortázar", False), ("B", "Neruda", False), ("C", "García Márquez", True), ("D", "Vargas Llosa", False)],
    ),
    (
        "¿Qué movimiento artístico representa Salvador Dalí?",
        2, 5,
        [("A", "Impresionismo", False), ("B", "Cubismo", False), ("C", "Surrealismo", True), ("D", "Expresionismo", False)],
    ),
    (
        "¿Quién pintó 'Las Meninas'?",
        2, 5,
        [("A", "Goya", False), ("B", "Velázquez", True), ("C", "Murillo", False), ("D", "El Greco", False)],
    ),
    (
        "¿Quién esculpió 'La Piedad' en el Vaticano?",
        2, 5,
        [("A", "Donatello", False), ("B", "Bernini", False), ("C", "Rafael", False), ("D", "Miguel Ángel", True)],
    ),
    (
        "¿En qué ciudad se encuentra el museo MoMA?",
        2, 5,
        [("A", "Londres", False), ("B", "París", False), ("C", "Nueva York", True), ("D", "Chicago", False)],
    ),
    (
        "¿Qué movimiento artístico se asocia con Claude Monet?",
        2, 5,
        [("A", "Cubismo", False), ("B", "Surrealismo", False), ("C", "Impresionismo", True), ("D", "Expresionismo", False)],
    ),
    (
        "¿Quién escribió 'La Odisea'?",
        2, 5,
        [("A", "Virgilio", False), ("B", "Homero", True), ("C", "Platón", False), ("D", "Sófocles", False)],
    ),
    (
        "¿Qué arquitecto diseñó el Museo Guggenheim de Bilbao?",
        2, 5,
        [("A", "Zaha Hadid", False), ("B", "Norman Foster", False), ("C", "Frank Gehry", True), ("D", "Renzo Piano", False)],
    ),
    (
        "¿Quién compuso 'El lago de los cisnes'?",
        2, 5,
        [("A", "Prokofiev", False), ("B", "Stravinsky", False), ("C", "Tchaikovsky", True), ("D", "Rachmaninov", False)],
    ),
    (
        "¿Qué escritor creó al detective Sherlock Holmes?",
        2, 5,
        [("A", "Agatha Christie", False), ("B", "Edgar Allan Poe", False), ("C", "Arthur Conan Doyle", True), ("D", "Raymond Chandler", False)],
    ),
    (
        "¿Quién pintó 'La última cena'?",
        2, 5,
        [("A", "Rafael", False), ("B", "Miguel Ángel", False), ("C", "Botticelli", False), ("D", "Leonardo da Vinci", True)],
    ),
    (
        "¿Cuántos movimientos tiene una sinfonía clásica?",
        2, 5,
        [("A", "2", False), ("B", "3", False), ("C", "4", True), ("D", "5", False)],
    ),
    (
        "¿Qué es el barroco?",
        2, 5,
        [("A", "Movimiento artístico del siglo XX", False), ("B", "Estilo artístico ornamentado del siglo XVII", True), ("C", "Arte minimalista contemporáneo", False), ("D", "Movimiento prerrafaelita", False)],
    ),

    # =====================================================================
    # MEDIO — Economía (cat 6) — +16
    # =====================================================================
    (
        "¿Qué es la inflación?",
        2, 6,
        [("A", "Reducción generalizada de precios", False), ("B", "Aumento generalizado y sostenido de precios", True), ("C", "Crecimiento del PIB", False), ("D", "Reducción del desempleo", False)],
    ),
    (
        "¿Qué significan las siglas PIB?",
        2, 6,
        [("A", "Plan de Inversión Bancario", False), ("B", "Producto Interno Bruto", True), ("C", "Presupuesto Institucional Base", False), ("D", "Plan de Incentivos Bancarios", False)],
    ),
    (
        "¿Qué es una acción bursátil?",
        2, 6,
        [("A", "Préstamo bancario", False), ("B", "Impuesto sobre ganancias", False), ("C", "Participación en el capital de una empresa", True), ("D", "Bono del gobierno", False)],
    ),
    (
        "¿Qué es la deflación?",
        2, 6,
        [("A", "Aumento de precios", False), ("B", "Caída generalizada de precios", True), ("C", "Aumento del desempleo", False), ("D", "Crisis bancaria", False)],
    ),
    (
        "¿Qué es una hipoteca?",
        2, 6,
        [("A", "Seguro de vida", False), ("B", "Tipo de impuesto", False), ("C", "Préstamo garantizado con un inmueble", True), ("D", "Inversión en bolsa", False)],
    ),
    (
        "¿Cuál es la función principal de un banco central?",
        2, 6,
        [("A", "Prestar dinero a particulares", False), ("B", "Regular la política monetaria del país", True), ("C", "Vender acciones en bolsa", False), ("D", "Cobrar impuestos", False)],
    ),
    (
        "¿Qué es la balanza comercial?",
        2, 6,
        [("A", "Deuda pública total", False), ("B", "Diferencia entre exportaciones e importaciones", True), ("C", "Reservas de oro del país", False), ("D", "Tipo de cambio oficial", False)],
    ),
    (
        "¿Cuál es la moneda de Japón?",
        2, 6,
        [("A", "Won", False), ("B", "Yuan", False), ("C", "Yen", True), ("D", "Ringgit", False)],
    ),
    (
        "¿Qué es el salario mínimo?",
        2, 6,
        [("A", "Sueldo máximo de directivos", False), ("B", "Remuneración mínima legal que debe recibir un trabajador", True), ("C", "Pensión de jubilación", False), ("D", "Bono anual obligatorio", False)],
    ),
    (
        "¿Qué es una recesión económica?",
        2, 6,
        [("A", "Crecimiento sostenido del PIB", False), ("B", "Caída del PIB durante dos trimestres consecutivos", True), ("C", "Periodo de alta inflación", False), ("D", "Aumento del desempleo sin caída del PIB", False)],
    ),
    (
        "¿Qué organismo regula el comercio mundial?",
        2, 6,
        [("A", "ONU", False), ("B", "FMI", False), ("C", "Banco Mundial", False), ("D", "OMC", True)],
    ),
    (
        "¿Qué es el tipo de interés?",
        2, 6,
        [("A", "Ganancia de exportaciones", False), ("B", "Precio del dinero prestado", True), ("C", "Tasa de crecimiento del PIB", False), ("D", "Porcentaje de inflación anual", False)],
    ),
    (
        "¿Cuál es la moneda del Reino Unido?",
        2, 6,
        [("A", "Euro", False), ("B", "Dólar", False), ("C", "Franco", False), ("D", "Libra esterlina", True)],
    ),
    (
        "¿Qué es la deuda pública?",
        2, 6,
        [("A", "Deudas de empresas privadas", False), ("B", "Total de lo que debe el gobierno a sus acreedores", True), ("C", "Deuda de las familias", False), ("D", "Préstamos bancarios a empresas", False)],
    ),
    (
        "¿Qué estudia la microeconomía?",
        2, 6,
        [("A", "Solo economías pequeñas", False), ("B", "El comportamiento de consumidores y empresas individuales", True), ("C", "Economía de países en desarrollo", False), ("D", "Política de bancos centrales", False)],
    ),
    (
        "¿Qué es el comercio exterior?",
        2, 6,
        [("A", "Comercio entre ciudades", False), ("B", "Intercambio de bienes y servicios entre países", True), ("C", "Venta en mercados locales", False), ("D", "Comercio electrónico", False)],
    ),

    # =====================================================================
    # DIFÍCIL — Ciencias (cat 1) — +12
    # =====================================================================
    (
        "¿Cuál es la ecuación de la energía cinética?",
        3, 1,
        [("A", "E = mc²", False), ("B", "Ec = ½mv²", True), ("C", "F = ma", False), ("D", "E = hf", False)],
    ),
    (
        "¿Qué describe la entropía en termodinámica?",
        3, 1,
        [("A", "Energía cinética de las moléculas", False), ("B", "Presión de un gas ideal", False), ("C", "Medida del desorden o aleatoriedad de un sistema", True), ("D", "Temperatura absoluta del sistema", False)],
    ),
    (
        "¿Qué establece el principio de incertidumbre de Heisenberg?",
        3, 1,
        [("A", "La energía se conserva siempre", False), ("B", "No se pueden conocer simultáneamente posición y cantidad de movimiento con precisión arbitraria", True), ("C", "El universo se expande aceleradamente", False), ("D", "La luz viaja a velocidad constante en el vacío", False)],
    ),
    (
        "¿Cuál es el número de Avogadro?",
        3, 1,
        [("A", "3.14 × 10²³", False), ("B", "6.022 × 10²³", True), ("C", "9.109 × 10²³", False), ("D", "1.602 × 10²³", False)],
    ),
    (
        "¿Qué es la fusión nuclear?",
        3, 1,
        [("A", "División de núcleos pesados en fragmentos más ligeros", False), ("B", "Unión de núcleos ligeros liberando grandes cantidades de energía", True), ("C", "Reacción química exotérmica", False), ("D", "Desintegración radiactiva espontánea", False)],
    ),
    (
        "¿Qué es la materia oscura?",
        3, 1,
        [("A", "Materia en estado sólido muy denso", False), ("B", "Agujeros negros supermasivos", False), ("C", "Materia que no emite luz pero ejerce atracción gravitacional", True), ("D", "Gas interestelar frío", False)],
    ),
    (
        "¿Qué establece la ley de Ohm?",
        3, 1,
        [("A", "F = ma", False), ("B", "E = mc²", False), ("C", "V = I·R", True), ("D", "P = mv", False)],
    ),
    (
        "¿Qué es un quasar?",
        3, 1,
        [("A", "Tipo de estrella de neutrones fría", False), ("B", "Núcleo galáctico activo extremadamente luminoso", True), ("C", "Agujero negro estelar", False), ("D", "Nube de gas y polvo interestelar", False)],
    ),
    (
        "¿Cuál es la diferencia principal entre fisión y fusión nuclear?",
        3, 1,
        [("A", "La fisión usa hidrógeno; la fusión usa uranio", False), ("B", "La fisión divide núcleos pesados; la fusión une núcleos ligeros", True), ("C", "La fisión no produce energía", False), ("D", "No hay diferencia energética entre ambas", False)],
    ),
    (
        "¿Qué es el efecto fotoeléctrico?",
        3, 1,
        [("A", "Refracción de la luz al pasar por el agua", False), ("B", "Emisión de electrones por un metal al recibir radiación electromagnética", True), ("C", "Absorción de calor por metales", False), ("D", "Polarización de la luz solar", False)],
    ),
    (
        "¿Qué es la teoría de la relatividad especial de Einstein?",
        3, 1,
        [("A", "Teoría que unifica mecánica cuántica y gravedad", False), ("B", "Teoría que establece que el tiempo y el espacio son relativos al movimiento del observador", True), ("C", "Teoría de la evolución de las especies", False), ("D", "Principio de conservación de la energía mecánica", False)],
    ),
    (
        "¿Qué es la radiación de fondo de microondas cósmicas?",
        3, 1,
        [("A", "Radiación emitida continuamente por el Sol", False), ("B", "Energía residual del Big Bang que llena el universo", True), ("C", "Radiación producida por agujeros negros", False), ("D", "Emisión electromagnética de galaxias activas", False)],
    ),

    # =====================================================================
    # DIFÍCIL — Historia (cat 2) — +21
    # =====================================================================
    (
        "¿En qué año ocurrió la Revolución Rusa bolchevique?",
        3, 2,
        [("A", "1905", False), ("B", "1914", False), ("C", "1917", True), ("D", "1921", False)],
    ),
    (
        "¿Quién fue Otto von Bismarck?",
        3, 2,
        [("A", "Kaiser de Alemania", False), ("B", "Canciller prusiano que unificó Alemania", True), ("C", "General de la Primera Guerra Mundial", False), ("D", "Filósofo alemán del idealismo", False)],
    ),
    (
        "¿Qué estableció el Tratado de Versalles de 1919?",
        3, 2,
        [("A", "Alianza militar entre Francia y Rusia", False), ("B", "Fin de la Primera Guerra Mundial con fuertes sanciones a Alemania", True), ("C", "Tratado comercial entre potencias europeas", False), ("D", "Paz entre Estados Unidos y Japón", False)],
    ),
    (
        "¿En qué año fue asesinado Abraham Lincoln?",
        3, 2,
        [("A", "1861", False), ("B", "1863", False), ("C", "1865", True), ("D", "1869", False)],
    ),
    (
        "¿Quién fue Gengis Kan?",
        3, 2,
        [("A", "Emperador de la dinastía Han", False), ("B", "Fundador y líder del Imperio Mongol", True), ("C", "Sultán del Imperio Otomano", False), ("D", "Faraón del Imperio Nuevo egipcio", False)],
    ),
    (
        "¿En qué año cayó el Imperio Azteca ante los conquistadores españoles?",
        3, 2,
        [("A", "1492", False), ("B", "1510", False), ("C", "1521", True), ("D", "1533", False)],
    ),
    (
        "¿Qué fue el apartheid en Sudáfrica?",
        3, 2,
        [("A", "Sistema económico de planificación central", False), ("B", "Régimen institucional de segregación racial", True), ("C", "Partido político de liberación nacional", False), ("D", "Movimiento independentista regional", False)],
    ),
    (
        "¿En qué año fue asesinado Julio César?",
        3, 2,
        [("A", "63 a.C.", False), ("B", "50 a.C.", False), ("C", "44 a.C.", True), ("D", "27 a.C.", False)],
    ),
    (
        "¿En qué año se firmó la Magna Carta?",
        3, 2,
        [("A", "1066", False), ("B", "1215", True), ("C", "1348", False), ("D", "1453", False)],
    ),
    (
        "¿Qué promovió la Ilustración del siglo XVIII?",
        3, 2,
        [("A", "El poder absoluto de los monarcas", False), ("B", "La fe religiosa como fuente de conocimiento", False), ("C", "La razón, la ciencia y los derechos individuales", True), ("D", "El retorno a las tradiciones medievales", False)],
    ),
    (
        "¿Qué fue la batalla de Waterloo (1815)?",
        3, 2,
        [("A", "Primera batalla de la Primera Guerra Mundial", False), ("B", "Derrota definitiva de Napoleón ante las potencias europeas", True), ("C", "Batalla decisiva de la Guerra Civil española", False), ("D", "Última batalla de la Segunda Guerra Mundial", False)],
    ),
    (
        "¿Quién fue Simón Bolívar?",
        3, 2,
        [("A", "Libertador de América Central exclusivamente", False), ("B", "Héroe de la independencia de varios países sudamericanos", True), ("C", "Primer presidente de Argentina", False), ("D", "General de la independencia de México", False)],
    ),
    (
        "¿Qué fue la Guerra de los Treinta Años (1618-1648)?",
        3, 2,
        [("A", "Conflicto colonial en América", False), ("B", "Serie de guerras religiosas y políticas en Europa Central", True), ("C", "Guerra entre España y el Imperio Otomano", False), ("D", "Conflicto entre China y Japón por el Pacífico", False)],
    ),
    (
        "¿Qué fue el Holocausto durante la Segunda Guerra Mundial?",
        3, 2,
        [("A", "Campaña de bombardeos sobre ciudades europeas", False), ("B", "Genocidio sistemático de judíos y otras minorías por el régimen nazi", True), ("C", "Destrucción de ciudades japonesas por bombas atómicas", False), ("D", "Hambruna provocada por el bloqueo naval aliado", False)],
    ),
    (
        "¿Quién fue Cleopatra?",
        3, 2,
        [("A", "Emperatriz del Imperio Romano", False), ("B", "Última soberana del Antiguo Egipto", True), ("C", "Reina de la Grecia clásica", False), ("D", "Gobernante de Cartago", False)],
    ),
    (
        "¿Qué fue la Inquisición española?",
        3, 2,
        [("A", "Organización de comercio colonial", False), ("B", "Tribunal eclesiástico que perseguía la herejía y la disidencia religiosa", True), ("C", "Corte de justicia civil española", False), ("D", "Partido político de la Reconquista", False)],
    ),
    (
        "¿En qué año se unificó Alemania como Estado nación bajo Bismarck?",
        3, 2,
        [("A", "1848", False), ("B", "1866", False), ("C", "1871", True), ("D", "1918", False)],
    ),
    (
        "¿Qué fue la Reconquista en la Península Ibérica?",
        3, 2,
        [("A", "Conquista española de América", False), ("B", "Proceso de recuperación de territorios peninsulares bajo dominio musulmán", True), ("C", "Revolución contra la monarquía española", False), ("D", "Guerra entre España y Francia por los Pirineos", False)],
    ),
    (
        "¿Quién fue Alejandro Magno?",
        3, 2,
        [("A", "Primer rey de la República Romana", False), ("B", "Rey macedonio que conquistó un vasto imperio hasta la India", True), ("C", "Faraón del Imperio Medio egipcio", False), ("D", "Comandante del ejército persa aqueménida", False)],
    ),
    (
        "¿En qué año se fundó la OTAN?",
        3, 2,
        [("A", "1945", False), ("B", "1947", False), ("C", "1949", True), ("D", "1955", False)],
    ),
    (
        "¿Qué fue la Revolución Cultural china (1966-1976)?",
        3, 2,
        [("A", "Proceso de industrialización acelerada", False), ("B", "Campaña de Mao Zedong que perseguía la élite intelectual y promovía la ortodoxia comunista", True), ("C", "Reforma económica hacia el capitalismo de Estado", False), ("D", "Guerra sino-soviética por el control de Mongolia", False)],
    ),

    # =====================================================================
    # DIFÍCIL — Geografía (cat 3) — +21
    # =====================================================================
    (
        "¿Cuál es la profundidad máxima aproximada de la Fosa de las Marianas?",
        3, 3,
        [("A", "~6.000 m", False), ("B", "~8.000 m", False), ("C", "~11.000 m", True), ("D", "~14.000 m", False)],
    ),
    (
        "¿En qué país se encuentra el monte Kilimanjaro?",
        3, 3,
        [("A", "Kenia", False), ("B", "Etiopía", False), ("C", "Tanzania", True), ("D", "Mozambique", False)],
    ),
    (
        "¿Cuál es el mar más salado del mundo?",
        3, 3,
        [("A", "Mar Rojo", False), ("B", "Mar Mediterráneo", False), ("C", "Mar Muerto", True), ("D", "Mar Caspio", False)],
    ),
    (
        "¿Cuál es la capital de Canadá?",
        3, 3,
        [("A", "Toronto", False), ("B", "Montreal", False), ("C", "Vancouver", False), ("D", "Ottawa", True)],
    ),
    (
        "¿Qué río atraviesa la ciudad de Londres?",
        3, 3,
        [("A", "Sena", False), ("B", "Rin", False), ("C", "Támesis", True), ("D", "Danubio", False)],
    ),
    (
        "¿Cuántos países forman actualmente la Unión Europea?",
        3, 3,
        [("A", "25", False), ("B", "27", True), ("C", "30", False), ("D", "33", False)],
    ),
    (
        "¿En qué país está el río Ganges?",
        3, 3,
        [("A", "China", False), ("B", "Bangladés", False), ("C", "Pakistán", False), ("D", "India", True)],
    ),
    (
        "¿Cuál es la capital de Turquía?",
        3, 3,
        [("A", "Estambul", False), ("B", "Ankara", True), ("C", "Esmirna", False), ("D", "Bursa", False)],
    ),
    (
        "¿Qué fue la Pangea?",
        3, 3,
        [("A", "Antiguo mar que cubría toda la Tierra", False), ("B", "Supercontinente único que existió hace ~300 millones de años", True), ("C", "Planeta similar a la Tierra", False), ("D", "Capa de hielo que cubrió el hemisferio norte", False)],
    ),
    (
        "¿Cuál es el desierto más frío del mundo?",
        3, 3,
        [("A", "Gobi", False), ("B", "Atacama", False), ("C", "Antártida", True), ("D", "Gran Desierto de Arena", False)],
    ),
    (
        "¿Qué país posee la mayor extensión de selva amazónica?",
        3, 3,
        [("A", "Colombia", False), ("B", "Perú", False), ("C", "Venezuela", False), ("D", "Brasil", True)],
    ),
    (
        "¿Por cuántos husos horarios se extiende Rusia?",
        3, 3,
        [("A", "7", False), ("B", "9", False), ("C", "11", True), ("D", "13", False)],
    ),
    (
        "¿Qué es el estrecho de Bering?",
        3, 3,
        [("A", "Paso que une el Atlántico con el Pacífico", False), ("B", "Paso marítimo que separa Rusia de Alaska", True), ("C", "Canal que une el Mediterráneo con el Mar Rojo", False), ("D", "Estrecho entre la India y Sri Lanka", False)],
    ),
    (
        "¿Cuál es la isla más grande del mundo?",
        3, 3,
        [("A", "Borneo", False), ("B", "Madagascar", False), ("C", "Groenlandia", True), ("D", "Nueva Guinea", False)],
    ),
    (
        "¿Qué es el trópico de Capricornio?",
        3, 3,
        [("A", "Línea imaginaria a 23,5° latitud norte", False), ("B", "Línea imaginaria a 23,5° latitud sur", True), ("C", "El ecuador geográfico", False), ("D", "El círculo polar antártico", False)],
    ),
    (
        "¿Cuál es el lago navegable más alto del mundo?",
        3, 3,
        [("A", "Lago Titicaca", True), ("B", "Lago Victoria", False), ("C", "Mar Caspio", False), ("D", "Lago Superior", False)],
    ),
    (
        "¿Cuál es la capital administrativa de Sudáfrica?",
        3, 3,
        [("A", "Ciudad del Cabo", False), ("B", "Johannesburgo", False), ("C", "Pretoria", True), ("D", "Durban", False)],
    ),
    (
        "¿Cuál es la montaña más alta de Europa (incluyendo el Cáucaso)?",
        3, 3,
        [("A", "Mont Blanc", False), ("B", "Matterhorn", False), ("C", "Monte Rosa", False), ("D", "Elbrus", True)],
    ),
    (
        "¿Qué separa el continente americano de Asia en el norte?",
        3, 3,
        [("A", "El océano Atlántico", False), ("B", "El estrecho de Bering", True), ("C", "El canal de Panamá", False), ("D", "El mar de Bering completo", False)],
    ),
    (
        "¿Cuál es el país con la línea costera más larga del mundo?",
        3, 3,
        [("A", "Rusia", False), ("B", "Australia", False), ("C", "Canadá", True), ("D", "Noruega", False)],
    ),
    (
        "¿En qué continente se encuentran más países sin salida al mar?",
        3, 3,
        [("A", "Asia", False), ("B", "Europa", False), ("C", "África", True), ("D", "América del Sur", False)],
    ),

    # =====================================================================
    # DIFÍCIL — Tecnología (cat 4) — +21
    # =====================================================================
    (
        "¿Qué describe la complejidad O(n log n) en algoritmos?",
        3, 4,
        [("A", "Algoritmo de tiempo constante", False), ("B", "Complejidad típica de algoritmos de ordenamiento eficientes", True), ("C", "Algoritmo cuadrático", False), ("D", "Algoritmo exponencial", False)],
    ),
    (
        "¿Qué es el protocolo TCP/IP?",
        3, 4,
        [("A", "Lenguaje de programación para redes", False), ("B", "Conjunto de protocolos que sustenta la comunicación en internet", True), ("C", "Sistema operativo para servidores", False), ("D", "Tipo de cifrado de clave pública", False)],
    ),
    (
        "¿Qué es el machine learning?",
        3, 4,
        [("A", "Aprendizaje de idiomas asistido por computadora", False), ("B", "Subcampo de la IA en el que los modelos aprenden patrones a partir de datos", True), ("C", "Programación de brazos robóticos", False), ("D", "Diseño automatizado de interfaces gráficas", False)],
    ),
    (
        "¿Qué es una API?",
        3, 4,
        [("A", "Tipo de base de datos no relacional", False), ("B", "Interfaz que permite la comunicación entre diferentes aplicaciones", True), ("C", "Sistema de detección de intrusiones", False), ("D", "Lenguaje de marcado para APIs web", False)],
    ),
    (
        "¿Qué es Docker?",
        3, 4,
        [("A", "Lenguaje de programación orientado a objetos", False), ("B", "Sistema operativo basado en Linux", False), ("C", "Plataforma de contenedores para empaquetar y desplegar aplicaciones", True), ("D", "Framework de JavaScript para frontends", False)],
    ),
    (
        "¿Qué es blockchain?",
        3, 4,
        [("A", "Tipo de virus de red", False), ("B", "Cadena de bloques descentralizada e inmutable para registrar datos", True), ("C", "Red social descentralizada", False), ("D", "Sistema de cifrado simétrico", False)],
    ),
    (
        "¿En qué año fue creado el lenguaje de programación C?",
        3, 4,
        [("A", "1965", False), ("B", "1969", False), ("C", "1972", True), ("D", "1980", False)],
    ),
    (
        "¿Qué es SQL?",
        3, 4,
        [("A", "Lenguaje de programación orientado a objetos", False), ("B", "Sistema operativo para bases de datos", False), ("C", "Lenguaje estándar para consultar y gestionar bases de datos relacionales", True), ("D", "Protocolo de transferencia de datos en red", False)],
    ),
    (
        "¿Quién creó el sistema operativo Linux?",
        3, 4,
        [("A", "Bill Gates", False), ("B", "Steve Jobs", False), ("C", "Dennis Ritchie", False), ("D", "Linus Torvalds", True)],
    ),
    (
        "¿Qué es Git?",
        3, 4,
        [("A", "Lenguaje de programación funcional", False), ("B", "Sistema de control de versiones distribuido", True), ("C", "Base de datos distribuida", False), ("D", "Framework de desarrollo web", False)],
    ),
    (
        "¿Qué es un ataque DDoS?",
        3, 4,
        [("A", "Virus que cifra archivos y pide rescate", False), ("B", "Intrusión silenciosa en sistemas bancarios", False), ("C", "Ataque de denegación de servicio distribuido que satura un servidor", True), ("D", "Robo de contraseñas mediante phishing", False)],
    ),
    (
        "¿Qué es la computación cuántica?",
        3, 4,
        [("A", "Computación de alta velocidad con procesadores convencionales", False), ("B", "Paradigma de computación basado en qubits y principios de mecánica cuántica", True), ("C", "Sistema para procesar grandes volúmenes de datos en paralelo", False), ("D", "Rama de la IA que simula el razonamiento humano", False)],
    ),
    (
        "¿Qué mejora introduce IPv6 respecto a IPv4?",
        3, 4,
        [("A", "Mayor velocidad de transmisión", False), ("B", "Espacio de direcciones IP mucho mayor (128 bits vs 32 bits)", True), ("C", "Cifrado obligatorio de todo el tráfico", False), ("D", "Compatibilidad con redes inalámbricas", False)],
    ),
    (
        "¿En qué año fue fundada Microsoft?",
        3, 4,
        [("A", "1970", False), ("B", "1973", False), ("C", "1975", True), ("D", "1980", False)],
    ),
    (
        "¿Qué hace un compilador?",
        3, 4,
        [("A", "Ejecuta código interpretado línea a línea", False), ("B", "Traduce código fuente a código máquina", True), ("C", "Gestiona la memoria del sistema operativo", False), ("D", "Comprime archivos ejecutables", False)],
    ),
    (
        "¿Qué es el cifrado AES?",
        3, 4,
        [("A", "Protocolo de autenticación en dos pasos", False), ("B", "Estándar de cifrado simétrico avanzado", True), ("C", "Sistema de firma digital asimétrica", False), ("D", "Protocolo de intercambio de claves públicas", False)],
    ),
    (
        "¿Qué es MapReduce?",
        3, 4,
        [("A", "Framework de JavaScript para frontends", False), ("B", "Función de agregación en bases de datos SQL", False), ("C", "Modelo de programación para procesamiento distribuido de grandes volúmenes de datos", True), ("D", "Protocolo de enrutamiento de redes", False)],
    ),
    (
        "¿Qué es la virtualización en computación?",
        3, 4,
        [("A", "Crear gráficos 3D fotorrealistas", False), ("B", "Simular hardware o entornos de software de forma lógica", True), ("C", "Comprimir archivos del sistema operativo", False), ("D", "Hacer copias de seguridad en la nube", False)],
    ),
    (
        "¿Qué es el protocolo HTTPS?",
        3, 4,
        [("A", "Versión más rápida de HTTP", False), ("B", "HTTP con capa de seguridad TLS/SSL", True), ("C", "Protocolo para transferencia de archivos FTP seguro", False), ("D", "Sistema de correo electrónico cifrado", False)],
    ),
    (
        "¿Qué es una red neuronal artificial?",
        3, 4,
        [("A", "Red de computadoras físicamente conectadas", False), ("B", "Sistema computacional inspirado en el funcionamiento del cerebro biológico", True), ("C", "Tipo de base de datos no estructurada", False), ("D", "Algoritmo de búsqueda en grafos", False)],
    ),
    (
        "¿Qué establece el principio de menor privilegio en ciberseguridad?",
        3, 4,
        [("A", "Dar todos los permisos a todos los usuarios", False), ("B", "Otorgar solo los permisos mínimos necesarios para realizar una tarea", True), ("C", "No usar contraseñas en sistemas internos", False), ("D", "Compartir accesos entre usuarios del mismo equipo", False)],
    ),

    # =====================================================================
    # DIFÍCIL — Arte (cat 5) — +14
    # =====================================================================
    (
        "¿Quién pintó 'La persistencia de la memoria'?",
        3, 5,
        [("A", "Picasso", False), ("B", "Miró", False), ("C", "Salvador Dalí", True), ("D", "Magritte", False)],
    ),
    (
        "¿Qué es el contrapunto en música?",
        3, 5,
        [("A", "Ritmo acelerado de una pieza musical", False), ("B", "Técnica de combinar dos o más melodías independientes simultáneamente", True), ("C", "Tipo de escala modal", False), ("D", "Instrumento de percusión barroco", False)],
    ),
    (
        "¿Quién escribió 'Ulises' (1922)?",
        3, 5,
        [("A", "Franz Kafka", False), ("B", "Marcel Proust", False), ("C", "James Joyce", True), ("D", "Virginia Woolf", False)],
    ),
    (
        "¿Qué es el dodecafonismo?",
        3, 5,
        [("A", "Música compuesta para 12 instrumentos", False), ("B", "Técnica de composición que utiliza las 12 notas de la escala cromática de forma serial", True), ("C", "Tipo de danza folclórica europea", False), ("D", "Movimiento pictórico del siglo XIX", False)],
    ),
    (
        "¿Por qué es conocida Frida Kahlo?",
        3, 5,
        [("A", "Escultora italiana del Renacimiento", False), ("B", "Pintora mexicana conocida por sus autorretratos y arte simbólico", True), ("C", "Fotógrafa francesa del movimiento surrealista", False), ("D", "Bailarina española del siglo XX", False)],
    ),
    (
        "¿Quién compuso 'El Mesías'?",
        3, 5,
        [("A", "Johann Sebastian Bach", False), ("B", "Georg Friedrich Händel", True), ("C", "Joseph Haydn", False), ("D", "Antonio Vivaldi", False)],
    ),
    (
        "¿Qué es el neoclasicismo?",
        3, 5,
        [("A", "Movimiento artístico del siglo XX que reinterpreta el arte moderno", False), ("B", "Corriente artística inspirada en los ideales del arte clásico griego y romano", True), ("C", "Arte abstracto y minimalista contemporáneo", False), ("D", "Movimiento dadaísta de los años 1910", False)],
    ),
    (
        "¿Quién esculpió 'El pensador'?",
        3, 5,
        [("A", "Gian Lorenzo Bernini", False), ("B", "Donatello", False), ("C", "Auguste Rodin", True), ("D", "Constantin Brâncuși", False)],
    ),
    (
        "¿Qué es el dadaísmo?",
        3, 5,
        [("A", "Corriente del realismo fotográfico", False), ("B", "Movimiento artístico de vanguardia que rechazaba la lógica y el racionalismo", True), ("C", "Escuela de arquitectura funcionalista", False), ("D", "Técnica escultórica minimalista", False)],
    ),
    (
        "¿Quién escribió 'En busca del tiempo perdido'?",
        3, 5,
        [("A", "Émile Zola", False), ("B", "Gustave Flaubert", False), ("C", "Honoré de Balzac", False), ("D", "Marcel Proust", True)],
    ),
    (
        "¿Qué arquitecto diseñó el museo Guggenheim de Nueva York?",
        3, 5,
        [("A", "Ludwig Mies van der Rohe", False), ("B", "Le Corbusier", False), ("C", "Frank Lloyd Wright", True), ("D", "Philip Johnson", False)],
    ),
    (
        "¿Qué es la perspectiva lineal en pintura?",
        3, 5,
        [("A", "Técnica de pintar únicamente con líneas rectas", False), ("B", "Método para representar profundidad con líneas que convergen en un punto de fuga", True), ("C", "Estilo de dibujo sin uso de color", False), ("D", "Movimiento artístico del siglo XX", False)],
    ),
    (
        "¿Quién compuso 'La Consagración de la Primavera'?",
        3, 5,
        [("A", "Claude Debussy", False), ("B", "Maurice Ravel", False), ("C", "Igor Stravinsky", True), ("D", "Béla Bartók", False)],
    ),
    (
        "¿Qué es el expresionismo abstracto?",
        3, 5,
        [("A", "Pintura realista que expresa emociones cotidianas", False), ("B", "Movimiento pictórico estadounidense de posguerra con énfasis en la expresión espontánea y el gesto", True), ("C", "Arte conceptual minimalista de los años 60", False), ("D", "Corriente del arte pop norteamericano", False)],
    ),

    # =====================================================================
    # DIFÍCIL — Economía (cat 6) — +13
    # =====================================================================
    (
        "¿Qué describe la curva de Phillips?",
        3, 6,
        [("A", "Relación directa entre deuda pública e inflación", False), ("B", "Relación inversa entre inflación y desempleo", True), ("C", "Curva de oferta del mercado laboral", False), ("D", "Relación entre PIB y tipo de cambio", False)],
    ),
    (
        "¿Qué es el riesgo moral (moral hazard)?",
        3, 6,
        [("A", "Riesgo de pérdida en inversiones bursátiles", False), ("B", "Tendencia a asumir más riesgo cuando las consecuencias las soporta otro", True), ("C", "Fraude en estados financieros", False), ("D", "Quiebra bancaria sistémica", False)],
    ),
    (
        "¿Qué es la trampa de liquidez?",
        3, 6,
        [("A", "Fraude en el sistema bancario internacional", False), ("B", "Situación donde la política monetaria pierde eficacia porque los tipos de interés ya son cero", True), ("C", "Exceso de reservas en los bancos comerciales", False), ("D", "Sistema de tipo de cambio fijo", False)],
    ),
    (
        "¿Qué estudia la teoría de juegos?",
        3, 6,
        [("A", "La racionalidad del consumidor en mercados perfectos", False), ("B", "Las decisiones estratégicas entre agentes interdependientes", True), ("C", "Los modelos de crecimiento económico a largo plazo", False), ("D", "El análisis de mercados de activos financieros", False)],
    ),
    (
        "¿Qué es el déficit fiscal?",
        3, 6,
        [("A", "Superávit presupuestario del sector público", False), ("B", "Exceso de exportaciones sobre importaciones", False), ("C", "Situación en que el gasto público supera los ingresos del gobierno", True), ("D", "Caída de la recaudación tributaria en términos reales", False)],
    ),
    (
        "¿Qué es la paridad del poder adquisitivo (PPA)?",
        3, 6,
        [("A", "Tipo de cambio fijado por el banco central", False), ("B", "Método para comparar el poder de compra entre países ajustando por niveles de precios", True), ("C", "Política de control de precios de bienes esenciales", False), ("D", "Sistema de tipo de cambio flotante administrado", False)],
    ),
    (
        "¿A quién se atribuye el desarrollo de la teoría del capital humano?",
        3, 6,
        [("A", "John Maynard Keynes", False), ("B", "Milton Friedman", False), ("C", "Gary Becker", True), ("D", "Paul Samuelson", False)],
    ),
    (
        "¿Qué es el mercado de futuros?",
        3, 6,
        [("A", "Mercado de acciones de empresas tecnológicas", False), ("B", "Mercado donde se negocian contratos de compraventa a un precio y fecha futura acordados", True), ("C", "Bolsa de materias primas al contado", False), ("D", "Mercado interbancario de divisas al contado", False)],
    ),
    (
        "¿Qué ilustra la curva de Laffer?",
        3, 6,
        [("A", "La relación entre oferta laboral y salario", False), ("B", "La relación entre la tasa impositiva y los ingresos fiscales totales", True), ("C", "El modelo IS-LM de equilibrio macroeconómico", False), ("D", "La curva de Phillips ampliada con expectativas", False)],
    ),
    (
        "¿Qué es el equilibrio de Nash?",
        3, 6,
        [("A", "Punto de máxima ganancia de un monopolio", False), ("B", "Estado en el que ningún jugador puede mejorar su resultado cambiando su estrategia unilateralmente", True), ("C", "Tipo de equilibrio en mercados de competencia perfecta", False), ("D", "Óptimo social de Pareto", False)],
    ),
    (
        "¿Qué relaciona la teoría cuantitativa del dinero?",
        3, 6,
        [("A", "La inflación con la tasa de desempleo", False), ("B", "La masa monetaria con el nivel general de precios (MV = PQ)", True), ("C", "Los modelos de préstamos bancarios con la demanda agregada", False), ("D", "La propensión marginal al consumo con el multiplicador keynesiano", False)],
    ),
    (
        "¿Qué es el efecto de expulsión (crowding out)?",
        3, 6,
        [("A", "Aumento del consumo privado inducido por el gasto público", False), ("B", "Reducción de la inversión privada causada por el aumento del gasto público", True), ("C", "Efecto multiplicador del presupuesto en el PIB", False), ("D", "Quiebra empresarial generada por alta presión fiscal", False)],
    ),
    (
        "¿Qué es la estagflación?",
        3, 6,
        [("A", "Alta inflación combinada con fuerte crecimiento económico", False), ("B", "Caída del PIB con deflación simultánea", False), ("C", "Inflación elevada combinada con estancamiento económico y desempleo alto", True), ("D", "Deflación con crecimiento moderado del PIB", False)],
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
        todas = PREGUNTAS + PREGUNTAS_ADICIONALES
        for enunciado, nivel_id, cat_id, opciones in todas:
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

        facil   = sum(1 for _, n, *_ in todas if n == 1)
        medio   = sum(1 for _, n, *_ in todas if n == 2)
        dificil = sum(1 for _, n, *_ in todas if n == 3)

        print("Base de datos inicializada correctamente.")
        print(f"  Categorías: {len(categorias_data)}")
        print(f"  Preguntas:  {len(todas)}  (Fácil: {facil}  Medio: {medio}  Difícil: {dificil})")
        print("  Usuario: admin  |  Contraseña: admin123")


if __name__ == "__main__":
    seed()