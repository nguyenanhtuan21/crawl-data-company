import csv



def load_csv():
    # Đọc file CSV và lấy cột mã số thuế
    tax_codes = []
    # Thay "your_file.csv" bằng đường dẫn đến file CSV của bạn
    with open('customer_ctl.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)  # Đọc file CSV dưới dạng từ điển
        for row in csv_reader:
            # Giả sử tên cột mã số thuế là 'Mã số thuế'
            tax_codes.append(row['taxcode'])  # Thêm giá trị của cột 'Mã số thuế' vào mảng
    return tax_codes



# In ra mảng chứa các mã số thuế
print(load_csv())
