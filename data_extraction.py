import argparse
import requests
import pandas as pd
from newspaper import Article


def download_news():
    news = pd.read_csv('data/news.csv')
    for i, row in news.iterrows():
        article = Article(row['url'])
        article.download()
        article.parse()
        filename = 'data/corpus/{}.txt'.format(row['news_id'])
        with open(filename, 'w+', encoding='utf-8') as f:
            f.write(article.text)


def download_prices():
    endpoint = 'https://api.iextrading.com/1.0'
    symbols = pd.read_csv('data/symbols.csv')
    prices_list = []
    for i, row in symbols.iterrows():
        symbol = row['symbol']
        print('Download prices for {}'.format(symbol))
        url = endpoint + '/stock/{}/chart/5y'.format(symbol)
        r = requests.get(url)
        prices = pd.DataFrame(r.json())
        if len(prices) == 0:
            continue
        prices['symbol'] = symbol
        prices_list.append(prices)
    prices_df = pd.concat(prices_list, ignore_index=True)
    prices_df.to_csv('data/prices.csv')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--news', action='store_true')
    parser.add_argument('--prices', action='store_true')
    args = parser.parse_args()
    if args.news:
        download_news()
    if args.prices:
        download_prices()
