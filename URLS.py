#### Generates URLS in file name output.txt and use that urls in the file for running scrapping script.

import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import NavigableString
import json
import ast
import pandas as pd

browser = webdriver.Firefox()
with open('text.txt','r') as f:
    for line in f:
        url = line.strip()
        with open('output.txt', 'a') as file:  # Use file to refer to the file object
            file.write(url+"\n")
        browser.get(url)
        # save html of the web page
        html_text = browser.page_source
        # make a soup out of html
        soup = BeautifulSoup(html_text, 'lxml')
        urls = soup.find_all("div", {"class": "col-l-4 mtop pagination-number"})
        No_of_pages = urls[0].find_all("b")
        No_of_pages = int(No_of_pages[1].get_text())
        for i in range(2,No_of_pages+1):
            with open('output.txt', 'a') as file:
                file.write("".join([url,"?page={}\n".format(i)]))
