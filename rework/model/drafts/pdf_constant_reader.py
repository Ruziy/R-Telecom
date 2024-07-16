import fitz  # PyMuPDF
import cv2
import numpy as np

# Список координат рамок
rectangles = [
    ((673, 27), (744, 54)), #номер документа
    ((661, 70), (956, 94)), #дата договора
    ((159, 96), (680, 114)), #первая сторона
    ((160, 186), (734, 204)), #вторая сторона
    ((478, 491), (799, 508)), #сумма
    ((157, 149),(944, 167)), #первые реквизиты
    ((154, 239),(949, 257)) #первые реквизиты
]
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

    # Отрисовка всех рамок с номерами
    for i, (start, end) in enumerate(rectangles):
        cv2.rectangle(img, start, end, (0, 255, 0), 2)
        cv2.putText(img, f'#{i+1}', (start[0], start[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Отображаем изображение
    window_name = "Page 1"
    cv2.imshow(window_name, img)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
else:
    print("PDF файл не содержит страниц.")
