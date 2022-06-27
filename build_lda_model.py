#import necessary packages
import pandas as pd
import gensim

#gets user input to get processed data
file = pd.read_csv (str(input('input preprocessed csv file name: '))+'.csv')
col = col = str(input('input column name containing the text: '))
df = [doc.split() for doc in file[col]] #splits into tokens

#builds the dictionary
dictionary = gensim.corpora.Dictionary(df)

#gets users input to filter dictionary
#no_below = int(input('input no_below: '))
#no_above = float(input('input no_above: '))
#dictionary.filter_extremes(no_below=no_below, no_above=no_above)
dictionary.filter_extremes(no_below=15, no_above=0.6, keep_n=100000)

#builds the model corpus
corpus = [dictionary.doc2bow(doc) for doc in df]

#builds the model from a set of user-defined parameters
k=100
#k = int(input('input value for k: '))
#lda_model = gensim.models.LdaMulticore(corpus, num_topics=k, id2word=dictionary, passes=10,
#                                       per_word_topics=True, alpha='asymmetric', iterations=100,
#                                       chunksize=100, random_state=100, eval_every=1)
lda_model = gensim.models.LdaMulticore(corpus=corpus,
                                       id2word=dictionary,
                                       num_topics=50)

#prints values for coherence and perplexity
coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, texts=processed_docs, dictionary=dictionary, coherence='u_mass')
coherence_lda = coherence_model_lda.get_coherence()
print('-'*50)
print('\nCoherence Score:', coherence_lda)
print('\nPerplexity Score: ', lda_model.log_perplexity(bow_corpus))  
print('-'*50)
