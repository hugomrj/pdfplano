import cv2
import numpy as np
from PIL import Image

def limpiar_imagen(pil_image):
    # 1. Convertir a formato OpenCV
    img = np.array(pil_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 2. Aumentar el contraste (Hacer los negros más negros y blancos más blancos)
    # Sin llegar al blanco y negro puro de Otsu.
    alpha = 1.5 # Contraste (1.0-3.0)
    beta = 0    # Brillo
    ajustada = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

    # 3. Suavizado muy leve para eliminar granos del escaneo
    suave = cv2.bilateralFilter(ajustada, 9, 75, 75)

    return Image.fromarray(suave)