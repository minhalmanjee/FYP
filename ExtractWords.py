import google.generativeai as genai
from IPython.display import display
import llama2

def extractTechwords(caption):
    model = genai.GenerativeModel('llama-2')
    response = model.generate_content("list down technical terms and advanced english words from this text, look precisely: "+caption)
    print(response.text)
    extracted_words = response.text.split("\n")

    tech_words_cleaned = [word.strip('*- ') for word in extracted_words if word.strip('*- ')]   

    print("Extracted Technical Words:", tech_words_cleaned)
    return tech_words_cleaned