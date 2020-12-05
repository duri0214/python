from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

input_path = 'market_report_fo_em_topic.pdf'
output_path = 'result.txt'

manager = PDFResourceManager()

with open(output_path, "wb") as txt_output:
    with open(input_path, 'rb') as pdf_input:
        with TextConverter(manager, txt_output, codec='utf-8', laparams=LAParams()) as conv:
            interpreter = PDFPageInterpreter(manager, conv)
            for page in PDFPage.get_pages(pdf_input):
                interpreter.process_page(page)
