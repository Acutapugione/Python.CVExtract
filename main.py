import docx2txt
import nltk
import pandas
from PyPDF2 import PdfFileReader
from pdfminer.high_level import extract_text as extr_pdf
from cv_extractor import CVExtractor
from extract_helpers import *

excel_data = pandas.read_excel('data/journal_list.xlsx')
SKILLS = [i.lower() for i in excel_data['Journal'].tolist()]
files_list = [
    'test1.pdf', 
    'test2.pdf',
    'test3.pdf',
    ]


def main():    
    for file in files_list:
        text = extract_text_from_file(f'data/{file}')
        extractor = CVExtractor(text)
        print(extractor.name)
        print(extractor.phone)
        print(extractor.email)
        print(extractor.skills)
        print(extractor.education)

if __name__ == '__main__':
    main()