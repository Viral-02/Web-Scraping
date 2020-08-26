import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from bs4 import NavigableString
import json
import ast
import pandas as pd

browser = webdriver.Firefox()
df = pd.DataFrame(columns = ['Id' , 'Name', 'Address' , 'Cuisine', 'Establishment', 'Cost', 'Ratings', 'Review_Count', 'latitude', 'longitude', 'outlet'])
with open('output.txt', 'r') as file:
    for line in file:
        stripped_line = line.strip()
        # url feed for selenium
        browser.get(stripped_line)
        # save html of the web page
        html_text = browser.page_source
        # make a soup out of html
        soup = BeautifulSoup(html_text, 'lxml')
        ids = []
        names = []
        addrs = []
        cuisines = []
        ests = []
        costs = []
        rating = []
        review_count = []
        lat = []
        long = []
        outlet = []
        res_names = soup.find_all('a', {"class" : "result-title hover_feedback zred bold ln24 fontsize0"})
        res_addrs = soup.find_all('div', {"class" : "col-m-16 search-result-address grey-text nowrap ln22"})
        res_cuisines = soup.find_all('span', {"class" : "col-s-11 col-m-12 nowrap pl0"})
        res_ests_ratings = soup.find_all('script')
        res_costs = soup.find_all('span', {"class" : "col-s-11 col-m-12 pl0"})
        st = "zomato.DailyMenuMap.mapData"

        for res_name in res_names:
            names.append(res_name.get_text().replace('\n',''))

        for res_addr in res_addrs:
            addrs.append(res_addr.get_text())

        for res_cuisine in res_cuisines:
            cuisines.append(res_cuisine.get_text())

        for res_ests in res_ests_ratings:
            if(st in str(res_ests)):
                for j in res_ests:
                    with open('data.txt', 'w') as outfile:
                        outfile.write(j)
                    with open('data.txt', 'r') as outfile:
                        lines = outfile.readlines()
                        d = lines[5].split("= ",1)
                        y = json.dumps(d[1],sort_keys=True)
                        y = y.replace('\\n', '')
                        y = y.replace('\\','')
                        p = y.replace("&quot;",'')
                        p = p.replace("\"","\'")
                        g = re.split("'\d{1,2}':",p)
                        str1 = "class='content'"

                        for i in range(0,len(g)):
                            if(re.search(str1,g[i])):
                                split_str = g[i].split(',',8)
                                ids.append((split_str[0]).split(":")[1].replace("'",''))
                                if(len((split_str[3]).split(":")[1]) == 0):
                                    rating.append("None")
                                else:
                                    rating.append((split_str[3]).split(":")[1])
                                if(len((split_str[6]).split(":")[1]) == 0):
                                    ests.append("None")
                                else:
                                    ests.append((split_str[6]).split(":")[1].replace("}",'').replace("'",''))
                                x = re.findall(r"(\((\d{1,},*\.*\d{1,}[kK]?))",g[i])
                                if(len(x) != 0):
                                    review_count.append(x[0][1].replace(",",''))
                                else:
                                    review_count.append(0)
                                lat.append((split_str[1]).split(":")[1])
                                long.append((split_str[2]).split(":")[1])
                                f = g[i].count(r"ui col-l-16 search_chain_bottom_snippet")
                                outlet.append(f)
                                cost = re.findall(r"Rs.\s\d{0,},*\d{1,}",g[i])
                                if(len(cost) != 0):
                                    costs.append(cost[0])
                                else:
                                    costs.append("Rs. 0")


        #print("Length of columns {} {} {} {} {} {} {} {} {} {} {}".format(len(ids),len(names),len(addrs),len(cuisines),len(ests),len(costs),len(rating),len(review_count), len(lat), len(long), len(outlet)))
        for k in range(0,len(ids)):
            df = df.append({'Id' : ids[k] , 'Name' : names[k] , 'Address' : addrs[k] , 'Cuisine' : cuisines[k] , 'Establishment' : ests[k] , 'Cost' : costs[k], 'Ratings' : rating[k], 'Review_Count' : review_count[k], 'latitude' : lat[k], 'longitude' : long[k], 'outlet' : outlet[k]} , ignore_index=True)
df.to_csv(r'File.csv')
