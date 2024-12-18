import csv

# Hàm để bọc giá trị cột cuối trong dấu nháy kép
def wrap_last_column_in_quotes(input_file, output_file):
    # Mở file CSV gốc để đọc dữ liệu
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        rows = list(reader)
        
    # Bọc giá trị cột cuối trong dấu nháy kép cho mỗi dòng
    for row in rows:
        # Lấy giá trị cột cuối cùng và bọc trong dấu nháy kép
        row[-1] = f'"{row[-1]}"'
    
    # Lưu lại file CSV mới với cột cuối được bọc trong dấu nháy kép
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)

# Đường dẫn đến file CSV đầu vào và file CSV đầu ra
input_file = 'output_file.csv'  # Thay thế bằng đường dẫn tới file CSV của bạn
output_file = 'final1.csv'  # Đường dẫn đến file CSV đầu ra (với cột cuối đã bọc trong dấu nháy kép)

# Gọi hàm để bọc cột cuối trong dấu nháy kép và lưu lại file CSV
wrap_last_column_in_quotes(input_file, output_file)

print(f"File đã được xử lý và lưu tại {output_file}")
