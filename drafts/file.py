from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Функция для создания PDF-файла с информацией о договоре
def create_contract_pdf(file_path):
    c = canvas.Canvas(file_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # Добавляем информацию о договоре
    c.drawString(100, 750, "Договор")
    c.drawString(100, 730, "Номер договора: ABC123")
    c.drawString(100, 710, "Дата договора: 2024-07-01")
    c.drawString(100, 690, "Предмет договора: услуги по разработке ПО")
    c.drawString(100, 670, "Сумма договора: 10000.00 USD")
    c.drawString(100, 650, "Валюта договора: USD")

    c.save()

if __name__ == "__main__":
    # Укажите путь, где будет создан PDF-файл
    pdf_file_path = r"C:\Users\Данила\Desktop\scan\example_contract.pdf"
    create_contract_pdf(pdf_file_path)
    print(f"PDF-файл успешно создан: {pdf_file_path}")
