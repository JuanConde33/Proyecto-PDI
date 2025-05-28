import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import os

# Función para cargar la imagen mediante un cuadro de diálogo
def cargar_imagen():
    root = tk.Tk()           # Crea una ventana principal
    root.withdraw()          # Oculta la ventana principal
    # Muestra un diálogo para seleccionar un archivo de imagen
    ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
    return ruta

# Función para seleccionar la carpeta donde se guardarán las imágenes resultantes
def seleccionar_carpeta_destino():
    root = tk.Tk()
    root.withdraw()
    # Muestra un diálogo para seleccionar una carpeta
    carpeta = filedialog.askdirectory(title="Selecciona una carpeta para guardar las imágenes")
    return carpeta

# Función principal de procesamiento de imagen
def procesar_imagen(ruta):
    # Carga la imagen original
    imagen_original = cv2.imread(ruta)

    # Aplica un filtro Gaussiano para reducir el ruido
    imagen_suavizada = cv2.GaussianBlur(imagen_original, (5, 5), 0)

    # Convierte la imagen suavizada a escala de grises
    gris = cv2.cvtColor(imagen_suavizada, cv2.COLOR_BGR2GRAY)

    # Aplica umbral adaptativo para separar objetos del fondo
    umbral = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                   cv2.THRESH_BINARY_INV, 11, 1)

    # Crea un kernel para operaciones morfológicas
    kernel = np.ones((3, 3), np.uint8)
    # Aplica apertura morfológica para limpiar ruido en la imagen binaria
    apertura = cv2.morphologyEx(umbral, cv2.MORPH_OPEN, kernel, iterations=2)

    # Detecta contornos en la imagen binaria procesada
    contornos, _ = cv2.findContours(apertura, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Copia la imagen original para dibujar los contornos
    imagen_contornos = imagen_original.copy()

    # Inicializa contador de células detectadas
    contador = 0
    for cnt in contornos:
        area = cv2.contourArea(cnt)
        if area > 10:  # Filtra contornos demasiado pequeños
            contador += 1
            # Dibuja el contorno sobre la imagen
            cv2.drawContours(imagen_contornos, [cnt], -1, (0, 255, 0), 1)

    # Muestra el total de células detectadas en consola
    print(f"Total de células detectadas: {contador}")

    # Muestra las imágenes en una figura con subgráficas
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

    # Imagen con detección de contornos
    plt.subplot(1, 3, 3)
    plt.title(f"Detección de células: {contador}")
    plt.imshow(cv2.cvtColor(imagen_contornos, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    # Permite al usuario elegir la carpeta donde se guardarán las imágenes
    carpeta_destino = seleccionar_carpeta_destino()
    if carpeta_destino:
        # Obtiene el nombre base del archivo (sin extensión)
        nombre_base = os.path.splitext(os.path.basename(ruta))[0]
        # Guarda las tres imágenes procesadas en la carpeta elegida
        cv2.imwrite(os.path.join(carpeta_destino, f"{nombre_base}_original.png"), imagen_original)
        cv2.imwrite(os.path.join(carpeta_destino, f"{nombre_base}_gris.png"), gris)
        cv2.imwrite(os.path.join(carpeta_destino, f"{nombre_base}_deteccion.png"), imagen_contornos)
        print("Imágenes guardadas exitosamente.")
    else:
        print("No se seleccionó una carpeta para guardar las imágenes.")

# --- Programa principal ---
ruta_imagen = cargar_imagen()  # Pide al usuario seleccionar una imagen
if ruta_imagen:
    procesar_imagen(ruta_imagen)  # Procesa la imagen si se seleccionó
else:
    print("No se seleccionó ninguna imagen.")
