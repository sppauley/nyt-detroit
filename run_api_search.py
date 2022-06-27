from api_request import build_dataset


key = str(input("input nyt api key: "))
term = str(input("input search term: "))
start_year = int(input("input start year: "))
end_year = int(input("input end year: "))

build_dataset(key, term, start_year, end_year)
