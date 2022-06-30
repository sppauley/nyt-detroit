import requests
import json
import pandas as pd
import time
import calendar


def build_dataset(key, term, start_year, end_year):
    cycle = 0
    script_start = time.time()

    # builds the range of years and months, which will later be iterated through
    years = range(start_year, end_year)
    months = range(1, 13)

    # empty dataframe for article storage
    articles_df = pd.DataFrame()

    # iterates through the years in the given range
    for year in years:

        #separates into months
        for month in months:
        
            # defines variables for building the http request and looping
            month_str = str(month).zfill(2) #uses zfill to convert 1 to 01, etc.
            end_day = calendar.monthrange(year, month)[1] #end days can vary from month to month
            start = f"{year}{month_str}01" 
            end = f"{year}{month_str}{end_day}"
            page = 0
            more = True  # determines whether there are more articles to loop thru

            # loops through requests
            while more:

                # counts cycles for visibility of process
                cycle += 1
                print(cycle)

                # builds search url and query, then converts to json
                search_url = f'https://api.nytimes.com/svc/search/v2/articlesearch.json/?begin_date={start}' \
                             f'&end_date={end}&api-key={key}&page={page}&q={term}'
                response = requests.get(search_url)
                response = response.json()

                # if possible, appends the articles to articles_df and moves to the next page
                try:

                    # concats the unformatted json response into the dataframe
                    docs = response['response']['docs']  # gets docs from the api payload
                    articles_df = pd.concat([articles_df, pd.DataFrame(docs)])

                    # if the current page is full (10 docs) and the page is less than or equal to 100, keep going
                    if len(docs) == 10 and page <= 100: #page limit of 100 in dev portal; 10 results per page
                        page += 1
                        more = True
                    else:
                        more = False

                    # NYT developer portal recommends a 6-second delay between requests to avoid hitting
                    # the per-minute limit
                    time.sleep(6)

                # error exception
                except KeyError as e:
                    print(response)

                    # if it hits the daily limit, pauses for 24 hours
                    if response['fault'] and 'Rate limit quota violation.' in err_msg['fault']['faultstring']:
                        print("Pausing for 24 hours")
                        time.sleep(86400)

                    # otherwise, breaks the for loop
                    else:
                        break;

    # sets filename based on query
    filename = f"{int(script_start)}_{start_year}_{end_year}_{term}"
    # gets the dataframe and converts it to csv
    articles_df.to_csv(filename, index=False)
    script_stop = time.time()
    script_length = script_stop - script_start
    print(f"Script finished in {script_length} seconds")
