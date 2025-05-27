import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt

def cargar_imagen():
    # Ventana para seleccionar archivo
    root = tk.Tk()
    root.withdraw()
    # Mostrar diálogo para seleccionar archivo de imagen
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
    return ruta

def procesar_imagen(ruta):
    # Cargar imagen
    imagen_original = cv2.imread(ruta)

    # Preprocesamiento - Reducción de ruido con filtro Gaussiano
    imagen_suavizada = cv2.GaussianBlur(imagen_original, (5, 5), 0)

    # Convertir a escala de grises
    gris = cv2.cvtColor(imagen_suavizada, cv2.COLOR_BGR2GRAY)

    # Eliminar el fondo - Umbral adaptativo + apertura morfológica
    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 1)

    # Operaciones morfológicas para limpiar la imagen binaria
    kernel = np.ones((3, 3), np.uint8)
    apertura = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel, iterations=2)

    # Encontrar contornos (células)
    contornos, _ = cv2.findContours(apertura, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Dibujar contornos encontrados sobre la imagen original
    imagen_contornos = imagen_original.copy()
    for i in range(len(contornos)):
        cv2.drawContours(imagen_contornos, contornos, i, (0, 255, 0), 1)

    # Contar células (filtro de tamaño mínimo)
    contador = 0
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area > 100:  # Ignorar pequeñas partículas (ajustar según necesidad)
            contador += 1

    print(f"Total de células detectadas: {contador}")

    # Mostrar resultado
    plt.figure(figsize=(15, 5))

    # Imagen original
    plt.subplot(1, 3, 1)
    plt.title("Original")
    plt.imshow(cv2.cvtColor(imagen_original, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    # Imagen en escala de grises
    plt.subplot(1, 3, 2)
    plt.title("Escala de grises")
    plt.imshow(gris, cmap='gray')
    plt.axis('off')

    # Imagen con detección de células
    plt.subplot(1, 3, 3)
    plt.title(f"Detección de células: {contador}")
    plt.imshow(cv2.cvtColor(imagen_contornos, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.tight_layout()
    plt.show()

# --- Programa principal ---
ruta_imagen = cargar_imagen()
if ruta_imagen:
    procesar_imagen(ruta_imagen)
else:
    print("No se seleccionó ninguna imagen.")
