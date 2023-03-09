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
images = "log.png"  # 圖片名稱

# 設置收據信息
client_name = "小明先生"
client_num = "A12345"
company_name = "全球针灸紧急救援传统与辅助医学学会"
company_address = "1234 Main St, Anytown, USA"
company_phone = "(555) 555-5555"
receipt_number = "001-002-0001234"
receipt_date = "2023-03-06"
filename = "receipt"

# 設置費用信息
descriptions = {
    "1": {"description": "服務費", "price": 1000.00, "tax": 0.05},
    "2": {"description": "會費", "price": 200.00, "tax": 0.05},
}

logger.info("Prepare to generate pdf receipt")
func.generate_pdf_receipt(
    filename,
    company_name,
    company_address,
    company_phone,
    receipt_number,
    receipt_date,
    angle,
    images,
    font,
    client_name, 
    client_num,
    logger,
    descriptions
)