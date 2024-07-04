import pdfplumber
import mysql.connector
import re

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

        # SQL-запрос для вставки данных в таблицу Contracts
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

# Основная функция для обработки скана договора в PDF
def process_contract_pdf(pdf_file):
    try:
        extracted_text = extract_text_from_pdf(pdf_file)
        
        print("Извлеченный текст из PDF:")
        print(extracted_text)

        # Логика для анализа извлеченного текста и извлечения данных о договоре
        contract_data = {
            'contract_number': extract_contract_number(extracted_text) or "Unknown",
            'contract_date': extract_contract_date(extracted_text) or "2024-01-01",
            'contract_subject_id': extract_contract_subject_id(extracted_text) or 1,
            'contract_amount': extract_contract_amount(extracted_text) or 0.0,
            'contract_currency_id': extract_contract_currency_id(extracted_text) or 1
        }

        print("Извлеченные данные:")
        print(contract_data)

        # Добавление распознанных данных в базу данных
        insert_contract_data(contract_data)

    except FileNotFoundError as e:
        print(f"Файл не найден: {e}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

def extract_contract_number(text):
    # Пример извлечения номера договора из текста
    match = re.search(r'Номер договора:\s*(\w+)', text)
    if match:
        return match.group(1)
    else:
        return None

def extract_contract_date(text):
    # Пример извлечения даты договора из текста
    match = re.search(r'Дата договора:\s*(\d{4}-\d{2}-\d{2})', text)
    if match:
        return match.group(1)
    else:
        return None

def extract_contract_amount(text):
    # Пример извлечения суммы договора из текста
    match = re.search(r'Сумма договора:\s*(\d+\.\d+)', text)
    if match:
        return float(match.group(1))
    else:
        return None

def extract_contract_subject_id(text):
    # Пример извлечения идентификатора предмета договора из текста
    # Например, можно использовать ключевые слова или анализ структурированных данных
    # Здесь приведен заглушечный пример
    if 'Предмет договора: услуги по...' in text:
        return 1  # Пример идентификатора
    else:
        return None

def extract_contract_currency_id(text):
    # Пример извлечения идентификатора валюты из текста
    # Например, можно использовать ключевые слова или анализ структурированных данных
    # Здесь приведен заглушечный пример
    if 'Валюта договора: USD' in text:
        return 1  # Пример идентификатора
    else:
        return None

# Пример использования функции для обработки скана договора в PDF
if __name__ == "__main__":
    # Укажите реальный путь к вашему PDF-файлу, используя сырую строку
    process_contract_pdf(r"C:\Users\Данила\Desktop\scan\example_contract.pdf")  # Путь к скану договора в формате PDF
