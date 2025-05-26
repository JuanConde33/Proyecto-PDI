Idea del Proyecto: Restaurador de Fotos Antiguas
Participantes: Juan Conde y Didier Tec
Este proyecto tiene como objetivo desarrollar una herramienta digital que permita contar células automáticamente en imágenes microscópicas, usando técnicas de procesamiento de imágenes.
Este tipo de tarea suele hacerse manualmente en laboratorios, lo que puede ser lento y propenso a errores, especialmente cuando hay muchas células o están muy juntas.
La aplicación está hecha en Python y utiliza bibliotecas como OpenCV y NumPy. El usuario solo necesita cargar una imagen de microscopía, y el sistema realiza varias etapas: 
convierte la imagen a escala de grises, mejora el contraste, aplica una técnica de umbral adaptativo o segmentación por Watershed para separar células pegadas, y finalmente detecta los contornos para contar cada célula individual.
El resultado muestra la imagen original con las células detectadas y el número total de células contadas. Este proyecto busca ofrecer una solución simple y eficiente para apoyar a estudiantes o investigadores en tareas básicas de
análisis celular sin necesidad de software especializado o costoso.
