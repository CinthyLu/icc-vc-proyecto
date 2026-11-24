# Spike · Diseño experimental del Proyecto Integrador

**Integrantes:** Cinthya Ramón, Sebastián Alvarado, Daniel Pacheco, Fernando Sánchez

---

## 1. Contexto

### Problema
En la sección de frutas de un supermercado, el inventario y la reposición se controlan a simple vista. El sistema que proponemos debe **localizar y recortar cada producto (fruta) en fotos de percha**, como base para reconocerlo después.

En fruta grande y separable (piña, mango, aguacate, naranja, manzana, pera, limón, banano) cada fruta es una región. En fruta pequeña o amontonada (fresa, mora, uvas), la región es la bandeja o el grupo completo.

### Por qué un spike
Antes de desarrollar la solución completa, se hace una exploración corta para decidir **con datos** qué técnica usar en cada fase. Cada decisión queda registrada en una ADR (registro de decisión).

### Dataset actual (fotos propias reales)
| Fruta | Propias | Meta mínima de reales |
|---|---|---|
| mango | 56 | 20 |
| manzana | 18 | 20 |
| banano | 14 | 20 |
| aguacate | 12 | 20 |
| fresa | 11 | 20 |
| naranja | 11 | 20 |
| piña | 11 | 20 |
| pera | 4 | 20 |
| limón | 2 | 20 |
| mora | 2 | 20 |

**Meta:** 100 imágenes por producto, completando con data augmentation.

### Métricas de calidad
| Tipo | Métricas |
|---|---|
| Calidad de datos | Completitud, formato de nombres, duplicados, fotos por fruta |
| Calidad de imagen sin referencia | Nitidez (varianza del Laplaciano), brillo, contraste, ruido (σ), píxeles quemados, dominante de color |
| Calidad de imagen con referencia | PSNR, SSIM |
| Calidad del resultado | Dice, IoU, error de conteo (solo frutas separables) |
| Costo | Milisegundos por foto, memoria |

---

## 2. Fases

Cada fase indica qué recibe de la anterior, qué opciones se prueban y con qué métrica se decide.

### Fase 1 · Completar el dataset
- **Objetivo:** tener suficientes fotos reales por fruta para llegar a 100 con augmentation.
- **Entrada:** fotos propias actuales y registro de captura.
- **Qué se hace:** capturar las fotos faltantes, registrar las condiciones de captura (lugar, luz, dispositivo, fondo) y verificar el formato de nombres.
- **Métrica:** fotos reales por fruta, completitud del registro.
- **Resultado:** ADR-01

### Fase 2 · Control de calidad y limpieza
- **Objetivo:** decidir qué fotos se descartan y cuáles se corrigen.
- **Entrada:** dataset de la Fase 1.
- **Opciones:** umbrales de nitidez, brillo, ruido y quemado por fuente; detección de duplicados.
- **Métrica:** % de fotos descartadas o marcadas por fuente.
- **Resultado:** ADR-02

### Fase 3 · Tamaño de trabajo
- **Objetivo:** igualar la resolución de todas las fuentes al menor costo sin perder calidad.
- **Entrada:** fotos limpias de la Fase 2; línea base sin procesamiento (Otsu en gris).
- **Opciones:** lado máximo de 256, 512 y 768 px.
- **Métrica:** Dice de la línea base y milisegundos por foto.
- **Resultado:** ADR-03

### Fase 4 · Representación y espacio de color
- **Objetivo:** elegir el canal que mejor separa la fruta del fondo de percha.
- **Entrada:** tamaño elegido en la Fase 3.
- **Opciones:** gris, S y H (HSV), a* y b* (Lab).
- **Métrica:** Dice con umbral de Otsu; histogramas por canal como evidencia.
- **Resultado:** ADR-04

### Fase 5 · Preprocesamiento: luz y ruido
- **Objetivo:** corregir solo lo que afecta al resultado.
- **Entrada:** canal elegido en la Fase 4.
- **Opciones de luz** (solo fotos oscuras): ninguna, gamma, ecualización global, CLAHE.
- **Opciones de ruido:** ninguno, mediana, gaussiano, bilateral.
- **Métrica:** Dice, SSIM y milisegundos por foto.
- **Resultado:** ADR-05

### Fase 6 · Segmentación clásica
- **Objetivo:** obtener una región por producto y recortarla.
- **Entrada:** pipeline de preprocesamiento de la Fase 5.
- **Opciones:** kernel morfológico 3, 5 o 7 × separación por componentes conectados o watershed; bordes con Canny y contornos para el recorte.
- **Métrica:** Dice, IoU, error de conteo en frutas separables; análisis de fallos (reflejos, oclusión, fondo).
- **Resultado:** ADR-06

### Fase 7 · División y data augmentation
- **Objetivo:** dividir 70/15/15 y completar 100 imágenes por producto sin inflar la evaluación.
- **Entrada:** fotos reales procesadas; variaciones que las Fases 5 y 6 no corrigieron.
- **Qué se hace:** primero se divide con las fotos reales (estratificado por fruta y fuente) y después se aumenta solo entrenamiento.
- **Opciones:** intensidad baja, media o alta de iluminación, rotación, escala, oclusión y desenfoque; número de variaciones por foto real.
- **Métrica:** imágenes por fruta, el rango de brillo y ruido del entrenamiento aumentado frente al de las fotos propias.
- **Resultado:** ADR-07

### Resumen del encadenamiento
| Fase | Entra con | Configuraciones |
|---|---|---|
| 1 Completar dataset | fotos actuales | — |
| 2 Control de calidad | dataset completo | — |
| 3 Tamaño | fotos limpias | 1 + 3 |
| 4 Espacio de color | tamaño elegido | 5 |
| 5 Luz y ruido | canal elegido | 4 + 4 |
| 6 Segmentación | pipeline elegido | 6 |
| 7 División y augmentation | regiones y variaciones pendientes | 3 |
| **Total** | | **26** |

---

## 3. Responsables

La carga es igual para todos: cada integrante captura una parte de las fotos faltantes, anota una parte de las 30 máscaras de evaluación y se encarga de sus fases con su ADR. Cada uno defiende su parte ante el docente.

| Integrante | Fotos faltantes | Máscaras | Fases | ADR |
|---|---|---|---|---|
| **Sebastián Alvarado** | pera, limón | 8 | Fase 1 · Completar el dataset y Fase 2 · Control de calidad | ADR-01, ADR-02 |
| **Fernando Sánchez** | mora, banano, manzana | 8 | Fase 3 · Tamaño de trabajo y Fase 4 · Espacio de color | ADR-03, ADR-04 |
| **Daniel Pacheco** | aguacate, fresa | 7 | Fase 5 · Luz y ruido y Fase 7 · División y augmentation | ADR-05, ADR-07 |
| **Cinthya Ramón** | naranja, piña | 7 | Fase 6 · Segmentación clásica | ADR-06 |
