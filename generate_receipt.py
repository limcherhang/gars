import logging
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

font = "simsun"

# 設置中文字型
pdfmetrics.registerFont(TTFont("simsun", "simsun.ttf"))

# 參數
angle = 0  # 旋轉角度
images = "logo.png"  # 圖片名稱

# 設置收據信息
company_name = "全球针灸紧急救援传统与辅助医学学会"
company_english_name = "GLOBAL ACUPUNCTURE RESCUE TRADITIONAL AND COMPLEMENTARY MEDICAL SOCIETY (GARS)"
company_malay_name = "PERSATUAN PERUBATAN TRADISIONAL DAN KOMPLEMENTARI (PT&K) PENYELAMAT AKUPUNKTUR GLOBAL"
company_address = ["NO. DAFTAR: PPM-022-07-06072022", "2A, Jalan Indah, Taman Bukit Indah", "14000 Bukit Mertajam", "PULAU PINANG"]
company_phone = "017-326 9318/016-521 0420"
receipt_number = "0149"
receipt_date = "2023-03-06"
filename = "receipt"

# 設置費用信息
infos = {"client_name": "林小明", "client_eng_name": "Lim Xiao Ming", "receipt_date": receipt_date, "prices": 1000, "membertype": "永久會員 Life Member - RM1000", "cash": "Yes"}

logger.info("Prepare to generate pdf receipt")
func.generate_pdf_receipt(
    company_name,
    company_english_name,
    company_malay_name,
    company_address,
    company_phone,
    receipt_number,
    images,
    font,
    logger,
    infos
)