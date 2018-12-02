import urllib.request
import re
from bs4 import BeautifulSoup

psych_url = 'https://psychusa.fandom.com/wiki/List_of_Gus%27_Nicknames'

class URLParser:
    def __init__(self, url=psych_url):
        self.url = url
        self.page = None

    def open(self):
        """
        Opens the url
        :return: url object
        """
        self.page = urllib.request.urlopen(self.url)
        return self.page

    def read(self):
        """
        Prints data from url
        :return: None
        """
        print(self.page.read().decode('utf-8'))

    def names(self):
        soup = BeautifulSoup(self.page, 'html.parser')
        div = soup.find("div", {"id": "mw-content-text"}).parent
        info = div.find_all('ul')
        seasons = [season.text.split("\n")[:-1] for season in info[:-2]]
        names = []

        p1 = re.compile('[/;,]+\s*')
        p2 = re.compile('^[^(]*')

        for season in seasons:
            for name in season:
                words = name.replace("\xa0", " ")
                words = words.split(" - ")[0]

                words = re.split(p1, words)
                for word in words:
                    if word != '':
                        names.append(re.search(p2, word).group(0))

        return names

if __name__ == '__main__':
    data = URLParser()
    data.open()
    #data.read()
    data.names()