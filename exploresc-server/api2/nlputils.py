from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
nltk.download('punkt')
nltk.download('stopwords')

def tokenize_text(text):
    tokens = {}
    stop_words = list(stopwords.words('english'))
    stop_words.extend([
        '{',
        '}',
        '[',
        ']',
        '(',
        ')',
        ',',
        '.',
        '\'',
        '\'\'',
        '/',
        '<',
        '>',
        ';',
        'br',
        '#',
        '&',
        '/b',
        '/i'
        ])
    doc_len = 0
    for item in [w for w in word_tokenize(text) if not w in stop_words]:
        if item in tokens:
            tokens[item] += 1
        else:
            tokens[item] = 1
        doc_len += 1
    return tokens,doc_len