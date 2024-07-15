import cv2

def get_area(contour):
    x, y, w, h = cv2.boundingRect(contour)
    area = w * h
    return area

def detect_and_draw_stamps(img,image_path=None,counter=True):
    if image_path==None:
        image = img
    else:
        image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Не удалось загрузить изображение по пути: {image_path}")

    # Преобразование в оттенки серого и бинаризация
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Сортируем контуры по площади (от большего к меньшему)
    contours = sorted(contours, key=get_area, reverse=True)
    bounding_boxes = []
    areas = []

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
                areas.append(w * h)
                if len(areas) and counter:
                    return 1
    if len(areas)==0 and counter:
        return 0
    
    if len(areas)>2:
        print(areas)
        average_area = sum(areas) / (len(areas)*2)
        print("avg",average_area)
    else:
        average_area = 0

    for (x, y, w, h) in bounding_boxes:
        area = w * h
        if area > average_area:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Отрисовка зеленой рамки
            area_text = f"{area:.2f}"
            print(area_text)
            cv2.putText(image, area_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Отображение изображения с отрисованными рамками
    image = cv2.resize(image, (600, 800))
    cv2.imshow('Stamped Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Пример использования
# image_path = 'images/img.png'
# res = detect_and_draw_stamps(image_path)
# print(res)

