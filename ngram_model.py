#imports necessary packages
from gensim.models import Phrases
import pandas as pd

#function for building the bigram model
#takes a pandas series of texts (ex. df['text']) and creates a bigram model
#parameters:
#text_series: pandas series containing the text
#min_count: parameter for ngram mdoel; only ngrams that occur this many times or more will be included

#based off code found at: https://radimrehurek.com/gensim/auto_examples/tutorials/run_lda.html

def bigram_model(text_series, min_count):

    #builds the bigram model on the series
    model = Phrases(text_series, min_count = min_count)

    #adds the ngram to the document if it occurs more times than the min_count
    for idx in range(text_series.shape[0]):

        #if the token contains an underscore (indicates bigram), adds to document
        for token in model[text_series[idx]]:
            if '_' in token:
                    text_series[idx].append(token)

    return text_series
                
