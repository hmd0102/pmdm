from PyPDF2 import PdfWriter

writer = PdfWriter()
writer.add_blank_page(width=595, height=842)  # A4 size

with open("empty.pdf", "wb") as f:
    writer.write(f)