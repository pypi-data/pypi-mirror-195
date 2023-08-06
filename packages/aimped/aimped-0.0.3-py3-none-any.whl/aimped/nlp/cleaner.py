import re
import nltk


def text_cleaner(text:str, 
                 language:str='english', 
                 remove_stopwords:bool=True, 
                 remove_short_words:int=1, 
                 remove_numbers:bool=True, 
                 remove_punctuation:bool=True, 
                 remove_non_ascii:bool=True, 
                 lower_case:bool=True)->str:
    # lower case
    if lower_case: 
        text = text.lower()
    # remove punctuation
    if remove_punctuation:
        text = re.sub(r'[^\w\s]','',text)
    # remove numbers
    if remove_numbers:
        text = re.sub(r'\d+','',text)
    # remove stop words
    if remove_stopwords:
        stopwords = nltk.corpus.stopwords.words(language)
        text = ' '.join([word for word in text.split() if word not in stopwords])
    # remove short words
    if remove_short_words:
        text = ' '.join([word for word in text.split() if len(word) > remove_short_words])
    # remove non-ascii characters
    if remove_non_ascii:
        text = text.encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

if __name__ == "__main__":
    text = "This is an easy test°′﻿, and This is the last chance."
    print(text_cleaner(text))