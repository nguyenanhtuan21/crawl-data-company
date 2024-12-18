import os
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
import re
import csv
import logging

# Cấu hình đường dẫn tới tesseract (nếu sử dụng Windows)
# Chỉ cần bỏ dòng dưới nếu bạn đang dùng Linux hoặc macOS
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

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

# Tìm tên công ty viết bằng tiếng Việt (hỗ trợ tên công ty trên nhiều dòng)
def find_company_name_vietnamese(content):
    # Tìm tên công ty có thể bị chia thành nhiều dòng
    match = re.search(r"Tên công ty viết bằng tiếng Việt[:\s]*(CÔNG TY [\w\s]+(?:\n[\w\s]+)*)", content)
    if match:
        # Xóa bỏ các ký tự xuống dòng (nếu có) và gộp tên công ty lại thành một chuỗi
        company_name = match.group(1).replace("\n", " ").strip()
        return company_name
    return "No information"

# Tìm Email
def find_email(content):
    match = re.search(r"Email[:\s]*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", content)
    return match.group(1) if match else "No information"

# Tìm số điện thoại
def find_phone(content):
    match = re.search(r"Điện thoại[:\s]*([\d\+]+)", content)
    return match.group(1) if match else "No information"

# Hàm xử lý tất cả các file PDF trong thư mục
def process_pdfs_in_directory(directory_path):
    result_data = []
    
    # Kiểm tra xem thư mục có chứa file PDF không
    if not os.path.exists(directory_path) or len(os.listdir(directory_path)) == 0:
        print("Directory is empty or path is incorrect!")
        return
    
    for filename in os.listdir(directory_path):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory_path, filename)
            # Lấy Mã số doanh nghiệp là tên file (không bao gồm phần mở rộng)
            business_code = os.path.splitext(filename)[0]
            print(f"Processing file: {filename}")
            try:
                content = extract_pdf_content(pdf_path)
                company_name_vn = find_company_name_vietnamese(content)
                email = find_email(content)
                phone = find_phone(content)
                
                # Thêm kết quả vào danh sách
                result_data.append({
                    'Mã số doanh nghiệp': business_code,
                    'Tên công ty viết bằng tiếng Việt': company_name_vn,
                    'Email': email,
                    'Điện thoại': phone
                })
                print(f"Data extracted: {company_name_vn}, {email}, {phone}")
                logging.info(f"Data extracted: {company_name_vn}, {email}, {phone}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")
                logging.error(f"Error processing {filename}: {e}")
    
    # Kiểm tra nếu có dữ liệu để lưu vào CSV
    if result_data:
        # Ghi kết quả vào file CSV bằng thư viện csv
        csv_file = 'outputfile_2.csv'
        with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=['Mã số doanh nghiệp', 'Tên công ty viết bằng tiếng Việt', 'Email', 'Điện thoại'])
            writer.writeheader()  # Ghi header vào file CSV
            writer.writerows(result_data)  # Ghi các dữ liệu vào file
        print(f"Extraction complete. Data saved to '{csv_file}'.")
    else:
        print("No data extracted.")

# Đường dẫn tới thư mục chứa các file PDF
directory_path = '/Users/tuannguyenanh/code/crawl-data-company/data/'  # Thay thế bằng đường dẫn tới thư mục chứa các file PDF của bạn

# Xử lý tất cả các file PDF trong thư mục
process_pdfs_in_directory(directory_path)
