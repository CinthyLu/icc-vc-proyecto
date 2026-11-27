# Spike · Diseño experimental del Proyecto Integrador

**Integrantes:** Cinthya Ramón, Sebastián Alvarado, Daniel Pacheco, Fernando Sánchez

---

## 1. Contexto

### Problema

En la sección de frutas de un supermercado, el inventario y la reposición se controlan a simple vista. El sistema que proponemos debe **localizar y recortar cada producto (fruta) en fotos de percha**, como base para reconocerlo después.

Para este spike nos enfocamos en **3 frutas grandes y separables** (mango, manzana y banano), donde cada fruta corresponde a una región individual. Si más adelante se incorporan frutas pequeñas o amontonadas (fresa, mora, uvas), la región pasará a ser la bandeja o el grupo completo.

### Por qué un spike

Antes de desarrollar la solución completa, se realiza una exploración corta y basada en datos para decidir rápidamente qué técnica, filtro y parámetros usar en cada etapa. Cada decisión queda documentada en una **ADR** (registro de decisión) respaldada por figuras, tablas comparativas y métricas.

### Alcance del dataset (congelado)

Por indicación docente, **se cierra la fase de adquisición de nuevas imágenes** y se trabaja con las 3 frutas que ya cuentan con mayor cantidad de fotos propias reales. El resto de productos queda como extensión opcional para iteraciones futuras.

| Fruta | Fotos propias reales | Estado en este spike | Meta con augmentation |
| --- | ---: | --- | ---: |
| **Mango** | 56 | Seleccionada (núcleo) | 100 |
| **Manzana** | 18 | Seleccionada (núcleo) | 100 |
| **Banano** | 14 | Seleccionada (núcleo) | 100 |
| **Total núcleo** | **88** | **Dataset congelado** | **300** |

*Nota:* Las variaciones faltantes (baja/alta iluminación, oclusiones parciales y desenfoque) se cubrirán mediante **data augmentation**, aplicándolo únicamente sobre el conjunto de entrenamiento luego de dividir las fotos reales.

### Métricas de calidad

| Tipo | Métricas |
| --- | --- |
| Calidad de datos | Completitud, formato de nombres, duplicados (MD5) y balance por fruta |
| Calidad de imagen sin referencia | Nitidez (varianza del Laplaciano), brillo (media de $V$), contraste, ruido ($\sigma$), píxeles quemados ($\ge 250$) y dominante de color |
| Calidad de imagen con referencia | PSNR y SSIM |
| Calidad del resultado | Dice, IoU y error de conteo |
| Costo | Milisegundos por foto y memoria |

---

## 2. Tabla de filtros, kernels y parámetros a evaluar

Esta tabla define explícitamente las técnicas, tamaños de kernel y parámetros que se probarán en los experimentos del spike.

| Etapa | Técnica / Filtro | Kernels y parámetros a evaluar | Métrica de decisión |
| --- | --- | --- | --- |
| **Tamaño de trabajo** | Redimensionado | Lado máximo: `256`, `512`, `768 px` (`cv2.INTER_AREA` en imagen; `cv2.INTER_NEAREST` en máscara) | Dice (Otsu base), ms/foto |
| **Espacio de color** | Conversión de canal | `Gris`, `HSV` (canales `H`, `S`), `Lab` (canales `a*`, `b*`) | Dice (Otsu), separación de histogramas (fruta vs. fondo) |
| **Corrección de luz** *(solo si brillo $V < 100$)* | Ajuste fotométrico | Ninguna (línea base), Gamma ($\gamma = 0.7$), Ecualización global, CLAHE (`clipLimit=2.0`, `tileGridSize=(8,8)` sobre $V$) | Dice, SSIM, ms/foto |
| **Reducción de ruido** | Suavizado espacial | Ninguno (línea base), Mediana (`k=3`, `k=5`), Gaussiano (`k=3x3`, `k=5x5`, $\sigma=0$), Bilateral (`d=5`, $\sigma_{\text{color}}=50$, $\sigma_{\text{space}}=50$) | Dice, SSIM, ms/foto |
| **Morfología** | Apertura + Cierre | Elemento estructurante elíptico (`MORPH_ELLIPSE`): `3x3`, `5x5`, `7x7` | Dice, IoU |
| **Separación de regiones** | Umbral + etiquetado | Otsu + Componentes conectados vs. Otsu + Transformada de distancia + Watershed | Dice, IoU, error de conteo |
| **Bordes y recorte** | Detección de contornos | Canny (`th1=50, th2=150` y `th1=100, th2=200`) + `cv2.findContours` para extraer bounding boxes y recortes | Dice, IoU, error de conteo |
| **Data augmentation** | Transformaciones en `train` | Intensidad baja / media / alta: brillo/contraste, rotación ($\pm 15^\circ$), escala ($0.9\text{--}1.1$), oclusión parcial (cutout) y desenfoque gaussiano (`k=3x3`) | Cobertura de brillo/ruido vs. fotos reales y balance (100/fruta) |

**Regla de desempate:** Si la diferencia de Dice entre dos configuraciones es menor a $0.02$, se selecciona la opción más simple y rápida.

---

## 3. Flujo de trabajo en paralelo

Para evitar que una fase detenga a la siguiente, el equipo acuerda primero un **hito inicial conjunto** (congelar las 88 fotos y anotar las 24 máscaras de evaluación: 8 por fruta) y luego se divide en **dos frentes de trabajo simultáneos** (2 personas por frente).

### Hito 0 · Congelación y máscaras (todo el equipo, inicio)

- Verificar nombres y subir las 88 fotos reales de `mango`, `manzana` y `banano`.
- Anotar **24 máscaras de evaluación** en `makesense.ai` (8 de mango, 8 de manzana, 8 de banano; 6 fotos por integrante) y convertirlas a PNG.
- Definir una **configuración base provisional** (`512 px`, espacio `Lab/HSV` preliminar) para que el frente de segmentación pueda programar y evaluar sin esperar el cierre de preprocesamiento.

### Frente A · Datos, Calidad y Augmentation (Sebastián + Daniel)

Trabajan sobre el conjunto completo de 88 fotos reales sin depender de los resultados de segmentación.

- **Fase A1 · Inventario y Control de calidad (ADR-01, ADR-02):**
  - Validar formato de nombres, detectar duplicados (MD5) y calcular nitidez, brillo, ruido y píxeles quemados.
  - Definir umbrales de descarte por fuente, generar `calidad.csv` y figura de las 6 peores imágenes.
- **Fase A2 · División y Data Augmentation (ADR-07):**
  - Dividir **solo las fotos reales limpias** en `70/15/15` (estratificado por fruta).
  - Aplicar augmentation **solo en `train`** (baja/alta luz, rotación, escala, oclusión y desenfoque) comparando intensidad baja, media y alta hasta completar 100 imágenes por fruta.
  - Entregar tabla de distribución antes/después y comparativa de rangos de brillo y ruido.

### Frente B · Preprocesamiento y Segmentación Clásica (Fernando + Cinthya)

Trabajan en paralelo sobre las **24 fotos con máscara**.

- **Fase B1 · Tamaño, Color y Filtros de Luz/Ruido (ADR-03, ADR-04, ADR-05):**
  - Evaluar tamaños (`256`, `512`, `768 px`) con Otsu en gris (línea base).
  - Comparar canales (`gris`, `H`, `S`, `a*`, `b*`) con Dice e histogramas fruta vs. fondo.
  - Evaluar correcciones de luz (solo en fotos oscuras) y filtros de ruido (Mediana, Gaussiano, Bilateral) midiendo Dice, SSIM y tiempo.
- **Fase B2 · Segmentación Clásica y Recorte (ADR-06):**
  - Desarrollar y probar en paralelo la matriz de morfología (`3x3`, `5x5`, `7x7`), componentes conectados vs. watershed y Canny + contornos usando la configuración base provisional.
  - Al finalizar la Fase B1, conectar los parámetros ganadores de ADR-03, ADR-04 y ADR-05, re-ejecutar el cuaderno y documentar Dice, IoU, error de conteo y análisis de los 3 peores fallos (reflejos, oclusión, fondo).

### Resumen de configuraciones experimentales

| Frente | Bloque experimental | Configuraciones | ADR |
| --- | --- | ---: | --- |
| Frente A | Calidad y limpieza de datos | — | ADR-01, ADR-02 |
| Frente A | División 70/15/15 y Data Augmentation | 3 | ADR-07 |
| Frente B | Tamaño de trabajo | 1 + 3 | ADR-03 |
| Frente B | Espacio de color | 5 | ADR-04 |
| Frente B | Filtros de luz y ruido | 4 + 6 | ADR-05 |
| Frente B | Segmentación clásica (morfología, watershed, Canny) | 6 + 2 | ADR-06 |
| **Total** | | **30** | **7 ADRs** |

---

## 4. Responsables

La carga está equilibrada en dos parejas que avanzan simultáneamente. Cada integrante anota 6 máscaras, ejecuta sus experimentos, redacta sus ADR y defiende su bloque ante el docente.

| Frente | Integrante | Máscaras (24 total) | Responsabilidades | ADR |
| --- | --- | ---: | --- | --- |
| **Frente A** | **Sebastián Alvarado** | 6 (banano 4, mango 2) | Inventario del núcleo, control de calidad, duplicados y `calidad.csv` | ADR-01, ADR-02 |
| **Frente A** | **Daniel Pacheco** | 6 (banano 4, mango 2) | División 70/15/15 y diseño/evaluación de data augmentation temprano | ADR-07 |
| **Frente B** | **Fernando Sánchez** | 6 (manzana 4, mango 2) + conversión a PNG | Tamaño de trabajo, espacio de color y evaluación de filtros de luz y ruido | ADR-03, ADR-04, ADR-05 |
| **Frente B** | **Cinthya Ramón** | 6 (manzana 4, mango 2) | Segmentación clásica (morfología, watershed/componentes, Canny, recortes) e integración final con B1 | ADR-06 |
