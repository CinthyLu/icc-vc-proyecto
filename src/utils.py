"""Funciones compartidas por todos los cuadernos."""
from pathlib import Path
import cv2, numpy as np, matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parents[1]
DATA, FIG = RAIZ / 'data', RAIZ / 'figuras'


def leer(ruta, lado=None):
    """Lee una imagen en BGR; si se da `lado`, reduce su lado mayor a ese tamaño."""
    img = cv2.imread(str(ruta))
    if lado:
        escala = lado / max(img.shape[:2])
        if escala < 1:
            img = cv2.resize(img, None, fx=escala, fy=escala, interpolation=cv2.INTER_AREA)
    return img


def mostrar(imgs, titulos, archivo=None, columnas=None):
    """Muestra imágenes lado a lado (original + transformaciones) y guarda la figura."""
    columnas = columnas or len(imgs)
    filas = int(np.ceil(len(imgs) / columnas))
    fig, ax = plt.subplots(filas, columnas, figsize=(3 * columnas, 3.2 * filas), squeeze=False)
    for a in ax.flat:
        a.axis('off')
    for a, im, t in zip(ax.flat, imgs, titulos):
        a.imshow(cv2.cvtColor(im, cv2.COLOR_BGR2RGB) if im.ndim == 3 else im, cmap='gray')
        a.set_title(t, fontsize=9)
    plt.tight_layout()
    if archivo:
        plt.savefig(FIG / archivo, dpi=200)
    plt.show()


def dice_iou(pred, real):
    """Dice e IoU entre una máscara predicha y la anotada."""
    p, r = pred > 0, real > 0
    inter, union = (p & r).sum(), (p | r).sum()
    return 2 * inter / (p.sum() + r.sum()), inter / union
