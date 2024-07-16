import fitz  # PyMuPDF
import cv2
import numpy as np

# Глобальные переменные
rect_start = None
rect_end = None
drawing = False
rectangles = []

# Функция для обработки событий мыши
def draw_rectangle(event, x, y, flags, param):
    global rect_start, rect_end, drawing, rectangles, img

    if event == cv2.EVENT_LBUTTONDOWN:
        rect_start = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, rect_start, (x, y), (0, 255, 0), 2)
            cv2.imshow(window_name, img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        rect_end = (x, y)
        drawing = False
        rectangles.append((rect_start, rect_end))
        cv2.rectangle(img, rect_start, rect_end, (0, 255, 0), 2)
        cv2.imshow(window_name, img)
        print(f"Rectangle #{len(rectangles)}: {rect_start} -> {rect_end}")

# Открываем PDF файл
pdf_document = fitz.open("images/img_1.pdf")

# Убедимся, что у нас есть хотя бы одна страница
if len(pdf_document) > 0:
    page = pdf_document.load_page(0)  # Загружаем первую страницу

    # Увеличиваем разрешение
    zoom = 2  # Масштабирование в 2 раза
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    # Преобразуем Pixmap в формат, поддерживаемый OpenCV
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    
    # Преобразуем изображение в формат BGR для OpenCV
    if pix.n == 4:  # RGBA
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGRA)
    else:  # RGB
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Улучшение резкости изображения
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    img = cv2.filter2D(img, -1, kernel)

    # Изменение размера изображения для удобного просмотра
    img_resized = cv2.resize(img, (1000, 1000))
    img = img_resized.copy()

    # Отображаем изображение
    window_name = "Page 1"
    cv2.imshow(window_name, img)
    cv2.setMouseCallback(window_name, draw_rectangle)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
else:
    print("PDF файл не содержит страниц.")
