# Imports
import re
import unicodedata
import json
import nltk
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords

import pandas as pd


####### Preparation

# basic_clean: take in a string and apply basic text cleaning
# - lowercase everything
# - normalize unocide characters
# - replace anything that is not a letter, number, whitespace or a single quote

def basic_clean(string):
    '''
    This function takes in a string and applies basic text cleaning. Returns the string.
    '''
    # Lowercase
    string = string.lower()
    # Unicode
    string = unicodedata.normalize('NFKD', string)\
        .encode('ascii', 'ignore').decode('utf-8', 'ignore')
    # Replace non-character
    string = re.sub(r"[^a-z0-9'\s]", '', string)
    # Return string
    return string


def tokenize(string):
    '''
    This function takes a string and tokenizes it before returning.
    '''
    # Create tokenizer
    tokenizer = nltk.tokenize.ToktokTokenizer()
    # Use with string
    string = tokenizer.tokenize(string, return_str = True)
    # Return string
    return string


def stem(string):
    '''
    This function takes in a string and returns a string with words trimmed.
    '''
    # Create stemmer
    ps = nltk.porter.PorterStemmer()
    # Stem the words
    stems = [ps.stem(word) for word in string.split()]
    # Join list of words back into string
    string = ' '.join(stems)
    # Return string
    return string


def lemmatize(string):
    '''
    This function takes in a string and returns a string with words lemmatized.
    '''
    # Create lemmatizer
    wnl = nltk.stem.WordNetLemmatizer()
    # Lemmatize the words
    lemmas = [wnl.lemmatize(word) for word in string.split()]
    # Join list of words back into string
    string = ' '.join(lemmas)
    # Return string
    return string


def remove_stopwords(string, extra_words = [], exclude_words = []):
    '''
    This function takes in a string, with optional extra or exclusion words, and returns a string.
    '''
    # Create stopword_list
    stopword_list = stopwords.words('english')
    # Remove the 'exclude_words' from stopword_list
    stopword_list = set(stopword_list) - set(exclude_words)
    # Add in extra_words
    stopword_list = stopword_list.union(set(extra_words))

    # Split words in string
    words = string.split()
    # Create list of words from string with stopwords removed
    new_string = [word for word in words if word not in stopword_list]
    # Join words in list back into strings
    without_stopwords = ' '.join(new_string)
    # Return string
    return without_stopwords


def prep_data(df, extra_words = [], exclude_words = []):
    '''
    This function takes in our dataframes (CodeUp blogs or news articles in these examples), and applies cleaning, stemming, and lemmatizing of the text.
    Returns a dataframe when clean, stemmed, and lemmatized columns along with the title and original text. Has option to include extra or exclude words 
    for stopwords.
    '''
    # Renaming the content column as original
    df = df.rename(columns={'content': 'original'})
    # Cleaned text column
    df['clean'] = (df.original.apply(basic_clean).apply(tokenize).apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words))
    # Stemmed text column
    df['stemmed'] = (df.original.apply(basic_clean).apply(tokenize).apply(stem).apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words))
    # Lemmatized text column
    df['lemmatized'] = (df.original.apply(basic_clean).apply(tokenize).apply(lemmatize).apply(remove_stopwords, extra_words=extra_words, exclude_words=exclude_words))
    # Return the df 
    return df


