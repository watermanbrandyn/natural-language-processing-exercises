import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

## Blog Articles







## Inshort News articles

def get_news_articles():
    '''
    This function returns a dataframe after acquiring the selected categories of news from Inshorts. It parses the html to produce dictionaries that are then 
    converted to a larger dataframe containing the category, title, content, author, and published date of the article. 
    '''
    categories = ['business', 'sports', 'entertainment', 'technology']
    articles = []

    for category in categories:
        print(f'getting articles for {category}')
        category_articles = parse_inshorts_page(category)
        articles.extend(category_articles)
        
    return pd.DataFrame(articles)


def parse_inshorts_page(category):
    '''
    This function parses the html from Inshorts using an input category. It creates a list of dictionaries for each article and returns the list. 
    '''
    url = 'http://www.inshorts.com/en/read/' + category
    response = get(url)
    soup = BeautifulSoup(response.text)
    articles = [parse_news_card(card, category) for card in soup.select('.news-card')]
    return articles