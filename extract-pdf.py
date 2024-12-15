import csv
from PyPDF2 import PdfReader
import re

# Đường dẫn đến file PDF
pdf_file = "data/output.pdf"  # Đổi thành file PDF của bạn
csv_file = "business_info_extracted.csv"  # File CSV đầu ra

# Đọc nội dung file PDF
reader = PdfReader(pdf_file)
text = ""
for page in reader.pages:
    text += page.extract_text()

# Trích xuất thông tin từ nội dung PDF
data = {
    "Tên công ty viết bằng tiếng Việt": re.search(r"Tên công ty.*?\n(.*)", text, re.IGNORECASE),
    "Tên công ty viết bằng tiếng nước ngoài": re.search(r"Tên tiếng nước ngoài.*?\n(.*)", text, re.IGNORECASE),
    "Tên công ty viết tắt": re.search(r"Tên viết tắt.*?\n(.*)", text, re.IGNORECASE),
    "Mã số doanh nghiệp": re.search(r"Mã số doanh nghiệp.*?(\d+)", text),
    "Địa chỉ trụ sở chính": re.search(r"Địa chỉ trụ sở chính.*?\n(.*)", text, re.IGNORECASE),
    "Ngày thành lập": re.search(r"Ngày thành lập.*?(\d{2}/\d{2}/\d{4})", text),
    "Vốn điều lệ": re.search(r"Vốn điều lệ.*?\n(.*)", text, re.IGNORECASE),
    "Số điện thoại": re.search(r"Điện thoại.*?(\d{10,11})", text),
    "Email": re.search(r"Email.*?([\w.-]+@[\w.-]+)", text),
    "Ngành, nghề kinh doanh": re.findall(r"(\d+)\s-\s(.*)", text),
    "Người đại diện": {
        "Họ và tên": re.search(r"Họ và tên người đại diện.*?\n(.*)", text, re.IGNORECASE),
        "Giới tính": re.search(r"Giới tính.*?(Nam|Nữ)", text, re.IGNORECASE),
        "Ngày sinh": re.search(r"Ngày sinh.*?(\d{2}/\d{2}/\d{4})", text),
        "Dân tộc": re.search(r"Dân tộc.*?\n(.*)", text, re.IGNORECASE),
        "Quốc tịch": re.search(r"Quốc tịch.*?\n(.*)", text, re.IGNORECASE),
        "Loại giấy tờ pháp lý": re.search(r"Loại giấy tờ pháp lý.*?\n(.*)", text, re.IGNORECASE),
        "Số giấy tờ pháp lý": re.search(r"Số giấy tờ pháp lý.*?(\d+)", text),
        "Ngày cấp": re.search(r"Ngày cấp.*?(\d{2}/\d{2}/\d{4})", text),
        "Nơi cấp": re.search(r"Nơi cấp.*?\n(.*)", text, re.IGNORECASE),
        "Địa chỉ thường trú": re.search(r"Địa chỉ thường trú.*?\n(.*)", text, re.IGNORECASE),
        "Địa chỉ liên lạc": re.search(r"Địa chỉ liên lạc.*?\n(.*)", text, re.IGNORECASE),
    },
    "Nơi đăng ký": re.search(r"Nơi đăng ký.*?\n(.*)", text, re.IGNORECASE),
    "Thời gian đăng": re.search(r"Thời gian đăng.*?\n(.*)", text, re.IGNORECASE)
}

# Làm sạch kết quả (lấy group 1 nếu có)
for key, value in data.items():
    if isinstance(value, re.Match):
        data[key] = value.group(1).strip()
    elif isinstance(value, list):  # Với danh sách ngành nghề
        data[key] = [{"Mã ngành": i[0], "Tên ngành": i[1]} for i in value]
    elif isinstance(value, dict):  # Với thông tin người đại diện
        for sub_key, sub_value in value.items():
            if isinstance(sub_value, re.Match):
                data[key][sub_key] = sub_value.group(1).strip()
            else:
                data[key][sub_key] = ""

# Ghi dữ liệu vào file CSV
with open(csv_file, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    
    # Ghi thông tin chung
    writer.writerow(["Thông tin", "Chi tiết"])
    for key in ["Tên công ty viết bằng tiếng Việt", "Tên công ty viết bằng tiếng nước ngoài", "Tên công ty viết tắt", 
                "Mã số doanh nghiệp", "Địa chỉ trụ sở chính", "Ngày thành lập", "Vốn điều lệ", "Số điện thoại", "Email"]:
        writer.writerow([key, data.get(key, "")])
    
    # Ghi ngành nghề kinh doanh
    writer.writerow(["Ngành, nghề kinh doanh", ""])
    writer.writerow(["Mã ngành", "Tên ngành"])
    for industry in data["Ngành, nghề kinh doanh"]:
        writer.writerow([industry["Mã ngành"], industry["Tên ngành"]])
    
    # Ghi thông tin người đại diện
    writer.writerow(["Người đại diện", ""])
    for sub_key, sub_value in data["Người đại diện"].items():
        writer.writerow([sub_key, sub_value])
    
    # Ghi nơi đăng ký và thời gian đăng
    writer.writerow(["Nơi đăng ký", data["Nơi đăng ký"]])
    writer.writerow(["Thời gian đăng", data["Thời gian đăng"]])

print(f"Dữ liệu đã được lưu vào file '{csv_file}'")
