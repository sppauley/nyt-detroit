#imports necessary packages and functions
from data_preprocess import preprocess
from ngram_model import bigram_model
import pandas as pd

#gets user input to define parameters
df = pd.read_csv (str(input('input csv file name: '))+'.csv')
col = str(input('input column name containing the text: '))

df1 = preprocess(df[col])
