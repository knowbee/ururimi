"""
Author: Igwaneza Bruce <knowbeeinc@gmail.com>
Attempt to collect all kinyarwanda words with english translations from kinyarwanda dictionary,
Source: kinyarwanda.net
"""


from bs4 import BeautifulSoup as bsf
from urllib.request import urlopen
from tqdm import tqdm
import time
import json
link = "http://kinyarwanda.net/index.php?q=%2A&start="
amagambo = {}
inshinga = []


def app():
    return scrape(link, amagambo)


def scrape(t, f):
    start = 6168
    end = 0
    try:
        with open("amagambo.json", "r") as f:
            file = json.load(f)
            if (len(file) > 0):
                while(end < start):
                    try:
                        with urlopen(t + str(start), data=None, timeout=1000) as page:
                            soup = bsf(page, 'html.parser')
                            words = soup.findAll(
                                "li", attrs={"class": "entry"})
                            with tqdm(total=len(inshinga)) as pbar:
                                for title in words:
                                    pbar.update(len(inshinga) / 0.1)
                                    pbar.desc = 'scraping'
                                    w_class = f"{title.find('a', attrs={'class': 'wordclass'}).text}"
                                    ref = f"{title.find('a', attrs={'class': 'reference'}).text}"
                                    # inshinga.append(ref)
                                    if(w_class == "v"):
                                        inshinga.append(ref)

                        start -= 10

                    except AttributeError:
                        print("not found")
                    finally:
                        start -= 10
                        print(start)
                        with open('inshinga.json', 'w') as file:
                            json.dump(inshinga, file)
            else:
                while(start < end):
                    try:
                        with urlopen(t + str(start), data=None, timeout=1000) as page:
                            soup = bsf(page, 'html.parser')
                            words = soup.findAll(
                                "li", attrs={"class": "entry"})
                            with tqdm(total=len(f)) as pbar:
                                for title in words:
                                    # time.sleep(0.1)
                                    pbar.update(len(f) / 0.1)
                                    pbar.desc = 'scraping'
                                    prefix = f"{title.find('span', attrs={'class': 'prefix'}).text}"
                                    lemma = f"{title.find('span', attrs={'class': 'lemma'}).text}"
                                    modifier = f"({title.find('span', attrs={'class': 'modifier'}).text})"
                                    meaning = f"{title.find('span', attrs={'class': 'meaning'}).text}"
                                    ijambo = prefix + lemma + modifier
                                    f.update(
                                        {ijambo: meaning})

                            start += 10
                    except AttributeError:
                        for title in words:
                            try:
                                prefix = f"{title.find('span', attrs={'class': 'prefix'}).text}"
                            except AttributeError:
                                prefix = ""
                            lemma = title.find(
                                "span", attrs={"class": "lemma"}).text
                            meaning = title.find(
                                "span", attrs={"class": "meaning"}).text
                            f.update({prefix + lemma: meaning})

                        start += 10
                    finally:
                        with open('amagambo.json', 'w') as file:
                            json.dump(f, file)
                        print(f"{len(f)}")
    except FileNotFoundError:
        pass
