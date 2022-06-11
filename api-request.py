import requests
import json
import pandas as pd
import time

def build_dataset(key, term, start_year, end_year):

    #builds the range of years, which will later be iterated through
    years = range(start_year, end_year)

    #empty dataframe for article storage
    articles_df = pd.DataFrame() 

    #iterates through the years in the given range
    for year in years:

        #defines variables for building the http request and looping
        start = f"{year}0101"
        end = f"{year}1231"
        page = 0
        more = True #determines whether there are more articles to loop thru

        #loops through requests
        while more:

            #builds search url and query, then converts to json
            search_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json/?begin_date={start}&end_date={end}&api-key={key}&page={page}&q={term}'
            response = requests.get(search_url)
            response = response.json()

            #if possible, appends the articles to articles_df and moves to the next page
            try:

                #concats the unformatted json response into the dataframe
                docs = response['response']['docs'] #gets docs from the api payload
                articles_df = pd.concat([articles_df, pd.DataFrame(docs)])
                
                #if the current page is full (10 docs) and the page is less than or equal to 200, keep going
                if len(docs) == 10 and page <= 200:
                    page += 1
                    more = True
                else:
                    more = False

                #NYT developer portal recommends a 6-second delay between requests to avoid hitting the per-minute limit
                time.sleep(6)

            #may have hit the daily limit, so pauses execution for 24-hours if given an error message
            except KeyError:
                time.sleep(86400)

    #gets the dataframe and converts it to csv
    articles_df.to_csv('../nyt_data.csv', index=False)
