import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import os


class CellDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detección de Células Avanzada")
        self.root.geometry("1400x900")

        # Variables
        self.original_image = None
        self.processed_image = None
        self.detected_image = None
        self.cell_count = 0
        self.file_path = None

        # Crear interfaz
        self.create_widgets()

    def create_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame para controles
        control_frame = tk.Frame(main_frame)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Frame para imágenes
        image_frame = tk.Frame(main_frame)
        image_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Controles
        tk.Button(control_frame, text="Cargar Imagen", command=self.load_image).pack(fill=tk.X, pady=5)

        # Preprocesamiento
        preprocess_frame = tk.LabelFrame(control_frame, text="Preprocesamiento")
        preprocess_frame.pack(fill=tk.X, pady=5)

        self.gray_var = tk.IntVar(value=1)
        tk.Checkbutton(preprocess_frame, text="Escala de Grises", variable=self.gray_var).pack(anchor=tk.W)

        self.blur_var = tk.IntVar(value=1)
        tk.Checkbutton(preprocess_frame, text="Eliminar Ruido (Gaussiano)", variable=self.blur_var).pack(anchor=tk.W)

        self.equalize_var = tk.IntVar()
        tk.Checkbutton(preprocess_frame, text="Ecualización de Histograma", variable=self.equalize_var).pack(
            anchor=tk.W)

        # Umbralización
        threshold_frame = tk.LabelFrame(control_frame, text="Umbralización")
        threshold_frame.pack(fill=tk.X, pady=5)

        self.threshold_method = tk.StringVar(value="otsu")
        tk.Radiobutton(threshold_frame, text="Umbral Otsu", variable=self.threshold_method, value="otsu").pack(
            anchor=tk.W)
        tk.Radiobutton(threshold_frame, text="Umbral Adaptativo", variable=self.threshold_method,
                       value="adaptive").pack(anchor=tk.W)

        # Morfología
        morph_frame = tk.LabelFrame(control_frame, text="Morfología Matemática")
        morph_frame.pack(fill=tk.X, pady=5)

        self.morph_operation = tk.StringVar(value="open")
        tk.Radiobutton(morph_frame, text="Ninguna", variable=self.morph_operation, value="ninguna").pack(anchor=tk.W)
        tk.Radiobutton(morph_frame, text="Dilatación", variable=self.morph_operation, value="dilate").pack(anchor=tk.W)
        tk.Radiobutton(morph_frame, text="Erosión", variable=self.morph_operation, value="erode").pack(anchor=tk.W)
        tk.Radiobutton(morph_frame, text="Apertura", variable=self.morph_operation, value="open").pack(anchor=tk.W)
        tk.Radiobutton(morph_frame, text="Cierre", variable=self.morph_operation, value="close").pack(anchor=tk.W)

        # Detección
        detect_frame = tk.LabelFrame(control_frame, text="Detección de Células")
        detect_frame.pack(fill=tk.X, pady=5)

        self.min_radius = tk.IntVar(value=5)
        self.max_radius = tk.IntVar(value=30)

        tk.Label(detect_frame, text="Radio mínimo:").pack(anchor=tk.W)
        tk.Entry(detect_frame, textvariable=self.min_radius).pack(fill=tk.X)

        tk.Label(detect_frame, text="Radio máximo:").pack(anchor=tk.W)
        tk.Entry(detect_frame, textvariable=self.max_radius).pack(fill=tk.X)

        # Procesar
        tk.Button(control_frame, text="Procesar y Detectar Células", command=self.process_and_detect).pack(fill=tk.X,
                                                                                                           pady=10)

        # Contador de células
        self.count_label = tk.Label(control_frame, text="Células detectadas: 0", font=('Arial', 12, 'bold'))
        self.count_label.pack(fill=tk.X, pady=5)

        # Guardar
        tk.Button(control_frame, text="Guardar Imagen Procesada", command=self.save_processed_image).pack(fill=tk.X,
                                                                                                          pady=5)
        tk.Button(control_frame, text="Guardar Imagen con Detección", command=self.save_detected_image).pack(fill=tk.X,
                                                                                                             pady=5)

        # Visualización de imágenes
        img_top_frame = tk.Frame(image_frame)
        img_top_frame.pack(fill=tk.BOTH, expand=True)

        img_bottom_frame = tk.Frame(image_frame)
        img_bottom_frame.pack(fill=tk.BOTH, expand=True)

        self.original_label = tk.Label(img_top_frame, text="Imagen Original", borderwidth=2, relief="groove")
        self.original_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.processed_label = tk.Label(img_top_frame, text="Imagen Procesada", borderwidth=2, relief="groove")
        self.processed_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.detected_label = tk.Label(img_bottom_frame, text="Células Detectadas", borderwidth=2, relief="groove")
        self.detected_label.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.tif;*.tiff")])
        if file_path:
            self.file_path = file_path
            self.original_image = cv2.imread(file_path)
            self.show_image(self.original_image, self.original_label)
            self.processed_image = None
            self.detected_image = None
            self.processed_label.config(image='')
            self.detected_label.config(image='')
            self.processed_label.config(text="Imagen Procesada")
            self.detected_label.config(text="Células Detectadas")
            self.cell_count = 0
            self.update_count_label()

    def show_image(self, image, label):
        if image is None:
            return

        # Convertir de BGR a RGB si es a color
        if len(image.shape) == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)

        # Convertir a formato PIL
        image_pil = Image.fromarray(image_rgb)

        # Redimensionar manteniendo aspecto
        label_width = label.winfo_width() - 20
        label_height = label.winfo_height() - 20

        if label_width <= 1 or label_height <= 1:
            label_width = 500
            label_height = 500

        aspect_ratio = image.shape[1] / image.shape[0]

        if aspect_ratio > 1:
            new_width = label_width
            new_height = int(label_width / aspect_ratio)
        else:
            new_height = label_height
            new_width = int(label_height * aspect_ratio)

        image_pil = image_pil.resize((new_width, new_height), Image.LANCZOS)

        # Convertir a ImageTk
        image_tk = ImageTk.PhotoImage(image_pil)

        # Mostrar en el label
        label.config(image=image_tk)
        label.image = image_tk

    def process_image(self):
        if self.original_image is None:
            messagebox.showerror("Error", "Por favor cargue una imagen primero")
            return None

        processed = self.original_image.copy()

        # RF2: Preprocesamiento - Escala de grises
        if self.gray_var.get():
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

        # RF2: Preprocesamiento - Eliminar ruido
        if self.blur_var.get() and len(processed.shape) == 2:
            processed = cv2.GaussianBlur(processed, (5, 5), 0)

        # RF4: Ecualización de histograma
        if self.equalize_var.get() and len(processed.shape) == 2:
            processed = cv2.equalizeHist(processed)

        # RF3: Morfología matemática
        kernel = np.ones((5, 5), np.uint8)
        morph_op = self.morph_operation.get()

        if len(processed.shape) == 3:
            processed = cv2.cvtColor(processed, cv2.COLOR_BGR2GRAY)

        if morph_op == "dilate":
            processed = cv2.dilate(processed, kernel, iterations=1)
        elif morph_op == "erode":
            processed = cv2.erode(processed, kernel, iterations=1)
        elif morph_op == "open":
            processed = cv2.morphologyEx(processed, cv2.MORPH_OPEN, kernel)
        elif morph_op == "close":
            processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, kernel)

        # Umbralización
        if self.threshold_method.get() == "otsu":
            _, processed = cv2.threshold(processed, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        else:
            processed = cv2.adaptiveThreshold(processed, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                              cv2.THRESH_BINARY_INV, 11, 2)

        return processed

    def detect_cells(self, processed):
        # Encontrar contornos
        contours, _ = cv2.findContours(processed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar por tamaño (basado en radio)
        min_area = np.pi * (self.min_radius.get() ** 2)
        max_area = np.pi * (self.max_radius.get() ** 2)

        valid_cells = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if min_area <= area <= max_area:
                valid_cells.append(cnt)

        # Crear imagen con detecciones
        detected_img = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)

        for cnt in valid_cells:
            # Dibujar contorno
            cv2.drawContours(detected_img, [cnt], -1, (0, 255, 0), 2)

            # Dibujar centroide
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(detected_img, (cX, cY), 3, (255, 0, 0), -1)

        # Mostrar conteo
        self.cell_count = len(valid_cells)
        self.update_count_label()

        # Añadir texto con el conteo
        cv2.putText(detected_img, f"Células detectadas: {self.cell_count}",
                    (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 2)

        return detected_img

    def update_count_label(self):
        self.count_label.config(text=f"Células detectadas: {self.cell_count}")

    def process_and_detect(self):
        processed = self.process_image()
        if processed is not None:
            self.processed_image = processed
            self.show_image(processed, self.processed_label)

            # Detectar células
            self.detected_image = self.detect_cells(processed)
            self.show_image(self.detected_image, self.detected_label)

    def save_processed_image(self):
        if self.processed_image is None:
            messagebox.showerror("Error", "No hay imagen procesada para guardar")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg")])
        if file_path:
            # Convertir a 3 canales si es binaria
            if len(self.processed_image.shape) == 2:
                save_img = cv2.cvtColor(self.processed_image, cv2.COLOR_GRAY2BGR)
            else:
                save_img = self.processed_image

            cv2.imwrite(file_path, save_img)
            messagebox.showinfo("Éxito", "Imagen procesada guardada correctamente")

    def save_detected_image(self):
        if self.detected_image is None:
            messagebox.showerror("Error", "No hay imagen con detección para guardar")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                            ("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, cv2.cvtColor(self.detected_image, cv2.COLOR_RGB2BGR))
            messagebox.showinfo("Éxito", "Imagen con detección guardada correctamente")


if __name__ == "__main__":
    root = tk.Tk()
    app = CellDetectionApp(root)
    root.mainloop()