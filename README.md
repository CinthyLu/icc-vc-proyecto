# 🍍 Reconocimiento de frutas en percha

Sistema de visión por computador que localiza y recorta cada fruta en fotos de percha de supermercado, como base para reconocer el producto.

**Equipo:** Cinthya Ramón · Sebastián Alvarado · Daniel Pacheco · Fernando Sánchez

## Estructura

```
vc-frutas-percha/
├── README.md
├── requirements.txt
├── docs/                 # spike e instrucciones del equipo
├── adr/                  # una decisión por fase (ADR-01 … ADR-07)
├── notebooks/            # un cuaderno por fase (.ipynb y .html)
├── src/utils.py          # funciones compartidas (leer, mostrar, dice_iou)
├── figuras/fase1 … fase7 # figuras que genera cada cuaderno
├── resultados/           # tablas .csv de cada experimento
└── data/
    ├── raw/              # fotos originales (NO se suben: van por Drive)
    ├── anotaciones/      # máscaras PNG de evaluación (sí se suben)
    └── procesada/        # salidas del pipeline (NO se suben)
```

## Fases

| Fase | Cuaderno | Responsable | Decisión |
|---|---|---|---|
| 1 · Completar el dataset | `notebooks/fase1_dataset.ipynb` | Sebastián | [ADR-01](adr/ADR-01.md) |
| 2 · Control de calidad y limpieza | `notebooks/fase2_calidad.ipynb` | Sebastián | [ADR-02](adr/ADR-02.md) |
| 3 · Tamaño de trabajo | `notebooks/fase3_tamano.ipynb` | Fernando | [ADR-03](adr/ADR-03.md) |
| 4 · Espacio de color | `notebooks/fase4_color.ipynb` | Fernando | [ADR-04](adr/ADR-04.md) |
| 5 · Luz y ruido | `notebooks/fase5_preprocesamiento.ipynb` | Daniel | [ADR-05](adr/ADR-05.md) |
| 6 · Segmentación clásica | `notebooks/fase6_segmentacion.ipynb` | Cinthya | [ADR-06](adr/ADR-06.md) |
| 7 · División y augmentation | `notebooks/fase7_division_augmentation.ipynb` | Daniel | [ADR-07](adr/ADR-07.md) |

Cada fase usa lo que decidió la ADR de la fase anterior.

## Cómo trabajar

1. Clonar el repo y crear tu rama: `git checkout -b <tu-nombre>`
2. Descargar las fotos de Drive en `data/raw/` (esa carpeta no se sube).
3. Instalar dependencias: `pip install -r requirements.txt`
4. Trabajar solo en tu cuaderno y tu ADR.
5. Subir tu rama y abrir un Pull Request a `main`. Cinthya revisa y fusiona.

## Datos

- Fotos propias y datasets públicos: carpeta compartida de Drive (enlace en `data/README.md`).
- Nombre de fotos propias: `clase_estado_persona_fecha_numero.jpg`
