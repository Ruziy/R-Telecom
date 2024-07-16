import fitz  # PyMuPDF
import cv2
import numpy as np
import easyocr
from stamp import detect_and_draw_stamps
import matplotlib.pyplot as plt
import mysql.connector

# Database connection
db_connection = mysql.connector.connect(
    host="MySQL-5.7",
    user="root",
    password="",
    database="pdf_data"
)
cursor = db_connection.cursor()

# Список координат рамок
rectangles = [
    ((673, 27), (744, 54)), # номер документа
    ((661, 70), (956, 94)), # дата договора
    ((159, 96), (680, 114)), # первая сторона
    ((160, 186), (734, 204)), # вторая сторона
    ((478, 491), (799, 508)), # сумма
    ((157, 149), (944, 167)), # первые реквизиты
    ((154, 239), (949, 257))  # вторые реквизиты
]
tags = ["номер документа", "дата договора", "первая сторона", "вторая сторона", "сумма", "первые реквизиты", "вторые реквизиты"]

# Открываем PDF файл
pdf_document = fitz.open(r"C:\Users\Данила\Desktop\1\model\images\img_2_with_stamp.pdf")

# Убедимся, что у нас есть хотя бы одна страница
if len(pdf_document) > 0:
    page = pdf_document.load_page(0)  # Загружаем первую страницу

    # Увеличиваем разрешение
    zoom = 2  # Масштабирование в 2 раза
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)

    # Преобразуем Pixmap в формат, поддерживаемый OpenCV
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    res_stamp = detect_and_draw_stamps(img)

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

    # Инициализация easyocr Reader
    reader = easyocr.Reader(['ru', 'en'])  # Используем русский и английский языки для распознавания

    extracted_data = [None] * len(tags)  # Инициализируем список нужной длины

    # Отрисовка всех рамок с номерами
    for i, (start, end) in enumerate(rectangles):
        cv2.rectangle(img, start, end, (0, 255, 0), 2)
        cv2.putText(img, f'#{i+1}', (start[0], start[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Извлекаем текст из текущей рамки
        x1, y1 = start
        x2, y2 = end
        sub_img = img[y1:y2, x1:x2]

        # Распознаем текст с помощью easyocr
        result = reader.readtext(sub_img)

        # Проверяем, есть ли распознанный текст
        if result:
            # Выводим распознанный текст в консоль
            print(f"Результаты распознавания для рамки тега: {tags[i]}:")
            for res in result:
                if tags[i] == "сумма":
                    # Выводим только строку до первого пробела
                    first_word = res[1].split(' ')[0]
                    print(first_word)
                    extracted_data[i] = first_word
                else:
                    # Выводим весь результат
                    print(res[1])
                    extracted_data[i] = res[1]
        else:
            # Если текст не распознан, выводим None
            print(f"Результаты распознавания для рамки тега: {tags[i]}: None")
            extracted_data[i] = None

    # Отображаем изображение с рамками
    print("Наличие печатей: ", res_stamp)

    # Отображаем изображение с использованием matplotlib
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    # Debugging: print the extracted data and length
    print("Extracted data:", extracted_data)
    print("Length of extracted data:", len(extracted_data))

    # Insert data into database
    insert_query = """
    INSERT INTO extracted_data (document_number, contract_date, first_party, second_party, amount, first_details, second_details, stamps_present)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_query, (*extracted_data, res_stamp))
    db_connection.commit()

else:
    print("PDF файл не содержит страниц.")

# Close the database connection
cursor.close()
db_connection.close()
