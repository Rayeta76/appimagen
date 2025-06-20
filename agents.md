# 🧩 Agents Overview – Proyecto *appimagen*

> Versión: 0.1 — 20 jun 2025  
> Autor: Rayeta76

---

## 📜 Propósito del documento
Este fichero describe los “agentes” o componentes inteligentes de la aplicación, cómo se comunican entre sí
y qué dependencias externas usan. Así cualquier colaborador (¡o tu “yo” del futuro!) entenderá la arquitectura
sin leer todo el código.

---

## 1. Agentes principales

| Agente | Módulo / Clase | Entradas | Salidas | Responsabilidad |
|--------|----------------|----------|---------|-----------------|
| **Florence2ImageTagger** | `processing/florence_wrapper.py::Florence2ImageTagger` | Ruta de imagen (`str`) | `title:str`, `description:str`, `tags:list[str]` | Invoca el checkpoint local de Florence 2 para generar metadatos. |
| **DBManager** | `processing/db.py::DBManager` | Objetos `ImageRecord` + `TagRecord` | Inserta/actualiza filas en SQLite | Persistir imágenes, etiquetas y relaciones N-a-N. |
| **ThumbnailGenerator** | `processing/thumbnails.py::ThumbnailGenerator` | Ruta de imagen, tamaño (`int`) | Ruta de miniatura | Crear y almacenar miniaturas en `./thumbnails/`. |
| **MainWindow** | `gui/main_window.py::MainWindow` | Señales de GUI | Señales a *workers* | Orquestar selección de carpeta y cola de procesamiento. |
| **SearchWindow** | `gui/search_window.py::SearchWindow` | Texto de búsqueda, filtros | Lista de registros + miniaturas | Consultas `LIKE` en SQLite y renderizado de resultados. |

---

## 2. Flujo de trabajo

```text
User → MainWindow ──[folder]──▶ WorkerPool
        ▲                        │
        │                        ▼
        └── ProgressBar ◀─ ResultsHandler
                               │
                               ▼
Florence2ImageTagger → ThumbnailGenerator → DBManager
