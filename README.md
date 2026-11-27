# 🍍 Reconocimiento de frutas en percha

Sistema de visión por computador que localiza y recorta cada fruta en fotos de percha de supermercado, como base para reconocer el producto.

**Equipo:**  Sebastián Alvarado · Daniel Pacheco ·  Cinthya Ramón · Fernando Sánchez

## Estructura

```
vc-frutas-percha/
├── README.md
├── requirements.txt
├── docs/
├── adr/
├── notebooks/
├── src/utils.py
├── figuras/
├── resultados/
└── data/
    ├── raw/
    ├── anotaciones/
    └── procesada/
```

| Carpeta | Contenido |
| --- | --- |
| `docs/` | Spike del proyecto |
| `adr/` | Registros de decisión ADR-01 a ADR-07 |
| `notebooks/` | Cuadernos por fase (.ipynb y .html) |
| `src/utils.py` | Funciones compartidas: `leer`, `mostrar`, `dice_iou` |
| `figuras/` | Figuras de cada fase (`a1`, `a2`, `b1`, `b2`) |
| `resultados/` | Tablas .csv de los experimentos |
| `data/raw/` | Fotos originales, en Drive |
| `data/anotaciones/` | Máscaras PNG de evaluación |
| `data/procesada/` | Salidas del pipeline |

## Fases

Hito inicial conjunto: 88 fotos de mango, manzana y banano, y 24 máscaras de evaluación. Después, dos frentes en paralelo.

| Frente | Fase | Cuaderno | Responsable | ADR |
| --- | --- | --- | --- | --- |
| A · Datos | A1 · Inventario y control de calidad | `notebooks/a1_calidad.ipynb` | Sebastián Alvarado | [ADR-01](adr/ADR-01.md), [ADR-02](adr/ADR-02.md) |
| A · Datos | A2 · División y data augmentation | `notebooks/a2_division_augmentation.ipynb` | Daniel Pacheco | [ADR-07](adr/ADR-07.md) |
| B · Segmentación | B1 · Tamaño, color y filtros de luz y ruido | `notebooks/b1_preprocesamiento.ipynb` | Fernando Sánchez | [ADR-03](adr/ADR-03.md), [ADR-04](adr/ADR-04.md), [ADR-05](adr/ADR-05.md) |
| B · Segmentación | B2 · Segmentación clásica y recorte | `notebooks/b2_segmentacion.ipynb` | Cinthya Ramón | [ADR-06](adr/ADR-06.md) |

Diseño experimental: [docs/SPIKE.md](docs/SPIKE.md)

## Flujo de trabajo

1. Clonar el repositorio y crear una rama propia: `git checkout -b <nombre>`
2. Descargar las fotos de Drive en `data/raw/`.
3. Instalar dependencias: `pip install -r requirements.txt`
4. Trabajar en el cuaderno y la ADR asignados.
5. Subir la rama y abrir un Pull Request a `main`.

## Datos

- Fotos propias y datasets públicos en Drive ([data/README.md](data/README.md)).
- Formato de nombre de las fotos propias: `clase_estado_persona_fecha_numero.jpg`
