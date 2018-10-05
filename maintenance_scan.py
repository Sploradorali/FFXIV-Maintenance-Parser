import re

from bs4 import BeautifulSoup
from requests import get
from requests.exceptions import RequestException

'''

Returns maintenance times for Final Fantasy XIV by parsing HTML from the Lodestone news pages

'''

root = 'https://na.finalfantasyxiv.com'
maintenance_page_url = root + '/lodestone/news/category/2'

'''
Regex for typical date/time format
Mon. dd, yyyy hh:mm a.m./p.m. to hh:mm a.m./p.m.
Mon. dd, yyyy hh:mm a.m./p.m. to Mon. dd, yyyy hh:mm a.m./p.m.
Mon. dd, yyyy hh:mm a.m./p.m.
'''
date_regex = re.compile('(([A-Z][a-z]{2}\.) ([1-9]{1,2}), \d{4} ([0-1]?\d:\d{2}) (a\.m\.|p\.m\.)'
                        '( to (([A-Z][a-z]{2}\.) ([1-9]{1,2}), \d{4} )?([0-1]?\d:\d{2}) (a\.m\.|p\.m\.))?)')
maintenance_page = None

# Requests HTML from page
try:
    maintenance_page = get(maintenance_page_url)
except RequestException as ex:
    print(str(ex) + ": Error requesting " + maintenance_page_url)

if maintenance_page is not None:
    maintenance_page_soup = BeautifulSoup(maintenance_page.text, 'html.parser')
    maintenance_article = maintenance_page_soup.find_all('a', attrs={'class': 'ic__maintenance--list'})

    # List to store links
    link_list = []

    # Loops through each page list item and picks out those with the [Maintenance] tag
    for article in maintenance_article:
        for tag in article.find_all('span', attrs={'class': 'news__list--tag'}):
            if tag.text == '[Maintenance]':
                for title in article.find_all('p', attrs={'class': 'news__list--title'}):
                    print(title.text)
                print(root + article['href'])
                link_list.append(root + article['href'])

    # Loops through the link on each page list item and parses for the maintenance date
    for i, link in enumerate(link_list):
        article_page = get(link)
        article_page_soup = BeautifulSoup(article_page.text, 'html.parser')
        body_divs = article_page_soup.find_all('div', attrs={'class': 'news__detail__wrapper'})
        for body_div in body_divs:
            date_text = None
            if len(date_regex.findall(body_div.text)) > 0:
                print(date_regex.findall(body_div.text)[0][0])
            else:
                print('No date found')
