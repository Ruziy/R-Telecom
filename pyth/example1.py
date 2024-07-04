import easyocr
from PIL import Image
import pdfplumber
import mysql.connector

# Функция для извлечения текста из изображения с помощью EasyOCR
def extract_text_from_image(image_path):
    reader = easyocr.Reader(['en', 'ru'])  # Укажите языки, которые будут использоваться для OCR
    result = reader.readtext(image_path, detail=0)  # detail=0 возвращает только текст
    text = " ".join(result)
    return text

# Функция для извлечения текста из PDF с помощью pdfplumber
def extract_text_from_pdf(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Функция для добавления данных в базу данных MySQL
def insert_contract_data(contract_data):
    try:
        connection = mysql.connector.connect(
            host="MySQL-5.7",
            user="root",
            password="",
            database="documents"
        )
        cursor = connection.cursor()

        # Пример SQL-запроса для вставки данных в таблицу Contracts
        sql_insert_query = """
        INSERT INTO Contracts (contract_number, contract_date, contract_subject_id, contract_amount, contract_currency_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        contract_values = (
            contract_data['contract_number'],
            contract_data['contract_date'],
            contract_data['contract_subject_id'],
            contract_data['contract_amount'],
            contract_data['contract_currency_id']
        )
        cursor.execute(sql_insert_query, contract_values)
        connection.commit()
        print("Данные успешно добавлены в базу данных")

    except mysql.connector.Error as error:
        print(f"Ошибка при работе с базой данных: {error}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Соединение с базой данных закрыто")

# Основная функция для обработки скана договора
def process_contract_scan(scan_file):
    try:
        if scan_file.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(scan_file)
        elif scan_file.endswith('.jpg') or scan_file.endswith('.jpeg') or scan_file.endswith('.png'):
            extracted_text = extract_text_from_image(scan_file)
        else:
            print("Неподдерживаемый формат файла")
            return

        # Здесь нужно добавить логику для анализа извлеченного текста и извлечения данных о договоре
        contract_data = {
            'contract_number': 'ABC123',  # Пример данных
            'contract_date': '2024-07-01',  # Пример данных
            'contract_subject_id': 1,  # Пример данных
            'contract_amount': 10000.00,  # Пример данных
            'contract_currency_id': 1  # Пример данных
        }

        # Добавление распознанных данных в базу данных
        insert_contract_data(contract_data)

    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
# Пример использования функции для обработки скана договора
if __name__ == "__main__":
    # Укажите реальный путь к вашему файлу, используя сырую строку
    process_contract_scan(r"C:\Users\Данила\Desktop\scan\p3.pdf")  # Путь к скану договора в формате PNG