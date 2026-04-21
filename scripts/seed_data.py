"""
Ejecutar una sola vez para inicializar la base de datos:
    python scripts/seed_data.py

Crea:
  - El usuario administrador (admin / admin123)
  - Los 3 niveles de dificultad
  - 3 categorías: Ciencias, Tecnología, Geografía
  - Preguntas suficientes para jugar cada categoría en cada dificultad:
      Fácil  ≥10 preguntas por categoría
      Medio  ≥15 preguntas por categoría
      Difícil ≥20 preguntas por categoría
  - Todas las opciones tienen ≤40 caracteres
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
# Categorías: Ciencias=1  Tecnología=2  Geografía=3
# Niveles:    Fácil=1     Medio=2        Difícil=3
# ---------------------------------------------------------------------------

PREGUNTAS = [

    # =========================================================================
    # FÁCIL — CIENCIAS (cat 1) — 12 preguntas
    # =========================================================================
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
        "¿Qué gas abunda más en la atmósfera terrestre?",
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
        "¿Qué instrumento mide la temperatura?",
        1, 1,
        [("A", "Barómetro", False), ("B", "Termómetro", True), ("C", "Higrómetro", False), ("D", "Anemómetro", False)],
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
        "¿Cuántos huesos tiene el cuerpo humano adulto?",
        1, 1,
        [("A", "106", False), ("B", "186", False), ("C", "206", True), ("D", "256", False)],
    ),
    (
        "¿Cuántos segundos tiene un minuto?",
        1, 1,
        [("A", "30", False), ("B", "45", False), ("C", "60", True), ("D", "100", False)],
    ),

    # =========================================================================
    # FÁCIL — TECNOLOGÍA (cat 2) — 12 preguntas
    # =========================================================================
    (
        "¿Qué empresa desarrolló el sistema operativo Windows?",
        1, 2,
        [("A", "Apple", False), ("B", "Google", False), ("C", "Microsoft", True), ("D", "IBM", False)],
    ),
    (
        "¿Qué significa 'USB'?",
        1, 2,
        [("A", "Universal Software Bus", False), ("B", "Unified Serial Board", False), ("C", "Universal Serial Bus", True), ("D", "Unique System Bridge", False)],
    ),
    (
        "¿Qué significa 'PDF'?",
        1, 2,
        [("A", "Personal Data File", False), ("B", "Portable Document Format", True), ("C", "Print Display Format", False), ("D", "Program Data File", False)],
    ),
    (
        "¿Qué significa 'RAM' en informática?",
        1, 2,
        [("A", "Random Access Memory", True), ("B", "Read-only Array Module", False), ("C", "Rapid Application Mode", False), ("D", "Remote Access Management", False)],
    ),
    (
        "¿Qué empresa creó el iPhone?",
        1, 2,
        [("A", "Samsung", False), ("B", "Google", False), ("C", "Apple", True), ("D", "Huawei", False)],
    ),
    (
        "¿Qué significa 'GPS'?",
        1, 2,
        [("A", "General Processing System", False), ("B", "Global Positioning System", True), ("C", "Graphic Processing Software", False), ("D", "Ground Patrol Signal", False)],
    ),
    (
        "¿Para qué sirve un antivirus?",
        1, 2,
        [("A", "Acelerar la computadora", False), ("B", "Editar documentos", False), ("C", "Proteger contra software malicioso", True), ("D", "Mejorar la pantalla", False)],
    ),
    (
        "¿Cuántos colores primarios tiene una pantalla RGB?",
        1, 2,
        [("A", "2", False), ("B", "3", True), ("C", "4", False), ("D", "7", False)],
    ),
    (
        "¿Qué atajo de teclado deshace una acción?",
        1, 2,
        [("A", "Ctrl+Z", True), ("B", "Ctrl+X", False), ("C", "Ctrl+D", False), ("D", "Alt+F4", False)],
    ),
    (
        "¿Qué significa 'Wi-Fi'?",
        1, 2,
        [("A", "Wired Fidelity", False), ("B", "Wide Frequency", False), ("C", "Wireless Fidelity", True), ("D", "Web Interface", False)],
    ),
    (
        "¿Cuál es el sistema operativo de Apple para Mac?",
        1, 2,
        [("A", "Windows", False), ("B", "Linux", False), ("C", "Android", False), ("D", "macOS", True)],
    ),
    (
        "¿Qué dispositivo conecta una red doméstica a internet?",
        1, 2,
        [("A", "Impresora", False), ("B", "Escáner", False), ("C", "Módem", True), ("D", "Monitor", False)],
    ),

    # =========================================================================
    # FÁCIL — GEOGRAFÍA (cat 3) — 12 preguntas
    # =========================================================================
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
        "¿Cuál es la capital de Japón?",
        1, 3,
        [("A", "Osaka", False), ("B", "Seúl", False), ("C", "Pekín", False), ("D", "Tokio", True)],
    ),
    (
        "¿Cuál es el país más grande del mundo por superficie?",
        1, 3,
        [("A", "China", False), ("B", "Canadá", False), ("C", "Estados Unidos", False), ("D", "Rusia", True)],
    ),
    (
        "¿En qué país se encuentra la Torre Eiffel?",
        1, 3,
        [("A", "Italia", False), ("B", "España", False), ("C", "Francia", True), ("D", "Bélgica", False)],
    ),
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

    # =========================================================================
    # MEDIO — CIENCIAS (cat 1) — 16 preguntas
    # =========================================================================
    (
        "¿Cuál es la velocidad de la luz en el vacío?",
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
        "¿Cuál es el punto de ebullición del agua a nivel del mar?",
        2, 1,
        [("A", "80 °C", False), ("B", "90 °C", False), ("C", "100 °C", True), ("D", "120 °C", False)],
    ),
    (
        "¿Qué partícula tiene carga positiva en el núcleo atómico?",
        2, 1,
        [("A", "Electrón", False), ("B", "Neutrón", False), ("C", "Protón", True), ("D", "Fotón", False)],
    ),
    (
        "¿Qué tipo de ondas son la luz visible?",
        2, 1,
        [("A", "Mecánicas", False), ("B", "Sonoras", False), ("C", "Electromagnéticas", True), ("D", "Gravitacionales", False)],
    ),
    (
        "¿Cuál es el número atómico del carbono?",
        2, 1,
        [("A", "4", False), ("B", "6", True), ("C", "8", False), ("D", "12", False)],
    ),
    (
        "¿Qué proceso convierte la glucosa en energía celular?",
        2, 1,
        [("A", "Fotosíntesis", False), ("B", "Fermentación alcohólica", False), ("C", "Respiración celular", True), ("D", "Osmosis", False)],
    ),

    # =========================================================================
    # MEDIO — TECNOLOGÍA (cat 2) — 15 preguntas
    # =========================================================================
    (
        "¿Quién inventó el teléfono?",
        2, 2,
        [("A", "Thomas Edison", False), ("B", "Nikola Tesla", False), ("C", "Alexander Graham Bell", True), ("D", "Guglielmo Marconi", False)],
    ),
    (
        "¿En qué año fue lanzado el primer iPhone?",
        2, 2,
        [("A", "2005", False), ("B", "2006", False), ("C", "2007", True), ("D", "2008", False)],
    ),
    (
        "¿Qué lenguaje de programación creó Guido van Rossum?",
        2, 2,
        [("A", "Java", False), ("B", "Ruby", False), ("C", "Python", True), ("D", "Perl", False)],
    ),
    (
        "¿Cuántos bits tiene un byte?",
        2, 2,
        [("A", "4", False), ("B", "8", True), ("C", "16", False), ("D", "32", False)],
    ),
    (
        "¿Qué significa 'CPU' en informática?",
        2, 2,
        [("A", "Central Processing Unit", True), ("B", "Computer Power Unit", False), ("C", "Central Program Utility", False), ("D", "Core Processing Unit", False)],
    ),
    (
        "¿En qué año se publicó la primera versión de Windows?",
        2, 2,
        [("A", "1981", False), ("B", "1983", False), ("C", "1985", True), ("D", "1990", False)],
    ),
    (
        "¿Cuál es el protocolo base de la World Wide Web?",
        2, 2,
        [("A", "FTP", False), ("B", "SMTP", False), ("C", "HTTP", True), ("D", "SSH", False)],
    ),
    (
        "¿Qué es un algoritmo?",
        2, 2,
        [("A", "Tipo de virus informático", False), ("B", "Lenguaje de programación", False), ("C", "Pasos para resolver un problema", True), ("D", "Sistema operativo", False)],
    ),
    (
        "¿Qué lenguaje estructura páginas web?",
        2, 2,
        [("A", "Python", False), ("B", "Java", False), ("C", "HTML", True), ("D", "SQL", False)],
    ),
    (
        "¿Qué significa 'IP' en redes informáticas?",
        2, 2,
        [("A", "Internal Program", False), ("B", "Internet Protocol", True), ("C", "Input Process", False), ("D", "Integrated Platform", False)],
    ),
    (
        "¿Cuál es la función principal de un sistema operativo?",
        2, 2,
        [("A", "Navegar por internet", False), ("B", "Editar videos", False), ("C", "Gestionar los recursos del hardware", True), ("D", "Proteger contra virus", False)],
    ),
    (
        "¿Qué significa 'URL'?",
        2, 2,
        [("A", "Universal Remote Login", False), ("B", "Uniform Resource Locator", True), ("C", "Unique Reference Link", False), ("D", "User Resource Library", False)],
    ),
    (
        "¿Quién cofundó Apple junto con Steve Jobs?",
        2, 2,
        [("A", "Bill Gates", False), ("B", "Steve Wozniak", True), ("C", "Elon Musk", False), ("D", "Mark Zuckerberg", False)],
    ),
    (
        "¿Qué es el código binario?",
        2, 2,
        [("A", "Sistema numérico en base 10", False), ("B", "Código secreto de cifrado", False), ("C", "Sistema numérico en base 2 (0 y 1)", True), ("D", "Tipo de cifrado asimétrico", False)],
    ),
    (
        "¿Qué empresa desarrolló el sistema operativo Android?",
        2, 2,
        [("A", "Apple", False), ("B", "Microsoft", False), ("C", "Samsung", False), ("D", "Google", True)],
    ),

    # =========================================================================
    # MEDIO — GEOGRAFÍA (cat 3) — 17 preguntas
    # =========================================================================
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
        "¿Cuál estrecho une el Mediterráneo con el Atlántico?",
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
        "¿En qué continente está la mayor parte de la Amazonia?",
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

    # =========================================================================
    # DIFÍCIL — CIENCIAS (cat 1) — 20 preguntas
    # =========================================================================
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
        "¿Cómo se llama el proceso por el que una estrella colapsa en agujero negro?",
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
        "¿Cuál es la distancia media de la Tierra al Sol en UA?",
        3, 1,
        [("A", "0.5 UA", False), ("B", "1 UA", True), ("C", "2 UA", False), ("D", "5 UA", False)],
    ),
    (
        "¿Quién descubrió la penicilina?",
        3, 1,
        [("A", "Louis Pasteur", False), ("B", "Robert Koch", False), ("C", "Joseph Lister", False), ("D", "Alexander Fleming", True)],
    ),
    (
        "¿Cómo se llama el proceso por el que el ADN se convierte en ARN?",
        3, 1,
        [("A", "Traducción", False), ("B", "Replicación", False), ("C", "Transcripción", True), ("D", "Transducción", False)],
    ),
    (
        "¿Cuál es la ecuación de la energía cinética?",
        3, 1,
        [("A", "E = mc²", False), ("B", "Ec = ½mv²", True), ("C", "F = ma", False), ("D", "E = hf", False)],
    ),
    (
        "¿Qué describe la entropía en termodinámica?",
        3, 1,
        [("A", "Energía cinética de las moléculas", False), ("B", "Presión de un gas ideal", False), ("C", "Medida del desorden de un sistema", True), ("D", "Temperatura absoluta del sistema", False)],
    ),
    (
        "¿Qué establece el principio de incertidumbre de Heisenberg?",
        3, 1,
        [("A", "La energía siempre se conserva", False), ("B", "No se conocen posición y momento exactos", True), ("C", "El universo se expande aceleradamente", False), ("D", "La luz viaja a velocidad constante", False)],
    ),
    (
        "¿Cuál es el número de Avogadro?",
        3, 1,
        [("A", "3.14 × 10²³", False), ("B", "6.022 × 10²³", True), ("C", "9.109 × 10²³", False), ("D", "1.602 × 10²³", False)],
    ),
    (
        "¿Qué es la fusión nuclear?",
        3, 1,
        [("A", "Divide núcleos pesados en más ligeros", False), ("B", "Une núcleos ligeros liberando energía", True), ("C", "Reacción química exotérmica", False), ("D", "Desintegración radiactiva espontánea", False)],
    ),
    (
        "¿Qué es la materia oscura?",
        3, 1,
        [("A", "Materia en estado sólido muy denso", False), ("B", "Agujeros negros supermasivos", False), ("C", "No emite luz pero ejerce gravedad", True), ("D", "Gas interestelar frío", False)],
    ),
    (
        "¿Qué establece la ley de Ohm?",
        3, 1,
        [("A", "F = ma", False), ("B", "E = mc²", False), ("C", "V = I·R", True), ("D", "P = mv", False)],
    ),
    (
        "¿Qué es un quasar?",
        3, 1,
        [("A", "Estrella de neutrones fría", False), ("B", "Núcleo galáctico activo muy luminoso", True), ("C", "Agujero negro estelar", False), ("D", "Nube de gas y polvo interestelar", False)],
    ),
    (
        "¿Cuál es la diferencia principal entre fisión y fusión nuclear?",
        3, 1,
        [("A", "Fisión usa hidrógeno; fusión usa uranio", False), ("B", "Fisión parte; fusión une núcleos", True), ("C", "La fisión no produce energía", False), ("D", "No hay diferencia energética entre ambas", False)],
    ),
    (
        "¿Qué es el efecto fotoeléctrico?",
        3, 1,
        [("A", "Refracción de la luz en el agua", False), ("B", "Electrones emitidos por metal irradiado", True), ("C", "Absorción de calor por metales", False), ("D", "Polarización de la luz solar", False)],
    ),
    (
        "¿Qué describe la teoría de la relatividad especial?",
        3, 1,
        [("A", "Unifica mecánica cuántica y gravedad", False), ("B", "El tiempo y espacio son relativos", True), ("C", "Teoría de la evolución de las especies", False), ("D", "Conservación de la energía mecánica", False)],
    ),
    (
        "¿Qué es la radiación de fondo de microondas cósmicas?",
        3, 1,
        [("A", "Radiación emitida por el Sol", False), ("B", "Radiación residual del Big Bang", True), ("C", "Radiación producida por agujeros negros", False), ("D", "Emisión de galaxias activas", False)],
    ),

    # =========================================================================
    # DIFÍCIL — TECNOLOGÍA (cat 2) — 21 preguntas
    # =========================================================================
    (
        "¿Qué describe la complejidad O(n log n) en algoritmos?",
        3, 2,
        [("A", "Algoritmo de tiempo constante", False), ("B", "Típica en algoritmos de ordenamiento", True), ("C", "Algoritmo cuadrático", False), ("D", "Algoritmo exponencial", False)],
    ),
    (
        "¿Qué es el protocolo TCP/IP?",
        3, 2,
        [("A", "Lenguaje de programación para redes", False), ("B", "Protocolos base de internet", True), ("C", "Sistema operativo para servidores", False), ("D", "Tipo de cifrado de clave pública", False)],
    ),
    (
        "¿Qué es el machine learning?",
        3, 2,
        [("A", "Aprendizaje de idiomas con computadora", False), ("B", "IA que aprende patrones desde datos", True), ("C", "Programación de brazos robóticos", False), ("D", "Diseño auto de interfaces gráficas", False)],
    ),
    (
        "¿Qué es una API?",
        3, 2,
        [("A", "Tipo de base de datos no relacional", False), ("B", "Interfaz entre aplicaciones de software", True), ("C", "Sistema de detección de intrusiones", False), ("D", "Lenguaje de marcado para APIs web", False)],
    ),
    (
        "¿Qué es Docker?",
        3, 2,
        [("A", "Lenguaje orientado a objetos", False), ("B", "Sistema operativo basado en Linux", False), ("C", "Plataforma para empaquetar aplicaciones", True), ("D", "Framework de JavaScript para frontends", False)],
    ),
    (
        "¿Qué es blockchain?",
        3, 2,
        [("A", "Tipo de virus de red", False), ("B", "Registro descentralizado e inmutable", True), ("C", "Red social descentralizada", False), ("D", "Sistema de cifrado simétrico", False)],
    ),
    (
        "¿En qué año fue creado el lenguaje de programación C?",
        3, 2,
        [("A", "1965", False), ("B", "1969", False), ("C", "1972", True), ("D", "1980", False)],
    ),
    (
        "¿Qué es SQL?",
        3, 2,
        [("A", "Lenguaje orientado a objetos", False), ("B", "Sistema operativo para BD", False), ("C", "Consultas y gestión de BD relacionales", True), ("D", "Protocolo de transferencia de datos", False)],
    ),
    (
        "¿Quién creó el sistema operativo Linux?",
        3, 2,
        [("A", "Bill Gates", False), ("B", "Steve Jobs", False), ("C", "Dennis Ritchie", False), ("D", "Linus Torvalds", True)],
    ),
    (
        "¿Qué es Git?",
        3, 2,
        [("A", "Lenguaje de programación funcional", False), ("B", "Control de versiones distribuido", True), ("C", "Base de datos distribuida", False), ("D", "Framework de desarrollo web", False)],
    ),
    (
        "¿Qué es un ataque DDoS?",
        3, 2,
        [("A", "Virus que cifra archivos y pide rescate", False), ("B", "Intrusión silenciosa en sistemas", False), ("C", "Satura servidores con peticiones masivas", True), ("D", "Robo de contraseñas mediante phishing", False)],
    ),
    (
        "¿Qué es la computación cuántica?",
        3, 2,
        [("A", "Computación con procesadores estándar", False), ("B", "Usa qubits y principios cuánticos", True), ("C", "Procesamiento paralelo de big data", False), ("D", "Rama de IA que simula razonamiento", False)],
    ),
    (
        "¿Qué mejora introduce IPv6 respecto a IPv4?",
        3, 2,
        [("A", "Mayor velocidad de transmisión", False), ("B", "Más IPs disponibles (128 bits vs 32)", True), ("C", "Cifrado obligatorio de todo el tráfico", False), ("D", "Compatibilidad con redes inalámbricas", False)],
    ),
    (
        "¿En qué año fue fundada Microsoft?",
        3, 2,
        [("A", "1970", False), ("B", "1973", False), ("C", "1975", True), ("D", "1980", False)],
    ),
    (
        "¿Qué hace un compilador?",
        3, 2,
        [("A", "Ejecuta código línea a línea", False), ("B", "Traduce código fuente a código máquina", True), ("C", "Gestiona la memoria del SO", False), ("D", "Comprime archivos ejecutables", False)],
    ),
    (
        "¿Qué es el cifrado AES?",
        3, 2,
        [("A", "Protocolo de autenticación en dos pasos", False), ("B", "Estándar de cifrado simétrico avanzado", True), ("C", "Sistema de firma digital asimétrica", False), ("D", "Protocolo de intercambio de claves", False)],
    ),
    (
        "¿Qué es MapReduce?",
        3, 2,
        [("A", "Framework de JavaScript para frontends", False), ("B", "Función de agregación en SQL", False), ("C", "Procesamiento distribuido de big data", True), ("D", "Protocolo de enrutamiento de redes", False)],
    ),
    (
        "¿Qué es la virtualización en computación?",
        3, 2,
        [("A", "Crear gráficos 3D fotorrealistas", False), ("B", "Simular hardware o software lógicamente", True), ("C", "Comprimir archivos del sistema operativo", False), ("D", "Hacer copias de seguridad en la nube", False)],
    ),
    (
        "¿Qué es el protocolo HTTPS?",
        3, 2,
        [("A", "Versión más rápida de HTTP", False), ("B", "HTTP con capa de seguridad TLS/SSL", True), ("C", "Protocolo FTP con seguridad", False), ("D", "Sistema de correo electrónico cifrado", False)],
    ),
    (
        "¿Qué es una red neuronal artificial?",
        3, 2,
        [("A", "Red de computadoras físicamente unidas", False), ("B", "Inspirado en el cerebro biológico", True), ("C", "Tipo de base de datos no estructurada", False), ("D", "Algoritmo de búsqueda en grafos", False)],
    ),
    (
        "¿Qué establece el principio de menor privilegio?",
        3, 2,
        [("A", "Dar todos los permisos a cada usuario", False), ("B", "Dar solo permisos mínimos necesarios", True), ("C", "No usar contraseñas en sistemas internos", False), ("D", "Compartir accesos entre el mismo equipo", False)],
    ),

    # =========================================================================
    # DIFÍCIL — GEOGRAFÍA (cat 3) — 21 preguntas
    # =========================================================================
    (
        "¿Cuál es la profundidad máxima de la Fosa de las Marianas?",
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
        [("A", "Antiguo mar que cubría toda la Tierra", False), ("B", "Supercontinente de hace ~300 M de años", True), ("C", "Planeta similar a la Tierra", False), ("D", "Capa de hielo del hemisferio norte", False)],
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
        [("A", "Une el Atlántico con el Pacífico", False), ("B", "Paso marítimo que separa Rusia de Alaska", True), ("C", "Une el Mediterráneo con el Mar Rojo", False), ("D", "Estrecho entre la India y Sri Lanka", False)],
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
        "¿Cuál es la montaña más alta de Europa (Cáucaso incluido)?",
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
        "¿En qué continente hay más países sin salida al mar?",
        3, 3,
        [("A", "Asia", False), ("B", "Europa", False), ("C", "África", True), ("D", "América del Sur", False)],
    ),
]


def seed():
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
            (2, "Tecnología",  "Informática, internet e inventos"),
            (3, "Geografía",   "Países, capitales, ríos y relieves"),
        ]
        for cid, nombre, desc in categorias_data:
            session.add(Categoria(id=cid, nombre=nombre, descripcion=desc))

        session.flush()

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
