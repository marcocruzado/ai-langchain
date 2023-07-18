import os 
from PyPDF2 import PdfReader
import pandas as pd
import re
from dotenv import load_dotenv
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


path="./v1/data/FAQS ALICIA VENTAS.pdf"
#Reglamento-Nacional-de-Transito.txt


def pdf_to_text(path):
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)
    text = ""
    for page in enumerate(reader.pages):
        text += page.extractText()
    return text

print(pdf_to_text(path))