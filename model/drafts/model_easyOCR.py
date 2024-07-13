import cv2
import easyocr

# Функция для загрузки и предварительной обработки изображения
def load_and_preprocess_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Не удалось загрузить изображение по пути: {image_path}")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Применяем бинаризацию для улучшения контраста текста
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    return binary

# Функция для извлечения текста с изображения с помощью EasyOCR
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['ru'])  # Указываем, что используем только русский язык
    image = load_and_preprocess_image(image_path)
    result = reader.readtext(image)
    text = '\n'.join([entry[1] for entry in result])
    return text

# Функция для сохранения текста в файл
def save_text_to_file(text, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(text)

# Основная программа для демонстрации работы
def main():
    image_path = 'images\img_4.png'  # Укажите путь к вашему изображению
    output_file = 'texts\img_4_text_EASY.txt'  # Название файла для сохранения текста
    text = extract_text_from_image(image_path)
    save_text_to_file(text, output_file)
    print(f"Распознанный текст сохранен в файле: {output_file}")

if __name__ == "__main__":
    main()
