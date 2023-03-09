import logging
from reportlab.pdfgen import canvas
from reportlab.lib import units

logger = logging.getLogger(__name__)

def generate_pdf_receipt(
    filename: str,
    company_name: str,
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
    descriptions: dict
):
    total = 0

    # 創建一個PDF檔案
    pdf_file = canvas.Canvas(f"{filename}.pdf")

    # 設置字型
    pdf_file.setFont(font, 16)

    # 寫入收據信息
    weight = 750
    logger.info(f"公司名稱 weight: {weight}")
    pdf_file.drawString(50, weight, company_name)
    pdf_file.setFont(font, 12)
    pdf_file.drawString(400, weight, "收据编号: {}".format(receipt_number))

    weight -= 15
    logger.info(f"公司地址 weight: {weight}")
    pdf_file.drawString(50, weight, company_address)
    pdf_file.drawString(400, weight, "日期: {}".format(receipt_date))

    weight -= 15
    logger.info(f"公司電話 weight: {weight}")
    pdf_file.drawString(50, weight, company_phone)

    weight -= 20
    logger.info(f"客戶名稱 weight: {weight}")
    pdf_file.drawString(50, weight, f"名称: {client_name}")
    pdf_file.drawString(400, weight, f"会员编号: {client_num}")

    weight -= 10
    logger.info(f"線1 weight: {weight}")
    pdf_file.line(50, weight, 550, weight)

    # 寫入費用信息
    weight -= 20
    logger.info(f"內容 weight: {weight}")
    pdf_file.drawString(50, weight, "内容")
    pdf_file.drawString(250, weight, "价格")
    pdf_file.drawString(350, weight, "税")

    weight -= 10
    logger.info(f"線2 weight: {weight}")
    pdf_file.line(50, weight, 550, weight)
    weight -= 20
    logger.info(f"第1筆 weight: {weight}")
    for i, (_, descrip) in enumerate(descriptions.items()):
        description = descrip["description"]
        price = descrip["price"]
        tax = descrip["tax"]
        pdf_file.drawString(50, weight, description)
        pdf_file.drawString(250, weight, f"{price:,.2f}")
        pdf_file.drawString(350, weight, f"{tax:,.0%}")
        total += price + price * tax

        weight -= 20
        if i == len(descriptions) - 1:
            logger.info(f"第{i+2}筆 weight: {weight}")
        else:
            logger.info(f"線3 weight: {weight}")

    pdf_file.line(50, weight, 550, weight)
    weight -= 20
    logger.info(f"總計 weight: {weight}")
    pdf_file.drawString(50, weight, "总计: ")
    pdf_file.drawString(250, weight, f"{total:,.2f}")

    # 设定浮水印
    pdf_file.rotate(angle)
    # 设置透明度
    pdf_file.setFillAlpha(0.4)
    pdf_file.drawImage(images, 9 * units.cm, 23 * units.cm, 3 * units.cm, 3 * units.cm)

    # 完成並關閉PDF檔案
    pdf_file.showPage()
    pdf_file.save()
