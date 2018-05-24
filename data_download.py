import requests
import pandas as pd


endpoint = 'https://api.iextrading.com/1.0'

r = requests.get(endpoint + '/ref-data/symbols')
symbols = pd.DataFrame(r.json())
symbols.to_csv('data/symbols.csv')

url = endpoint + '/stock/{}/news/last/{}'
news_list = []
for i, row in symbols.iterrows():
    symbol = row['symbol']
    print('Download news for {}'.format(symbol))
    r = requests.get(url.format(symbol, 50))
    news = r.json()
    news = pd.DataFrame(news)
    news['symbol'] = symbol
    news_list.append(news)
    if i > 4:
        break

news = pd.concat(news_list, ignore_index=False)
news['news_id'] = list(range(len(news)))
news.to_csv('data/news.csv')
