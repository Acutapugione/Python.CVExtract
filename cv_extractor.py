import spacy
from spacy.matcher import Matcher
import spacy
import re
import pandas as pd
import nltk
from nltk.corpus import stopwords

nltk.download('words')
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
 

nlp = spacy.load('en_core_web_sm')
#noun_chunks = nlp.noun_chunks
matcher = Matcher(nlp.vocab)



STOPWORDS = set(stopwords.words('english'))
EDUCATION = [
            'BE','B.E.', 'B.E', 'BS', 'B.S', 
            'ME', 'M.E', 'M.E.', 'MS', 'M.S', 
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH', 
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]

class CVExtractor:
    def __init__(self, text):
        self.__text = text
    
    @property
    def name(self):
        return self.extract_name()
    
    @property
    def phone(self):
        return self.extract_mobile_number()
    
    @property
    def email(self):
        return self.extract_email()

    @property
    def skills(self):
        return self.extract_skills()
    
    @property
    def education(self):
        return self.extract_education()
    
    def extract_name(self):
        nlp_text = nlp(self.__text)

        patterns = [
            [{'POS': 'PROPN'}, {'POS': 'PROPN'}],
        ]
        matcher.add('NAME', patterns)

        matches = matcher(nlp_text)
        
        for match_id, start, end in matches:
            span = nlp_text[start:end]
            return span.text

    def extract_mobile_number(self):
        phone = re.findall(re.compile(r'(?:(?:\+?([1-9]|[0-9][0-9]|[0-9][0-9][0-9])\s*(?:[.-]\s*)?)?(?:\(\s*([2-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9])\s*\)|([0-9][1-9]|[0-9]1[02-9]|[2-9][02-8]1|[2-9][02-8][02-9]))\s*(?:[.-]\s*)?)?([2-9]1[02-9]|[2-9][02-9]1|[2-9][02-9]{2})\s*(?:[.-]\s*)?([0-9]{4})(?:\s*(?:#|x\.?|ext\.?|extension)\s*(\d+))?'), self.__text)
        
        if phone:
            number = ''.join(phone[0])
            if len(number) > 10:
                return '+' + number
            else:
                return number

    def extract_email(self):
        email = re.findall("([^@|\s]+@[^@]+\.[^@|\s]+)", self.__text)
        if email:
            try:
                return email[0].split()[0].strip(';')
            except IndexError:
                return None

    def extract_skills(self):
        nlp_text = nlp(self.__text)

        # removing stop words and implementing word tokenization
        tokens = [token.text for token in nlp_text if not token.is_stop]
        
        # reading the excel file
        data = pd.read_excel('skills.xlsx')
        #['Journal'].tolist()
        
        # reading the csv file
        #data = pd.read_csv("skills.csv") 
        
        # extract values
        #skills = list(data.columns.values)
        skills = data['Journal'].tolist()
        skills = set([x.lower() for x in skills])
        skillset = []
        
        # check for one-grams (example: python)
        for token in tokens:
            if token.lower() in skills:
                skillset.append(token)
        
        # check for bi-grams and tri-grams (example: machine learning)
        for token in nlp_text.noun_chunks:
            token = token.text.lower().strip()
            if token in skills:
                skillset.append(token)
        
        return [i.capitalize() for i in set([i.lower() for i in skillset])]

    def extract_education(self):
        nlp_text = nlp(self.__text)

        # Sentence Tokenizer
        nlp_text = [sent.text.strip() for sent in nlp_text.sents]

        edu = {}
        # Extract education degree
        for index, text in enumerate(nlp_text):
            for tex in text.split():
                # Replace all special symbols
                tex = re.sub(r'[?|$|.|!|,]', r'', tex)
                if tex.upper() in EDUCATION and tex not in STOPWORDS:
                    edu[tex] = text + nlp_text[index + 1]

        # Extract year
        education = []
        for key in edu.keys():
            year = re.search(re.compile(r'(((20|19)(\d{2})))'), edu[key])
            if year:
                education.append((key, ''.join(year[0])))
            else:
                education.append(key)
        return education
