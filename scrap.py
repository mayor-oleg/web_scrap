# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 22:23:28 2021

@author: jr
"""

# Imports
import requests
import re
from bs4 import BeautifulSoup
import unidecode
import json


# Getting row data
url = 'https://www.allot.com/careers/careers-page/' 
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
job_title_temp = soup.find_all('div', class_='position-name')
country_temp = soup.find_all('div', class_='position-location')
city_temp = soup.find_all('div', class_='position-location')
job_description_temp = soup.find_all('a', class_='position wow fadeIn')

# Next 4 function for cleaning data
def clean_job_title(item):
    print ('Collection data of job title...')
    item_done = []
    for el in item:
        item_done.append(el.text)
    print ('DONE')    
    return item_done

def clean_country(item):
    print ('Collection data of country...')
    item_done = []
    for num in range(len(item)):
        item[num] = item[num].text
        item[num] = re.sub('\s+', '', item[num])
        item_done.append(item[num].split(',')[1])
    print ('DONE')
    return   item_done

def clean_city (item):
    print ('Collection data of city...')
    item_done = []
    for num in range(len(item)):
        item[num] = item[num].text
        item[num] = re.sub('\s+', '', item[num])
        item_done.append(item[num].split(',')[0])
    print ('DONE')
    return   item_done

def clean_job_description(item):
    print ('Collection data of job description...')
    item_done = []
    for el in item:
        response = requests.get(el.get('href'))
        soup = BeautifulSoup(response.text, 'lxml')
        job_desc = soup.find('div', class_='position-description').get_text(separator=' ')[18:-18]
        job_desc = unidecode.unidecode(job_desc)
        item_done.append([job_desc.strip()])
    print ('DONE')
    return item_done

# Getting clean data
job_title = clean_job_title(job_title_temp)
country = clean_country(country_temp)
city = clean_city(city_temp)
job_description = clean_job_description(job_description_temp)

# Creating and saving jsons files
output_dict = {}
for num in range(len(job_title)):
    print ('Creating json of', job_title[num]) 
    output_dict = {'job_title': job_title[num],
                   'country' : country[num],
                   'city' : city[num],
                   'job_description' : job_description[num]}
    if '/' in job_title[num]:
        jt = job_title[num].replace('/', 'or')
    else:
        jt = job_title[num]
    with open(jt+'.json', 'w') as fp:
        json.dump(output_dict, fp)
    print ("DONE")      