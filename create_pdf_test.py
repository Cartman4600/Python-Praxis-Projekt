
# importing modules 
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from reportlab.pdfbase import pdfmetrics 
from reportlab.lib import colors 
  
#
fileName = r"sample.pdf"
documentTitle = 'sample'
title = "Real Estate Price Calculator"
subTitle = 'Zusammenfassung'
textLines = ["{} : {}",
             "{} : {}",
             "{} : {}",
             "{} : {}",
             "{} : {}",
             "{} : {}",
             "{} : {}",
             "{} : {}",
             "{} : {}",
             "{} : {}"  
            ] 
image = r'logo.jpg'
  
# 
pdf = canvas.Canvas(fileName) 
  
# 
pdf.setTitle(documentTitle) 
  
# 
pdf.setFont('Courier', 30) 
pdf.drawCentredString(300, 770, title) 
  
#
pdf.setFillColorRGB(0, 0, 0) 
pdf.setFont("Courier", 24) 
pdf.drawCentredString(290, 720, subTitle) 
  
#
pdf.line(30, 710, 550, 710) 
  
#
text = pdf.beginText(40, 680) 
text.setFont("Courier", 18) 
text.setFillColor(colors.black) 
for line in textLines: 
    text.textLine(line) 
pdf.drawText(text) 
  
# drawing a image at the  
# specified (x.y) position 
pdf.drawImage(image, 0, 0 , width=400, height=300, preserveAspectRatio=True)  
# saving the pdf 
pdf.save() 
