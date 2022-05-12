import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

## Blog Articles

def get_blog_article_urls():
    '''
    This function makes a request to the Codeup blog site and gathers the urls by analyzing the returned html text. Returns the list of urls.
    '''
    headers = {User-Agent: 'Codeup Data Science'}
    response = requests.get('https://codeup.com/blog/', headers=headers)
    soup = BeautifulSoup(response.text)
    # Getting the url by the a class subcategory 'more-link'
    urls = [a.attrs['href'] for a in soup.select('a.more-link')]
    return urls


def parse_blog_article(soup):
    '''
    This function parses each individual article to gather the title, content, and published date.
    '''
    return {
        'title': soup.select_one('h1.entry-title').text,
        'content': soup.select_one('.entry-content').text.strip(),
        'published': soup.select_one('.published').text
    }


def get_blog_articles():
    '''
    This function returns a dataframe of the articles from the Codeup blog site. 
    Inside the function the list of urls is used to gather the article's html and then parse it for title, content, and date published.
    '''
    urls = get_blog_article_urls()
    articles = []

    for url in urls:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text)
        articles.append(parse_blog_article(soup))

    df = pd.DataFrame(articles)
    return df


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