import logging
from reportlab.pdfgen import canvas
from reportlab.lib import utils, units
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

import pandas as pd

logger = logging.getLogger(__name__)

def generate_pdf_receipt(
    company_name: str,
    company_english_name: str,
    company_malay_name: str,
    company_address: str,
    company_phone: str,
    images: str,
    font: str,
    logger: logging.Logger,
    infos: dict
):
    client_name = infos["client_name"]
    client_eng_name = infos["client_eng_name"]
    receipt_date = infos["receipt_date"]
    prices = infos["prices"]
    chinese_price = arab_price_to_chinese_price(prices)
    cash = infos.get("cash")
    cheque_no = infos.get("cheque_no")
    bank_in_no = infos.get("bank_in_no")
    member_type = infos["membertype"]
    font = "simsun"
    fontbold = "arialbold"
    fontitalic = "arialitalic"

    # 創建一個PDF檔案
    pdf_file = canvas.Canvas(f"./receipt/{client_name}-入会费收据.pdf")


    # 寫入收據信息
    weight = 800
    change_font(pdf_file, fontbold, 7)
    pdf_file.drawString(160, weight, company_malay_name)
    
    weight -= 15
    change_font(pdf_file, fontitalic, 7)
    pdf_file.drawString(160, weight, company_english_name)

    weight -= 15
    change_font(pdf_file, font, 9)
    pdf_file.drawString(160, weight, company_name)
    change_font(pdf_file, font, 12)
    
    weight -= 15
    change_font(pdf_file, font, 9)
    for addr in company_address:
        pdf_file.drawString(160, weight, addr)
        weight -= 10
    
    pdf_file.drawString(400, weight, f"Tel: {company_phone}")

    weight -= 15
    pdf_file.drawString(400, weight, "Email: garsmy07@gmail.com")

    weight -= 15
    pdf_file.drawString(400, weight, f"Website: www.garsmy.org")

    change_font(pdf_file, font, 12)

    weight -= 50
    change_font(pdf_file, font, 20)
    pdf_file.drawString(450, weight, "Receipt")
    change_font(pdf_file, font, 12)

    weight -= 20
    try:
        receipt_df = pd.read_excel("收據明細.xlsx")
        receipt_dict = receipt_df.to_dict(orient='index')
        existed_max_number = max([int(rec["收據單號"][7:]) for rec in receipt_dict.values()])
    except:
        receipt_dict = {}
        existed_max_number = 0
    next_receipt_number = existed_max_number+1
    length = len(str(next_receipt_number))
    receipt_number = f"GARS707{'0'*(3-length)}{next_receipt_number}"
    receipt_dict[next_receipt_number] = {'收據單號': receipt_number, "收據收件人": client_name}
    receipt_df = pd.DataFrame.from_dict(receipt_dict, orient="index")
    receipt_df.to_excel("收據明細.xlsx", index=False)

    pdf_file.drawString(100, weight, f"Receipt No: {receipt_number}")
    
    weight -= 15
    pdf_file.drawString(100, weight, f"Date      : {receipt_date}")

    weight -= 15
    pdf_file.drawString(100, weight, f"Payer Name: {client_name}   {client_eng_name}")

    weight -= 50
    pdf_file.drawString(50, weight, f"茲收到")
    pdf_file.drawString(400, weight, "日期")

    weight -= 15
    pdf_file.drawString(50, weight, "Received From_______________________________")
    pdf_file.drawString(400, weight, "Date_____________________")
    change_font(pdf_file, font, 15)
    pdf_file.drawString(150, weight+5, f"{client_name}")
    pdf_file.drawString(450, weight+5, f"{receipt_date}")
    change_font(pdf_file, font, 12)

    # 寫入費用信息
    weight -= 35
    pdf_file.drawString(50, weight, "来大银")
    

    weight -= 15
    pdf_file.drawString(50, weight, "The Sum of Ringgit_________________________________________________________________")
    change_font(pdf_file, font, 15)
    pdf_file.drawString(250, weight+5, chinese_price)
    change_font(pdf_file, font, 12)
    
    weight -= 35
    pdf_file.drawString(50, weight, "系对还")

    weight -= 15
    pdf_file.drawString(50, weight, "Being payment of___________________________________________________________________")
    change_font(pdf_file, font, 15)
    pdf_file.drawString(160, weight+5, member_type)
    change_font(pdf_file, font, 12)

    weight -= 50
   
    weight -= 25
        
    weight -= 15
    pdf_file.drawString(50, weight, "马币")

    # pdf_file.drawString(440, weight-7, "________")
    # pdf_file.drawString(440, weight-20, "  财政")
    # pdf_file.drawString(440, weight-30, "Treasurer")
    # pdf_file.drawString(500, weight-7, "________")
    # pdf_file.drawString(500, weight-20, "  经手人")
    # pdf_file.drawString(500, weight-30, "Collector")

    weight -= 15
    pdf_file.drawString(50, weight, "Ringgit Malaysia___________________________")
    change_font(pdf_file, font, 15)
    pdf_file.drawString(200, weight+5, f"{str(prices)}.00")
    change_font(pdf_file, font, 12)

    change_font(pdf_file, fontbold, 9)
    weight -= 80
    pdf_file.drawString(50, weight, "Persatuan Perubatan Tradisional dan Komplementari Penyelamat Akupunktur")
    
    weight -= 20
    change_font(pdf_file, fontitalic, 7)
    pdf_file.drawString(50, weight, "GLOBAL ACUPUNCTURE RESCUE TRADITIONAL AND COMPLEMENTARY MEDICAL SOCIETY")
    change_font(pdf_file, font, 12)

    logo = utils.ImageReader(images)
    pdf_file.drawImage(logo, 50, 720,width=100, height=100)

    link = infos.get("link")

    # create a paragraph style with a hyperlink
    style = ParagraphStyle('hyperlink')
    style.fontName = font
    style.textColor = 'blue'
    style.fontSize = 12
    style.leading = 14
    style.href = infos.get("link")

    # create a hyperlink
    text = f'<a href="{link}">缴费证明</a>'
    paragraph = Paragraph(text, style)

    paragraph.wrapOn(pdf_file, 6 * units.cm, 6*units.cm)
    paragraph.drawOn(pdf_file, 1.8*units.cm, 3*units.cm)
    
    text = f'<a href="{link}">Proof of Payment Transaction</a>'
    paragraph2 = Paragraph(text, style)

    paragraph2.wrapOn(pdf_file, 6 * units.cm, 6*units.cm)
    paragraph2.drawOn(pdf_file, 1.8*units.cm, 2.5*units.cm)

    # 完成並關閉PDF檔案
    pdf_file.showPage()
    pdf_file.save()

def change_font(pdf_file: canvas.Canvas, font, size, bold: bool = False, italic: bool = False):
    if bold and italic:
        return pdf_file.setFont(font, size, leading="bolditalic")
    elif bold:
        return pdf_file.setFont(font, size, leading="bold")
    elif italic:
        return pdf_file.setFont(font, size, leading="italic")    
    else:
        return pdf_file.setFont(font, size)

def arab_price_to_chinese_price(arab_price: int):
    str_price = str(arab_price)
    chinese_price = []  # 0:個位數, 1:十位數, 2:百位數, 3:千位數, 4:萬位數

    for idx, num in enumerate(str_price):
        if num == "0":
            chinese_num="零"
        elif num == "1":
            chinese_num="壹"
        elif num == "2":
            chinese_num="貳"
        elif num == "3":
            chinese_num="參"
        elif num == "4":
            chinese_num="肆"
        elif num == "5":
            chinese_num="伍"
        elif num == "6":
            chinese_num="陸"
        elif num == "7":
            chinese_num="柒"
        elif num == "8":
            chinese_num="捌"
        elif num == "9":
            chinese_num="玖"
        chinese_price.append(chinese_num)
    length = len(chinese_price)
    if length-1 == 4:
        unit = ["萬","仟","佰","拾"]
    elif length-1 == 3:
        unit = ["仟","佰","拾"] 
    elif length-1 == 2:
        unit = ["佰","拾"]
    elif length-1 == 1:
        unit = ["拾"]
    
    chinese = ""
    if length-1 == 0:
        chinese += chinese_price+"元"
    else:
        # for chi, un in zip(chinese_price[:-1], unit):
        #     if chi != "零":
        #         chinese += chi+un
        for i in range(len(chinese_price[:-1])):

            if chinese_price[i] != "零":
                chinese += chinese_price[i] + unit[i]
            else:
                if i != len(chinese_price[-1]) - 1:
                    _next = chinese_price[i+1]
                    if _next != '零':
                        chinese += chinese_price[i]

        if chinese_price[-1]!= "零":
            chinese += chinese_price[-1]+"元"
        else:
            chinese += "元"

    return chinese

