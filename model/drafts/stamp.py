import cv2

def detect_and_draw_stamps(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Не удалось загрузить изображение по пути: {image_path}")

    # Преобразование в оттенки серого и бинаризация
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Сортируем контуры по площади (от большего к меньшему)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    bounding_boxes = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 50 and h > 50:  # Пример фильтрации по размеру
            bounding_box = (x, y, w, h)
            overlap = False
            for (x2, y2, w2, h2) in bounding_boxes:
                # Проверка на пересечение рамок
                if not (x + w < x2 or x > x2 + w2 or y + h < y2 or y > y2 + h2):
                    overlap = True
                    break
            if not overlap:
                bounding_boxes.append(bounding_box)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Отрисовка зеленой рамки
                
                # Вывод площади над рамкой
                area = w * h
                area_text = f"{area:.2f}"

                print(area_text)
                cv2.putText(image, area_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Отображение изображения с отрисованными рамками
    image = cv2.resize(image, (600, 800))
    cv2.imshow('Stamped Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Пример использования
image_path = 'images/img_5.jpg'
detect_and_draw_stamps(image_path)
