🧬 Detección de Células Avanzada

🎯 Objetivo

Desarrollar una aplicación interactiva que permita cargar imágenes microscópicas, preprocesarlas y detectar células automáticamente mediante técnicas de visión por computadora, con el fin de facilitar el análisis visual y el conteo de células en entornos académicos o de investigación básica. Esta herramienta busca ser accesible, configurable y visualmente clara para usuarios con conocimientos básicos en procesamiento digital de imágenes.

📷 Características Principales
* Carga de imágenes (.png, .jpg, .jpeg, .tif, .tiff)

Opciones de preprocesamiento:
* Conversión a escala de grises
* Filtro Gaussiano para eliminar ruido
  

Métodos de umbralización:
* Umbral adaptativo gaussiano

Operaciones morfológicas:
* Dilatación
* Erosión
* Apertura
* Cierre
* Detección de células basada en contornos con filtrado por área (radio mínimo y máximo)

Visualización de:
* Imagen original
* Imagen procesada
* Imagen con células detectadas
* Guardado de resultados
* Contador automático de células detectadas

📦 Requisitos
Asegúrate de tener Python 3 instalado y ejecuta:

* pip install opencv-python numpy pillow matplotlib

🛠 Tecnologías Usadas
* OpenCV para procesamiento de imágenes
* Tkinter para la GUI
* NumPy para operaciones matemáticas
* Pillow (PIL) para visualización en GUI
* Matplotlib para soporte gráfico (opcional)

📌 Notas
* El filtrado por área se basa en el área de un círculo usando los radios mínimo y máximo proporcionados.

* La imagen final con detección incluye contornos en verde y centroides en azul.

👥 Autores
* Juan Carlos Conde Marrufo
* Didier Andrey Tec Esquivel
