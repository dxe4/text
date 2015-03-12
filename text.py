import requests
from bs4 import BeautifulSoup
import re
from collections import defaultdict
# http://www.cs.duke.edu/courses/spring14/compsci290/assignments/lab02.html


def get_html(url):
    result = requests.get(url)
    if result.status_code != 200:
        raise Exception('Got status code {}'.format(result.status_code))
    else:
        return result.text

url = 'http://en.wikipedia.org/wiki/Georg_Cantor'
html = get_html(url)
soup = BeautifulSoup(html)
links = soup.select('a[title]')

# This is the first sentence of each page,
# usually the most descriptive part
short_descreption_html = soup.select('p')[0]
description = short_descreption_html.getText()
# clean up
description = re.sub('(\[[^\]]+\])', '', description)


def should_exclude_link(link):
    title = link.attrs.get('title', '').lower()
    title_stopwords = [
        'wikipedia:', 'wikimedia:', 'Category:',
    ]
    attr_stopwords = ['lang', 'action', 'accesskey']
    # TODO Most of those exist in robots.txt
    href_stopwords = [
        '/wiki/Category:', '/w/index.php', '/wiki/Wikipedia:Community_portal',
        'https://donate.wikimedia.org', '/wiki/Main_Page', '/wiki/Help:',
        '/wiki/Portal:', '/wiki/Wikipedia:', '//shop.wikimedia.org',
        '//en.wikiquote.org', '//commons.wikimedia.org', '#',
        '/wiki/Special:'
    ]

    for stopword in attr_stopwords:
        if stopword in link.attrs:
            return True

    for stopword in href_stopwords:
        if link.attrs['href'].startswith(stopword):
            return True

    if title:
        for stopword in title_stopwords:
            if title.startswith(stopword):
                return True

    return False


def link_result():
    return (0, set())

link_dict = defaultdict(link_result)

for link in links:
    if should_exclude_link(link):
        continue
    else:
        title = link.attrs['title']
        href = link.attrs['href']
        count, titles = link_dict[href]
        titles.add(title)
        link_dict[href] = (count+1, titles)

page = {
    'short_description': description,
    'links': link_dict,
    'url': url
}
