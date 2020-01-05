from bs4 import BeautifulSoup as bsf
from urllib.request import urlopen
from tqdm import tqdm  # progress bar library
import time
import json
link = "http://kinyarwanda.net/index.php?q=%2A&start="
amagambo = {}


def app():
    return scrape(link, amagambo)


def scrape(t, f):
    start = 0
    while(start < 10):
        with urlopen(t + str(start), data=None, timeout=1000) as page:
            soup = bsf(page, 'html.parser')
            words = soup.findAll("li", attrs={"class": "entry"})
            with tqdm(total=len(f)) as pbar:
                for title in words:
                    time.sleep(0.1)
                    pbar.update(5)
                    pbar.desc = 'scraping'
                    print(title.find("span", attrs={"class": "meaning"}).text)
                    f.update({title.find("span", attrs={"class": "lemma"}).text: title.find(
                        "span", attrs={"class": "meaning"}).text})
            start += 10
    print(start)
    print(f)
    print(f"'size': {len(f)}")
    # with open('amagambo.json', 'w') as file:
    #     json.dump(f, file)
