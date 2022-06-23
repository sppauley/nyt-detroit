#import necessary packages
import pandas as pd
import gensim

#gets user input to get processed data
df = pd.read_csv (str(input('input preprocessed csv file name: '))+'.csv')

#builds the dictionary
dictionary = gensim.corpora.Dictionary(df)
count = 0
for k, v in dictionary.iteritems():
    count += 1
    if count > 10:
        break

#gets users input to filter dictionary
no_below = str(input('input no_below: '))
no_above = str(input('input no_above: '))
dictionary.filter_extremes(no_below=no_below, no_above=no_above)

#builds the model corpus
bow_corpus = [dictionary.doc2bow(doc) for doc in df]

#builds the model from a set of user-defined parameters
k = str(input('input value for k: '))
lda_model = gensim.models.LdaMulticore(bow_corpus, num_topics=k, 
                                       id2word=dictionary, 
                                       passes=10, per_word_topics=True, 
                                       alpha='asymmetric', iterations=100,  
                                       chunksize=100, 
                                       random_state=100, eval_every=1)

#prints values for coherence and perplexity
coherence_model_lda = gensim.models.CoherenceModel(model=lda_model, texts=processed_docs, dictionary=dictionary, coherence='u_mass')
coherence_lda = coherence_model_lda.get_coherence()
print('-'*50)
print('\nCoherence Score:', coherence_lda)
print('\nPerplexity Score: ', lda_model.log_perplexity(bow_corpus))  
print('-'*50)
