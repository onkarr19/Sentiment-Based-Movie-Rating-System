import os
import pickle
import re
import string

import numpy as np
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import TweetTokenizer


def load_data(file='model_1.pkl'):
    file = os.getcwd() + r'\Notebooks\\' + file
    with open(file, 'rb') as f:
        return pickle.load(f)


def process_statements(statement):
    """Process statement function.
    Input:
        statement: a string containing a statement
    Output:
        statements_clean: a list of words containing the processed statement

    """
    stemmer = PorterStemmer()
    stopwords_english = stopwords.words('english')

    # remove stock market tickers like $GE
    statement = re.sub(r'\$\w*', '', statement)

    # remove old style retweet text "RT"
    statement = re.sub(r'^RT[\s]+', '', statement)

    # remove hyperlinks
    statement = re.sub(r'https?:\/\/.*[\r\n]*', '', statement)

    # remove hashtags
    # only removing the hash # sign from the word
    statement = re.sub(r'#', '', statement)

    # tokenize statements
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                               reduce_len=True)
    statement_tokens = tokenizer.tokenize(statement)

    statements_clean = []
    for word in statement_tokens:
        if (word not in stopwords_english and  # remove stopwords
                word not in string.punctuation):  # remove punctuation
            # statements_clean.append(word)
            stem_word = stemmer.stem(word)  # stemming word
            statements_clean.append(stem_word)

    return statements_clean


def getvalue(s):
    cleaned = process_statements(s)
    arr = []
    model_dict = load_data('model_1.pkl')
    for i in cleaned:
        x = model_dict.get(i, 0.5)
        arr.append(x)

    return np.mean(arr)
