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


def app():
    return scrape(link, amagambo)


def scrape(t, f):
    start = 0
    end = 20
    while(start < end):
        try:
            with urlopen(t + str(start), data=None, timeout=1000) as page:
                soup = bsf(page, 'html.parser')
                words = soup.findAll("li", attrs={"class": "entry"})
                with tqdm(total=len(f)) as pbar:
                    for title in words:
                        time.sleep(0.1)
                        pbar.update(5)
                        pbar.desc = 'scraping'
                        f.update({title.find("span", attrs={"class": "lemma"}).text: title.find(
                            "span", attrs={"class": "meaning"}).text})
                start += 10
        except ConnectionResetError:
            pass
        finally:
            print(f"'size': {len(f)}")
            with open('amagambo.json', 'w') as file:
                json.dump(f, file)
