import logging
import pandas as pd
from datetime import datetime
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import func

logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    encoding="utf-8",
    filename="generateReceipt.log",
)

font_normal = "simsun"
font_english = "arial"
font_chinese = "standard"
font = font_normal

images = "logo.png"  # 圖片名稱

# 設置中文字型
pdfmetrics.registerFont(TTFont("simsun", "simsun.ttf"))
pdfmetrics.registerFont(TTFont('arial', 'Arial.ttf'))
pdfmetrics.registerFont(TTFont('arialbold', 'Arial-Bold.ttf'))
pdfmetrics.registerFont(TTFont('arialitalic', 'Arial-Italic.ttf'))
pdfmetrics.registerFont(TTFont("standard", "standard.ttf"))

df = pd.read_excel("名單.xlsx")
df = df.where(pd.notnull(df), None)

dct = df.to_dict(orient='index')

company_name = "全球针灸紧急救援传统与辅助医学学会"
company_english_name = "GLOBAL ACUPUNCTURE RESCUE TRADITIONAL AND COMPLEMENTARY MEDICAL SOCIETY (GARS)"
company_malay_name = "PERSATUAN PERUBATAN TRADISIONAL DAN KOMPLEMENTARI (PT&K) PENYELAMAT AKUPUNKTUR GLOBAL"
company_address = ["NO. DAFTAR: PPM-022-07-06072022", "2A, Jalan Indah, Taman Bukit Indah", "14000 Bukit Mertajam", "PULAU PINANG"]
company_phone = "017-326 9318/016-521 0420"

for d  in dct.values():
    # print(d)
    receipt_date = datetime(2023, 4, 8).strftime("%d/%m/%Y")
    membertype = d.get("Member Type")

    if membertype == "永久会员 Life Member - RM1000":
        prices = 1000
        membertype = "永久会员费 Life Member Fee"
    elif membertype == "普通会员 Original Member - RM100/year":
        prices = 100
        membertype = "普通会员费 Original Member Fee"
    else:
        prices = 0

    infos = {"client_name": d["chinese_name"], "client_eng_name": d['english_name'], "receipt_date": receipt_date, "prices": prices, "membertype": membertype, "cash": "Yes", "link": d.get("google", "")}

    func.generate_pdf_receipt(
        company_name,
        company_english_name,
        company_malay_name,
        company_address,
        company_phone,
        images,
        font,
        logger,
        infos
    )