import nltk
from nltk.corpus import words
nltk.download('words')
english_words_ = words.words()

def is_coherent_nltk(text):
    """
    Check if the text is coherent using NLTK's words corpus.
    """
    english_words = set(english_words_)
    words_in_text = text.split()
    for word in words_in_text:
        if word.lower() not in english_words:
            return False
    return True


def filter_incoherent_texts_nltk(texts):
    """
    Filter out incoherent texts from a list of texts.
    """
    filtered_texts = []
    for text in texts:
        if is_coherent_nltk(text):
            filtered_texts.append(text)
    return filtered_texts
