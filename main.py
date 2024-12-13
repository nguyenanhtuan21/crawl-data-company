from nextcaptcha import NextCaptchaAPI

CLIENT_KEY = "next_e8ebfdf8b770fc8d713436ea6103665f00"
WEBSITE_URL = "https://bocaodientu.dkkd.gov.vn/egazette/Forms/Egazette/ANNOUNCEMENTSListingInsUpd.aspx"
WEBSITE_KEY = "6LewYU4UAAAAAD9dQ51Cj_A_1uHLOXw9wJIxi9x0"

api = NextCaptchaAPI(client_key=CLIENT_KEY)
result = api.recaptchav2(website_url=WEBSITE_URL, website_key=WEBSITE_KEY)

if result["status"] == "ready":
    print(f"reCAPTCHA solved: {result['solution']}")
else:
    print(f"Failed to solve reCAPTCHA: {result['error']}")