import logging
from reportlab.pdfgen import canvas
from reportlab.lib import units, utils

logger = logging.getLogger(__name__)

def generate_pdf_receipt(
    filename: str,
    company_name: str,
    company_english_name: str,
    company_address: str,
    company_phone: str,
    receipt_number: str,
    receipt_date: str,
    angle: str,
    images: str,
    font: str,
    client_name: str,
    client_num: str,
    logger: logging.Logger,
    descriptions: dict,
):
    total = 0

    # 創建一個PDF檔案
    pdf_file = canvas.Canvas(f"{filename}.pdf")

    # 設置字型
    pdf_file.setFont(font, 16)

    # 寫入收據信息
    weight = 800
    logger.info(f"公司名稱 weight: {weight}")
    pdf_file.drawString(160, weight, company_name)
    change_font(pdf_file, font, 12)
    

    weight -= 15
    change_font(pdf_file, font, 9)
    pdf_file.drawString(160, weight, company_english_name)
    change_font(pdf_file, font, 12)

    weight -= 15
    logger.info(f"公司地址 weight: {weight}")
    change_font(pdf_file, font, 9)
    for addr in company_address:
        pdf_file.drawString(160, weight, addr)
        weight -= 7
    change_font(pdf_file, font, 12)

    weight -= 15
    logger.info(f"公司電話 weight: {weight}")
    pdf_file.drawString(160, weight, company_phone)
    pdf_file.drawString(450, weight, "收据编号: {}".format(receipt_number))

    weight -= 50
    logger.info(f"客戶名稱 weight: {weight}")
    pdf_file.drawString(50, weight, f"茲收到")
    pdf_file.drawString(400, weight, "日期")

    weight -= 10
    pdf_file.drawString(50, weight, "Received From")
    pdf_file.drawString(400, weight, "Date")
    change_font(pdf_file, font, 15)
    pdf_file.drawString(150, weight, f"{client_name}")
    pdf_file.drawString(450, weight, f"{receipt_date}")
    change_font(pdf_file, font, 12)

    weight -= 10
    logger.info(f"線1 weight: {weight}")
    pdf_file.line(50, weight, 550, weight)

    # 寫入費用信息
    weight -= 20
    logger.info(f"內容 weight: {weight}")
    pdf_file.drawString(50, weight, "内容")
    pdf_file.drawString(350, weight, "价格")
    pdf_file.drawString(500, weight, "現金")

    weight -= 10
    pdf_file.drawString(50, weight, "Content")
    pdf_file.drawString(350, weight, "Price")
    pdf_file.drawString(500, weight, "Cash")

    weight -= 10
    logger.info(f"線2 weight: {weight}")
    pdf_file.line(50, weight, 550, weight)
    weight -= 20
    logger.info(f"第1筆 weight: {weight}")
    for i, (_, descrip) in enumerate(descriptions.items()):
        description = descrip["description"]
        english_description = descrip["English"]
        price = descrip["price"]
        cash = descrip["cash"]
        pdf_file.drawString(50, weight, description)
        pdf_file.drawString(50, weight-10, english_description)
        change_font(pdf_file, font, 15)
        pdf_file.drawString(350, weight-5, f"RM {price:,.2f}")
        change_font(pdf_file, font, 12)
        pdf_file.drawString(500, weight, cash)
        total += price

        weight -= 20
        if i == len(descriptions) - 1:
            logger.info(f"第{i+2}筆 weight: {weight}")
        else:
            logger.info(f"線3 weight: {weight}")
    
    pdf_file.line(50, weight, 550, weight)
    weight -= 30
    logger.info(f"總計 weight: {weight}")
    pdf_file.drawString(50, weight, "总计 ")
    pdf_file.drawString(50, weight-10, "Total ")
    change_font(pdf_file, font, 15)
    pdf_file.drawString(350, weight-5, f"RM {total:,.2f}")
    change_font(pdf_file, font, 12)


    # # 设定浮水印
    # pdf_file.rotate(angle)
    # # 设置透明度
    # pdf_file.setFillAlpha(0.4)
    # pdf_file.drawImage(images, 9 * units.cm, 23 * units.cm, 3 * units.cm, 3 * units.cm)
    logo = utils.ImageReader(images)
    pdf_file.drawImage(logo, 50, 720,width=100, height=100)

    # 完成並關閉PDF檔案
    pdf_file.showPage()
    pdf_file.save()

def change_font(pdf_file, font, size):
    return pdf_file.setFont(font, size)