#imports necessary packages
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

#function for building the bigram model
#takes a pandas series of texts (ex. df['text']) and creates a bigram model
#parameters:
#text_series: pandas series containing the text
#min_count: parameter for ngram mdoel; only ngrams that occur this many times or more will be included

#based off code found at: https://towardsdatascience.com/text-analysis-basics-in-python-443282942ec5

def ngram_model(text_series, min_count):

    #builds the bigram (2) and trigram (3) model on the series
    c_vec = CountVectorizer(ngram_range=(2,3))
    ngrams = c_vec.fit_transform(text_series)
    count_values = ngrams.toarray().sum(axis=0)
    vocab = c_vec.vocabulary_

    #builds a dataframe of ngrams and frequencies
    df_ngram = pd.DataFrame(sorted([(count_values[i],k) for k,i in vocab.items()], reverse=True)
            ).rename(columns={0: 'frequency', 1:'ngram'})

    #filters to include only those occuring more than min_count
    df_ngram = df_ngram[df_ngram['frequency']>=min_count]

    #adds the relevant ngram to the documents
    for idx in range(text_series.shape[0]):

        #if the document at the index contains the bigram, adds it to the document
        for ngram in df_ngram['ngram']:
            if ngram and ngram in text_series[idx]:
                text_series[idx] = text_series[idx] + ' ' + '_'.join(ngram.split())

    return text_series
                
