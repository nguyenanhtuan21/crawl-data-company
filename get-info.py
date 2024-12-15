import requests
from bs4 import BeautifulSoup
import os
import random
import urllib.parse
from nextcaptcha import NextCaptchaAPI
import csv
import time
import logging
# Configure logging
logging.basicConfig(
    filename='log.txt',
    filemode='a',  # Append mode
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

CLIENT_KEY = "next_e8ebfdf8b770fc8d713436ea6103665f00"
WEBSITE_URL = "https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/ANNOUNCEMENTSListingInsUpd.aspx"
WEBSITE_KEY = "6LewYU4UAAAAAD9dQ51Cj_A_1uHLOXw9wJIxi9x0"

api = NextCaptchaAPI(client_key=CLIENT_KEY)


def create_captcha_resolve():
    result = api.recaptchav2(website_url=WEBSITE_URL, website_key=WEBSITE_KEY)
    return result["solution"].get('gRecaptchaResponse')


def load_csv():
    # Đọc file CSV và lấy cột mã số thuế
    tax_codes = []
    # Thay "your_file.csv" bằng đường dẫn đến file CSV của bạn
    with open('customer_ctl.csv', mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)  # Đọc file CSV dưới dạng từ điển
        for row in csv_reader:
            # Giả sử tên cột mã số thuế là 'Mã số thuế'
            tax_codes.append(row['taxcode'])  # Thêm giá trị của cột 'Mã số thuế' vào mảng
            if len(tax_codes) > 50:
                break
    return tax_codes

def get_pdf_file(taxcode):
    logger.info(f"Starting get_pdf_file for {taxcode}")
    # URL của trang web
    url = "https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/ANNOUNCEMENTSListingInsUpd.aspx"
    # Tạo session để giữ cookie (giống như duy trì session khi duyệt web)
    session = requests.Session()
    # Gửi yêu cầu GET để lấy nội dung trang ban đầu (nhận các cookie và dữ liệu cần thiết)
    response = session.get(url, verify=False)
    response.raise_for_status()  # Kiểm tra lỗi HTTP
    # Phân tích nội dung HTML bằng BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")
    # Tìm các trường cần thiết trong payload
    payload = {
        "__EVENTTARGET": soup.find("input", {"name": "__EVENTTARGET"})["value"] if soup.find("input", {"name": "__EVENTTARGET"}) else "",
        "__EVENTARGUMENT": soup.find("input", {"name": "__EVENTARGUMENT"})["value"] if soup.find("input", {"name": "__EVENTARGUMENT"}) else "",
        "__LASTFOCUS": soup.find("input", {"name": "__LASTFOCUS"})["value"] if soup.find("input", {"name": "__LASTFOCUS"}) else "",
        "__VIEWSTATE": soup.find("input", {"name": "__VIEWSTATE"})["value"] if soup.find("input", {"name": "__VIEWSTATE"}) else "",
        "__EVENTVALIDATION": soup.find("input", {"name": "__EVENTVALIDATION"})["value"] if soup.find("input", {"name": "__EVENTVALIDATION"}) else "",
        "ctl00$nonceKeyFld": "5ac9b54e-8b51-4671-ba76-b61aafa64187" ,#soup.find("input", {"name": "ctl00$nonceKeyFld"})["value"] if soup.find("input", {"name": "ctl00$nonceKeyFld"}) else "",
        "ctl00$hdParameter": soup.find("input", {"name": "ctl00$hdParameter"})["value"] if soup.find("input", {"name": "ctl00$hdParameter"}) else "",
        "ctl00$FldSearch": "",#soup.find("input", {"name": "ctl00$FldSearch"})["value"] if soup.find("input", {"name": "ctl00$FldSearch"}) else "",
        "ctl00$FldSearchID": "",# soup.find("input", {"name": "ctl00$FldSearchID"})["value"] if soup.find("input", {"name": "ctl00$FldSearchID"}) else "",
        "ctl00$searchtype": soup.find("input", {"name": "ctl00$searchtype"})["value"] if soup.find("input", {"name": "ctl00$searchtype"}) else "",
        "ctl00$C$PUBLISH_DATEFilterFldFrom": "",# soup.find("input", {"name": "ctl00$C$PUBLISH_DATEFilterFldFrom"})["value"] if soup.find("input", {"name": "ctl00$C$PUBLISH_DATEFilterFldFrom"}) else "",
        "ctl00$C$PUBLISH_DATEFilterFldTo": "",# soup.find("input", {"name": "ctl00$C$PUBLISH_DATEFilterFldTo"})["value"] if soup.find("input", {"name": "ctl00$C$PUBLISH_DATEFilterFldTo"}) else "",
        "ctl00$C$ENT_CODEFilterFld": "",# soup.find("input", {"name": "ctl00$C$ENT_CODEFilterFld"})["value"] if soup.find("input", {"name": "ctl00$C$ENT_CODEFilterFld"}) else "",
        "ctl00$C$ENT_GDT_CODEFld": taxcode,# soup.find("input", {"name": "ctl00$C$ENT_GDT_CODEFld"})["value"] if soup.find("input", {"name": "ctl00$C$ENT_GDT_CODEFld"}) else "",
        "ctl00$C$HO_PROVINCE_IDFld": soup.find("select", {"name": "ctl00$C$HO_PROVINCE_IDFld"}).find("option", selected=True)["value"] if soup.find("select", {"name": "ctl00$C$HO_PROVINCE_IDFld"}) else "",
        "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld": soup.find("select", {"name": "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld"}).find("option", selected=True)["value"] if soup.find("select", {"name": "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld"}) else "",
        "g-recaptcha-response": create_captcha_resolve(),  # Captcha cần xử lý riêng
        "ctl00$C$BtnFilter": "Tìm kiếm"
    }

    # Gửi yêu cầu POST với payload đã được điền vào
    response_post = session.post(url, data=payload, verify=False)

    # Kiểm tra và in kết quả
    response_post.raise_for_status()  # Kiểm tra lỗi HTTP
    # print(response_post.text)  # In nội dung trả về từ POST

    # Bạn có thể phân tích lại nội dung trả về nếu cần trích xuất dữ liệu
    # request thứ 2 để download file
    soup2 = BeautifulSoup(response_post.text, "html.parser")

    payload_temp = {
        "__EVENTTARGET": soup2.find("input", {"name": "__EVENTTARGET"})["value"] if soup2.find("input", {"name": "__EVENTTARGET"}) else "",
        "__EVENTARGUMENT": soup2.find("input", {"name": "__EVENTARGUMENT"})["value"] if soup2.find("input", {"name": "__EVENTARGUMENT"}) else "",
        "__LASTFOCUS": soup2.find("input", {"name": "__LASTFOCUS"})["value"] if soup2.find("input", {"name": "__LASTFOCUS"}) else "",
        "__VIEWSTATE": soup2.find("input", {"name": "__VIEWSTATE"})["value"] if soup2.find("input", {"name": "__VIEWSTATE"}) else "",
        "__EVENTVALIDATION": soup2.find("input", {"name": "__EVENTVALIDATION"})["value"] if soup2.find("input", {"name": "__EVENTVALIDATION"}) else "",
        "ctl00$nonceKeyFld": soup2.find("input", {"name": "ctl00$nonceKeyFld"})["value"] if soup2.find("input", {"name": "ctl00$nonceKeyFld"}) else "",
        "ctl00$hdParameter": soup2.find("input", {"name": "ctl00$hdParameter"})["value"] if soup2.find("input", {"name": "ctl00$hdParameter"}) else "",
        "ctl00$FldSearch": "",
        "ctl00$FldSearchID": "",
        "ctl00$searchtype": soup2.find("input", {"name": "ctl00$searchtype"})["value"] if soup2.find("input", {"name": "ctl00$searchtype"}) else "",
        "ctl00$C$PUBLISH_DATEFilterFldFrom": "",
        "ctl00$C$PUBLISH_DATEFilterFldTo": "",
        "ctl00$C$PUBLISH_DATEFilterFld": "",
        "ctl00$C$ENT_CODEFilterFld": "",
        "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld": "NEW",
        "ctl00$C$ENT_GDT_CODEFld": taxcode,
        "ctl00$C$HO_PROVINCE_IDFld": "",
        "ctl00$C$ENT_NAMEFilterFld": "",
        "ctl00$C$WebTextBox1": "",
        "g-recaptcha-response": "",
        "ctl00$C$CtlList$ctl02$LnkGetPDFActive.x": random.randint(1, 31),
        "ctl00$C$CtlList$ctl02$LnkGetPDFActive.y": random.randint(1, 31)
    }
    header2 = {
        "Content-Type": "application/x-www-form-urlencoded", 
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response_post_download = session.post(url, data=urllib.parse.urlencode(payload_temp), headers=header2, verify=False)

    response_post_download.raise_for_status()  # Kiểm tra lỗi HTTP

    #print(response_post_download.text)  # In nội dung trả về từ POST


    # Lưu file PDF vào thư mục data
    if response_post_download.status_code == 200:
        # Tạo thư mục 'data' nếu chưa có
        if not os.path.exists('data'):
            os.makedirs('data')

        # Lưu file PDF
        file_path = f'data/{taxcode}.pdf'
        with open(file_path, 'wb') as f:
            f.write(response_post_download.content)

        print(f"File đã được lưu tại: {file_path}")
        logger.info(f"PDF file saved successfully for {taxcode}")
    else:
        print(f"Không thể tải file, mã lỗi: {response_post_download.status_code}")
        

if __name__ == "__main__":
    pass
    tax_codes = load_csv()
    for tax_code in tax_codes:
        get_pdf_file(tax_code)
        time.sleep(3)