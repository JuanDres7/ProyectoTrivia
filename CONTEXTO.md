# Contexto del Proyecto — Sistema de Preguntas de Opción Múltiple

## Descripción general

Aplicación de escritorio en Python que simula un juego de preguntas tipo concurso.
El sistema tiene dos módulos principales: un **módulo administrativo** (gestión de preguntas)
y un **módulo de juego** (partidas para jugadores). Proyecto académico de entrega única.

**Fecha límite de entrega:** 22 de abril de 2026 a las 8:00 PM. NO hay extensión.

**Equipo:** 3 personas. Solo Juan tiene nivel intermedio-avanzado en Python.
Los otros dos integrantes son principiantes.

---

## Requerimientos funcionales

| # | Requerimiento |
|---|---------------|
| RF-01 | Autenticación de administrador (usuario + contraseña con bcrypt) |
| RF-02 | Registro de preguntas con 4 opciones y una única respuesta correcta |
| RF-03 | Modificación de preguntas existentes |
| RF-04 | Eliminación de preguntas |
| RF-05 | Inicio de una partida de juego |
| RF-06 | Cancelación de una partida en cualquier instante |
| RF-07 | Presentación de preguntas con cuatro opciones (A, B, C, D) |
| RF-08 | Validación de respuestas del jugador |
| RF-09 | Cálculo del puntaje final (1 punto por respuesta correcta) |
| RF-10 | Registro del jugador y su puntaje |
| RF-11 | Consulta del histórico de jugadores |
| RF-12 | Verificación automática de récord global |

### Requerimientos opcionales (valor extra)
- Temporizador por pregunta
- Presentación aleatoria de preguntas
- Diferentes niveles de dificultad
- Ranking Top 10 jugadores

### Validaciones obligatorias
- No se permiten preguntas duplicadas (mismo enunciado)
- Cada pregunta debe tener exactamente 4 opciones
- Solo una opción puede ser la correcta

---

## Flujo del juego

1. El jugador ingresa su nombre
2. Selecciona un nivel (Fácil / Medio / Difícil) — esto determina la cantidad de preguntas y el tiempo límite por pregunta
3. Se presentan N preguntas aleatorias del nivel elegido, una por una, cada una con 4 opciones
4. Por cada respuesta correcta suma 1 punto
5. Al finalizar se muestra nombre del jugador y puntaje final
6. El sistema compara contra el récord histórico y muestra "¡Nuevo récord!" o "No superaste el récord actual"
7. La partida se registra en el historial

---

## Herramientas y dependencias

| Herramienta | Uso |
|---|---|
| Python 3.11+ | Lenguaje base |
| customtkinter 5.2.2 | Interfaz gráfica principal |
| tkinter.ttk | Widget de tablas (Treeview) en el panel admin |
| tkinter.messagebox | Ventanas emergentes de error, info y confirmación |
| SQLModel 0.0.21 | ORM para mapeo de modelos a SQLite |
| SQLite3 | Motor de base de datos (viaja dentro del proyecto) |
| bcrypt 4.2.1 | Hashing de contraseñas del administrador |
| random | Selección aleatoria de preguntas por partida |
| threading | Temporizador sin bloquear la UI |
| datetime | Fechas en partidas y ranking |
| unittest | Casos de prueba |
| venv + requirements.txt | Entorno reproducible entre los 3 computadores |

---

## Arquitectura — 3 capas

```
UI (customtkinter) → Services (lógica de negocio) → Repository (acceso a datos) → SQLite
```

- Dependencias **unidireccionales**: UI llama a Services, Services llama a Repository, Repository accede a la BD. Nunca al revés ni saltando capas.
- Inyección de dependencias desde `main.py`
- La sesión de SQLModel se gestiona en `database.py` y se pasa a los repositories

---

## Modelo de base de datos — 9 tablas

### Dominio Autenticación
```
usuarios (id, username, password_hash)
```

### Dominio Contenido
```
niveles_dificultad (id, nombre, num_preguntas, tiempo_limite_seg)
categorias         (id, nombre, descripcion, activa)
preguntas          (id, categoria_id FK, nivel_id FK, enunciado, activa)
opciones           (id, pregunta_id FK, letra, texto, es_correcta)
```

### Dominio Partidas
```
jugadores  (id, nombre, total_partidas)
partidas   (id, jugador_id FK, nivel_id FK, total_preguntas, respuestas_correctas, puntaje_final, estado, fecha)
respuestas (id, partida_id FK, pregunta_id FK, opcion_elegida_id FK, es_correcta, puntos_obtenidos)
ranking    (id, jugador_id FK, nivel_id FK, puntaje, es_record_global, fecha)
```

### Datos de los niveles (seed)
| id | nombre | num_preguntas | tiempo_limite_seg |
|----|--------|--------------|-------------------|
| 1 | Fácil | 10 | 30 |
| 2 | Medio | 15 | 25 |
| 3 | Difícil | 20 | 20 |

### Notas del modelo
- `usuarios` es una isla de autenticación, no se conecta a otras tablas por diseño
- `partidas.estado` puede ser: `en_curso`, `finalizada`, `cancelada`
- `opciones.letra` almacena A, B, C o D
- `preguntas.categoria_id` es opcional (puede ser NULL)

---

## Estructura de carpetas

```
ProyectoTrivia/
│
├── main.py                          ← Entry point + inyección de dependencias
├── requirements.txt                 ← customtkinter, sqlmodel, bcrypt
├── .gitignore
├── CONTEXTO.md                      ← Este archivo
├── plan_backend.docx                ← Funciones a implementar por archivo
│
├── scripts/
│   └── seed_data.py                 ← Crea admin + 3 niveles de dificultad
│
└── app/
    ├── config/
    │   └── settings.py              ← Constantes globales (colores, fuentes, etc.)
    │
    ├── database/
    │   ├── database.py              ← Engine SQLite + get_session()
    │   └── models/
    │       ├── __init__.py          ← Exporta todos los modelos
    │       ├── autenticacion.py     ← Usuario
    │       ├── contenido.py         ← NivelDificultad, Categoria, Pregunta, Opcion
    │       └── partidas.py          ← Jugador, Partida, Respuesta, Ranking
    │
    ├── repository/                  ← Acceso a datos (inserts, selects, updates)
    │   ├── usuario_repository.py    ← Juan
    │   ├── contenido_repository.py  ← Persona 2
    │   └── partida_repository.py    ← Persona 3
    │
    ├── services/                    ← Lógica de negocio
    │   ├── auth_service.py          ← Juan
    │   ├── contenido_service.py     ← Persona 2
    │   └── partida_service.py       ← Persona 3
    │
    ├── ui/                          ← Interfaz customtkinter
    │   ├── app.py                   ← Ventana raíz + navegación entre frames (Juan)
    │   ├── login_frame.py           ← Juan
    │   ├── menu_frame.py            ← Juan
    │   ├── admin_categorias_frame.py   ← Persona 2
    │   ├── admin_niveles_frame.py      ← Persona 2
    │   ├── admin_preguntas_frame.py    ← Persona 2
    │   ├── ingreso_jugador_frame.py    ← Persona 3
    │   ├── seleccion_nivel_frame.py    ← Persona 3
    │   ├── pregunta_frame.py           ← Persona 3
    │   └── resultado_frame.py          ← Persona 3
    │
    └── tests/
        ├── test_contenido_service.py   ← Persona 2
        └── test_partida_service.py     ← Persona 3
```

---

## Estado actual del proyecto

| Archivo | Estado |
|---------|--------|
| `requirements.txt` | ✅ Completo |
| `app/database/models/autenticacion.py` | ✅ Completo |
| `app/database/models/contenido.py` | ✅ Completo |
| `app/database/models/partidas.py` | ✅ Completo |
| `app/database/models/__init__.py` | ✅ Completo |
| `app/database/database.py` | ⬜ Pendiente |
| `app/config/settings.py` | ⬜ Pendiente |
| `scripts/seed_data.py` | ⬜ Pendiente |
| `app/repository/*.py` | ⬜ Pendiente |
| `app/services/*.py` | ⬜ Pendiente |
| `app/ui/*.py` | ⬜ Pendiente |
| `main.py` | ⬜ Pendiente |

---

## Decisiones de diseño tomadas

- Sin auditoría ni logs (proyecto de entrega única)
- Sin roles (un solo tipo de administrador)
- Sin sesiones persistentes (customtkinter maneja estado en memoria)
- 1 punto por pregunta independientemente del nivel
- SQLite porque la BD viaja dentro de la carpeta del proyecto
- `quiz.db` va en `.gitignore` — cada integrante genera su propia BD con `seed_data.py`
- `usuarios` no se conecta con `jugadores` por diseño: el admin y los jugadores son entidades separadas
- El nivel determina tanto la dificultad de las preguntas como la cantidad y el tiempo límite
