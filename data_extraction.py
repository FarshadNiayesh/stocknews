import pandas as pd
from newspaper import Article


news = pd.read_csv('data/news.csv')
for i, row in news.iterrows():
    article = Article(row['url'])
    article.download()
    article.parse()
    filename = 'data/corpus/{}.txt'.format(row['news_id'])
    with open(filename, 'w+', encoding='utf-8') as f:
        f.write(article.text)
