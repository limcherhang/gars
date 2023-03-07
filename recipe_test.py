from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import units

# def createwatermark():



font = "simsun"

# 設置中文字型
pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttf'))

# 設置收據信息
company_name = "全球针灸紧急救援传统与辅助医学学会"
company_address = "1234 Main St, Anytown, USA"
company_phone = "(555) 555-5555"
receipt_number = "001-002-0001234"
receipt_date = "2023-03-06"

# 設置費用信息
description = "服務費"
price = 1000.00
tax = 0.05

# 計算總費用
total = price + (price * tax)

# 創建一個PDF檔案
pdf_file = canvas.Canvas("receipt.pdf")

# 設置字型
pdf_file.setFont(font, 12)

# 寫入收據信息
pdf_file.drawString(50, 750, company_name)
pdf_file.drawString(50, 735, company_address)
pdf_file.drawString(50, 720, company_phone)
pdf_file.drawString(450, 750, "收據編號：{}".format(receipt_number))
pdf_file.drawString(450, 735, "日期：{}".format(receipt_date))
pdf_file.line(50, 710, 550, 710)

# 寫入費用信息
pdf_file.drawString(50, 680, "描述")
pdf_file.drawString(250, 680, "價格")
pdf_file.drawString(350, 680, "稅")
pdf_file.line(50, 670, 550, 670)
pdf_file.drawString(50, 650, description)
pdf_file.drawString(250, 650, "{:.2f}".format(price))
pdf_file.drawString(350, 650, "{:.0%}".format(tax))
pdf_file.line(50, 640, 550, 640)
pdf_file.drawString(50, 620, "總計：")
pdf_file.drawString(250, 620, "{:.2f}".format(total))

# 完成並關閉PDF檔案
pdf_file.showPage()
pdf_file.save()