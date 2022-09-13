import docx2txt
from pdfminer.high_level import extract_text as extr_pdf
import filetype 

def is_pdf_type(path):
	return filetype.guess(path).mime == "application/pdf"

def is_pdf(path):
	try:
		extract_text_from_pdf(path)
		return True
	except:
		return False

def extract_text_from_pdf(path):
	return extr_pdf(path)


def extract_text_from_docx(path):
	text = docx2txt.process(path)
	text = [line.replace('\t', ' ') for line in text.split('\n') if line]
	if text:
		return ' '.join(text)

def extract_text_from_file(path):
	if is_pdf_type(path):
		if is_pdf(path):
			return extract_text_from_pdf(path)
		raise Exception(f'can\'t open file {path} as PDF!')
	return extract_text_from_file(path)

	
def main():
	pass


if __name__ == '__main__':
	main()