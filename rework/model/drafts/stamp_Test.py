import cv2

def get_area(contour):
    x, y, w, h = cv2.boundingRect(contour)
    area = w * h
    return area

def size_contor(contours):
    areas = []
    counter = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        area = get_area(contour)
        if area>300:
            areas.append(area)
    for el in range(len(areas)-2): 
        diff = areas[el] - areas[el+1]
        diff_2 = areas[el+1] - areas[el+2]
        if diff<diff_2:
            counter+=1
        else:
            break
    return counter+1

def detect_and_draw_stamps(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Не удалось загрузить изображение по пути: {image_path}")

    # Преобразование в оттенки серого и бинаризация
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Поиск контуров
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=get_area, reverse=True)

    bounding_boxes = []

    counter = size_contor(contours)
    print(counter)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        
        if w > 50 and h > 50:  # Пример фильтрации по размеру
            bounding_box = (x, y, w, h)
            overlap = False
            area = get_area(contour)
            for (x2, y2, w2, h2) in bounding_boxes:
                # Проверка на пересечение рамок
                if not (x + w < x2 or x > x2 + w2 or y + h < y2 or y > y2 + h2):
                    overlap = True
                    break
            if not overlap:
                bounding_boxes.append(bounding_box)
                if(counter):
                    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Отрисовка зеленой рамки
                    # Вывод площади над рамкой 
                    area_text = f"{area:.2f}"
                    print(area_text)
                    cv2.putText(image, area_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    counter -=1
                else:
                    break

    # Отображение изображения с отрисованными рамками
    image = cv2.resize(image, (600, 800))
    cv2.imshow('Stamped Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Пример использования
image_path = 'model/images/img_2.jpg'
detect_and_draw_stamps(image_path)
