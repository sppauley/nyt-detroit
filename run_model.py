#imports necessary packages and functions
from data_preprocess import preprocess
from ngram_model import ngram_model
import pandas as pd

#gets user input to define parameters
df = pd.read_csv (str(input('input csv file name: '))+'.csv')
col = str(input('input column name containing the text: '))

#step one: run the preprocess function
df1 = preprocess(df[col])

#step two: get parameters and run ngram model
min_count = str(input('input min_count for ngram model: '))
df2 = ngram_model(df1, min_count)
