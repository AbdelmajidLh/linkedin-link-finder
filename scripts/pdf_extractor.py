import PyPDF2
import pandas as pd
import logging

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text_from_pdf(self):
        text_list = []
        with open(self.pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()
                text_list.append(text)
        return text_list

    def pdf_to_dataframe(self):
        text_list = self.extract_text_from_pdf()
        df = pd.DataFrame(text_list, columns=["Page Text"])
        return df
