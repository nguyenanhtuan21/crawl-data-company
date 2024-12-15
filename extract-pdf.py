from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re

# Cấu hình đường dẫn tới tesseract (nếu sử dụng Windows)
# Chỉ cần bỏ dòng dưới nếu bạn đang dùng Linux hoặc macOS
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Đường dẫn tới tesseract.exe trên Windows

# Chuyển PDF thành hình ảnh
def pdf_to_image(pdf_path):
    images = convert_from_path(pdf_path)
    return images

# Áp dụng OCR để trích xuất văn bản từ hình ảnh
def ocr_from_image(images):
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img, lang='vie')  # Sử dụng ngôn ngữ tiếng Việt nếu có
    return text

# Đọc file PDF và trích xuất văn bản
def extract_pdf_content(pdf_path):
    images = pdf_to_image(pdf_path)
    text = ocr_from_image(images)
    return text

# Tìm Mã số doanh nghiệp
def find_business_code(content):
    match = re.search(r"Mã số doanh nghiệp[:\s]*([\d]+)", content)
    return match.group(1) if match else "No information"

# Tìm tên công ty viết bằng tiếng Việt
def find_company_name_vietnamese(content):
    match = re.search(r"Tên công ty viết bằng tiếng Việt[:\s]*(CÔNG TY [\w\s]+)", content)
    return match.group(1) if match else "No information"

# Tìm Email
def find_email(content):
    match = re.search(r"Email[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", content)
    return match.group(1) if match else "No information"

# Tìm số điện thoại
def find_phone(content):
    match = re.search(r"Điện thoại[:\s]*([\d\+]+)", content)
    return match.group(1) if match else "No information"


# Đường dẫn đến file PDF
pdf_file = 'data/0110632065.pdf'  # Thay thế bằng đường dẫn tới file PDF của bạn

# Trích xuất nội dung và in ra
content = extract_pdf_content(pdf_file)
business_code = find_business_code(content)
company_name_vn = find_company_name_vietnamese(content)
email = find_email(content)
phone = find_phone(content)

# print(content)

print(f"Mã số doanh nghiệp: {business_code}")
print(f"Tên công ty viết bằng tiếng Việt: {company_name_vn}")
print(f"Email: {email}")
print(f"Điện thoại: {phone}")
