#imports necessary packages
import pandas as pd
import contractions
import string
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *

#this function will apply preprocessing over a panda series, ex df['text']
def preprocess(text_series):

    #convert to lowercase
    text_series = text_series.apply(lambda x: ' '.join([word.lower() for word in x.split()]))

    #expand contractions
    text_series = text_series.apply(lambda x: ' '.join([contractions.fix(word) for word in x.split()]))

    #remove punctuation
    text_series = text_series.apply(lambda x: ''.join([character for character in x if character not in string.punctuation]))

    #remove numbers
    text_series = text_series.apply(lambda x: ' '.join(re.sub("[^a-zA-Z]+", " ", x).split()))

    #remove stopwords
    stopwords = [sw for sw in nltk.corpus.stopwords.words('english')]
    text_series = text_series.apply(lambda x: ' '.join([word for word in x. split() if word not in stopwords]))

    #lemmatization
    text_series = text_series.apply(lambda x: ' '.join([nltk.stem.PorterStemmer().stem(WordNetLemmatizer().lemmatize(word, pos='v')) for word in x.split()]))

    return text_series
