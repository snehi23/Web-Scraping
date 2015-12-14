__author__ = 'snehi23'

import urllib2
import bs4
from collections import OrderedDict
import json
import locale

# Code constants
LIST_OF_COUNTRIES_URL = 'http://bgp.he.net/report/world'
PER_COUNTRY_PART_URL = 'http://bgp.he.net'
URL_1_TABLE_ID = 'table_countries'
URL_2_TABLE_ID = 'asns'


# Call to Beautiful Soup API to get parse tree
# Input : url to scrape
# Return: parse tree of web page
def url_to_soup(url):

    req = urllib2.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    html = urllib2.urlopen(req).read()
    soup = bs4.BeautifulSoup(html,"lxml")
    return soup

# Get list of country code and link
def scrape_country_code_and_link():

    soup = url_to_soup(LIST_OF_COUNTRIES_URL)
    table_data = soup.find(id=URL_1_TABLE_ID)
    code_and_link = []

    for row in table_data:
        for column in row:
         anchor = column.find('a')
         if anchor is not -1 and anchor is not None:
            href = anchor['href']
            country_code = href.replace("/country/", "")
            country_link = PER_COUNTRY_PART_URL+href
            code_and_link.append((country_code, country_link))

    return code_and_link

# Get dictionary of required fields per country
# Input : code and link
# Return: dictionary of asn info per country
def scrape_per_country_info(code, link):

     soup = url_to_soup(link)
     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

     parent_dict = dict()

     table_data = soup.find(id=URL_2_TABLE_ID)

     if table_data is not None:

        for row in table_data:
         for column in row:
             anchor = column.find('a')
             if anchor is not -1 and anchor is not None:
                  ASN_CODE = anchor.string.replace("AS","")
                  info = column.findAll('td')
                  name = info[1].string
                  Routesv4 = info[3].string
                  Routesv6 = info[5].string

                  child_dict = OrderedDict()
                  child_dict['Country'] = str(code)

                  if name is not None:
                    child_dict['Name'] = name.encode("utf-8") # Fix for locale issue

                  child_dict['Routes v4'] = locale.atoi(Routesv4)
                  child_dict['Routes v6'] = locale.atoi(Routesv6)

                  parent_dict[locale.atoi(ASN_CODE)] = child_dict

     return parent_dict

if __name__ == '__main__':

     code_and_link = scrape_country_code_and_link()
     scrape_all_country = dict()

     for (code, link) in code_and_link:
         scrape_all_country.update(scrape_per_country_info(code,link))

     with open('asn.json','a') as f:
         json.dump(scrape_all_country,f)
