import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# Переменные для хранения координат начала и конца прямоугольника
start_point = None
end_point = None
drawing = False

# Путь к изображению
image_path = r"images\img_pdf_1.jpg"

# Загрузка изображения
image = cv2.imread(image_path)

# Проверка загрузки изображения
if image is None:
    print("Не удалось загрузить изображение.")
else:
    # Инициализация easyocr для распознавания текста на русском языке
    reader = easyocr.Reader(['ru'], gpu=False)

    # Список для хранения прямоугольников и извлеченного текста
    rectangles = []
    extracted_texts = []

    # Функция для обработки событий клика на изображении
    def on_click(event):
        global start_point, end_point, drawing
        
        if event.button == 1:  # Левая кнопка мыши для начала рисования
            drawing = True
            start_point = (int(round(event.xdata)), int(round(event.ydata)))
        
        elif event.button == 3:  # Правая кнопка мыши для завершения рисования
            if drawing:
                end_point = (int(round(event.xdata)), int(round(event.ydata)))
                drawing = False
                draw_rectangle()
                extract_text()

    # Функция для отрисовки прямоугольника на изображении
    def draw_rectangle():
        global start_point, end_point
        
        if start_point and end_point:
            x1, y1 = start_point
            x2, y2 = end_point
            rect = Rectangle((min(x1, x2), min(y1, y2)), abs(x2 - x1), abs(y2 - y1), edgecolor='r', facecolor='none')
            ax.add_patch(rect)
            rectangles.append((min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)))
            fig.canvas.draw()

    # Функция для извлечения текста из выделенной области
    def extract_text():
        global start_point, end_point
        
        if start_point and end_point:
            x1, y1 = start_point
            x2, y2 = end_point
            roi_image = image[min(y1, y2):max(y1, y2), min(x1, x2):max(x1, x2)]
            result = reader.readtext(roi_image)
            extracted_text = " ".join([res[1] for res in result])
            extracted_texts.append(extracted_text)
            print("Извлеченный текст:", extracted_text)

    # Отображение изображения с обработчиком событий мыши
    fig, ax = plt.subplots()
    ax.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Выделите область для распознавания текста (Левая кнопка мыши для начала, Правая - для конца)")
    fig.canvas.mpl_connect('button_press_event', on_click)
    plt.axis('off')
    plt.show()

    # Вывод извлеченного текста из каждой области
    for i, text in enumerate(extracted_texts):
        print(f"Извлеченный текст {i + 1}: {text}")