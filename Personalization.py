from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from Translation import audio_to_text
import google.generativeai as genai
from gensim import corpora, models
from nltk.corpus import wordnet
from nltk.corpus import stopwords
import moviepy.editor as mp
import pandas as pd
import llama2
import os
import re


def extract_caption(video_path):
    clip = mp.VideoFileClip(video_path)
    audio_path = f"./temp.wav"
    clip.audio.write_audiofile(audio_path)
        
    caption = audio_to_text(audio_path)
    return caption

def process_caption(text_to_translate):
        
    def preprocess_text(text):
        # Tokenization
        tokens = word_tokenize(text.lower())  # Convert to lowercase

        # Remove punctuation and non-alphabetic characters
        tokens = [word for word in tokens if word.isalpha()]

        # Remove stopwords
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]

        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]

        return tokens

    caption_text = text_to_translate
    # Preprocess the text
    preprocessed_texts = [preprocess_text(caption_text)]
    print(preprocessed_texts)

    # Create a dictionary representation of the documents
    dictionary = corpora.Dictionary(preprocessed_texts)

    # Convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in preprocessed_texts]

    # Build LDA model
    lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=15)

    # Print topics
    for idx, topic in lda_model.print_topics():
        print(f'Topic {idx + 1}: {topic}')

    # Extracted topics from LDA model
    extracted_topics = [lda_model.print_topic(i) for i in range(lda_model.num_topics)]

    # Formatting topics into a single string
    formatted_topics = "\n".join(extracted_topics)

    
    model = genai.GenerativeModel('llama-2')
    response1 = model.generate_content("what subject do you think this given text is about?"+(text_to_translate))
    print(response1.text)
    
    response = model.generate_content("Write 4 relevant" + response1.text + "chapter names looking at the following tokens(technical concepts):"+''.join(extracted_topics))
    print(response.text)
    
    pattern = r'\d+\.\s*(.*)'

    # Find all matches of the pattern in the text
    matches = re.findall(pattern, response.text)

    # Extract only the topics
    suggested_topics = [match.strip() for match in matches]

    print(suggested_topics)

    # Load a pre-trained BERT-based model
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # Load the Excel file into a Pandas DataFrame (replace with your data)
    excel_file = 'student_info.xlsx'
    df = pd.read_excel(excel_file)

    # Extract the topics that the student hasn't studied (where 'Studied' column is 0)
    not_studied_topics = df[df['Studied'] == 0]['Topic'].tolist()

    # Get BERT embeddings for suggested and not studied topics
    suggested_topic_embeddings = model.encode(suggested_topics)
    not_studied_topic_embeddings = model.encode(not_studied_topics)

    # Calculate cosine similarity between suggested and not studied topics
    similarity_matrix = cosine_similarity(suggested_topic_embeddings, not_studied_topic_embeddings)

    # Loop through suggested topics and find similar not studied topics
    for i, topic_similarities in enumerate(similarity_matrix):
        similar_topics_indices = topic_similarities.argsort()[::-1]  # Sort by similarity
        similar_topics = [not_studied_topics[idx] for idx in similar_topics_indices]
        print(f"Suggested Topic: {suggested_topics[i]}")
        print(f"Similar Not Studied Topics: {similar_topics[0]}\n")

    preprocessed_text = preprocess_text(caption_text)
    print(preprocessed_text)  # Ensure the list is of individual words
    
    model = genai.GenerativeModel('llama-2')
    response = model.generate_content("List any technical terms related to the given topic: "+''.join(preprocessed_text))
    answer=response.text
    answer_list = answer.split('\n')

    # Print the list
    print(answer_list)

    def get_word_definition(word):
        synsets = wordnet.synsets(word)
        if not synsets:
            return f"No definition found for '{word}'"
        return synsets[0].definition() if synsets else f"No definition found for '{word}'"

    model = genai.GenerativeModel('llama-2')
    response = model.generate_content("Give short explanation of the technical terms: "+''.join(answer))
    definition=response.text
    print(response.text)
    
    return definition