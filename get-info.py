import requests
from bs4 import BeautifulSoup

# URL của trang web
url = "https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/ANNOUNCEMENTSListingInsUpd.aspx"

# Tạo session để giữ cookie (giống như duy trì session khi duyệt web)
session = requests.Session()

# Gửi yêu cầu GET để lấy nội dung trang ban đầu (nhận các cookie và dữ liệu cần thiết)
response = session.get(url, verify=False)
response.raise_for_status()  # Kiểm tra lỗi HTTP

# Phân tích nội dung HTML bằng BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# print(response.text)    # In nội dung trả về từ GET

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
    "ctl00$C$ENT_GDT_CODEFld": "3603992896",# soup.find("input", {"name": "ctl00$C$ENT_GDT_CODEFld"})["value"] if soup.find("input", {"name": "ctl00$C$ENT_GDT_CODEFld"}) else "",
    "ctl00$C$HO_PROVINCE_IDFld": soup.find("select", {"name": "ctl00$C$HO_PROVINCE_IDFld"}).find("option", selected=True)["value"] if soup.find("select", {"name": "ctl00$C$HO_PROVINCE_IDFld"}) else "",
    "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld": soup.find("select", {"name": "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld"}).find("option", selected=True)["value"] if soup.find("select", {"name": "ctl00$C$ANNOUNCEMENT_TYPE_IDFilterFld"}) else "",
    "g-recaptcha-response": "03AFcWeA7QqLd7KuGR5CNPJE6d2HIFw8Fdg3TSL2iNTGuZ-i52oGRPd13JXX4PIzuFZDeqW1TSgASwoKk-R__4r-Q-ldGPGpgYSYhiMKxxkwka29wPZ2NdEMM6FYvcKXjpro2PZ-OT7T7GpWMh3xGZfF2immsfydyieL8ftKwdpV1ZTO9Zv1edGbhDVUv1ejQruTeuHpScFrfJZOi8ZCLi3xuXi1_-BGskPHVgEUt3ItV67Dinlag05zaOXgO2gl-3fqO34JT4b-pv5LbYlceI-WOVZT6LRWbKZY-xkzBAZC9dxgNo5hh9IR35cW2GSbFbgLuHFBbjr94BsdXG0DAt6E1iI7oztmu4o_GcT7M6zZxkM5CoQQHyqep1SPLVOw-crd6ps7fw4nsZ5QIkwR1s5VKk1PiebNQkPGzHrggo_IYAU8Av_a16zqw5fSzkLP0O6rQozlaSLOoKQkVDKgniKhQ2qy02Z_Q8Vpa_WHBZLajmStMJOFjf4Pk1nB5C2RH2asNRfDaB3TEouCo2H_mdYsvxhKYa--tCUakmi_5N8483-Yfu3acrprZ1c7mjtqTpd9lBStyDLMfNfpUX_IzuqenO7Z0YJOj7OPxu6sKYqHZhc4klMEOb1PiPS2VAjOYp8JOizD1712EYWUTx_SI3tb0NlYRabeRZc2ZJ7tv3x76dkxUA5GjMY-VLSXVhJDC6HMNHtx8iICiP-D_UNZAtlRHwySdPi97T-3EFFZsIhdLtiqMlQwxJfhJWyLp9G1tuz2vk3S4hqqVYIuEvEtQUFS3akD2DjMMRDp8ND7AiVXSi2DZsOsJuKM5ZBnxVQp0PvY7RHmDoRMWvk9_9ia8GPaTwJUxkHaGylG-NkQV4pS6KmDWkdKL9ak5Lrq67KpGq6VkK_GBDvGNFpJyQfpd0i3nDFW6fA9JUbvPA3Aoj8j4gxuRpVzxIMNgm69ccbXQLjsTxcRZbf0FFRAF0Odob-c0zmo_i7U3Mw4Y8efl8KwcaZbww4aGDNxI",  # Captcha cần xử lý riêng
    "ctl00$C$BtnFilter": "Tìm kiếm"
}

# Gửi yêu cầu POST với payload đã được điền vào
response_post = session.post(url, data=payload, verify=False)

# Kiểm tra và in kết quả
response_post.raise_for_status()  # Kiểm tra lỗi HTTP
print(response_post.text)  # In nội dung trả về từ POST

# Bạn có thể phân tích lại nội dung trả về nếu cần trích xuất dữ liệu

#print(payload)  # In payload để kiểm tra