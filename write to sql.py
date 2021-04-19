# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 14:25:00 2021

@author: jr
"""
# Imports
import json
import os
import pymysql
from pymysql.cursors import DictCursor

# General 
directory = os.path.join("c:\\","path")
mypath = os.getcwd()
json_files = []
host = 'localhost' #input localhost
user = 'root' # input root
password = '' # input password
db='base' # input basename


def add(job_title, country, city, job_description):
    """ Function for adding info to DB """
    connection = pymysql.connect(host=host,user=user, password=password, db=db, charset='utf8mb4', cursorclass=DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO jobs ('job_title', 'country', 'city', 'job_description') VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (job_title, country, city, job_description))
        connection.commit()
    finally:
        connection.close()


# General loop
for root,dirs,files in os.walk(mypath):
    for file in files:       
        if file.endswith(".json"):
           json_files.append(file)
           with open(file) as f:
               row = json.load(f)
               add(row['job_title'], row['country'], row['city'], row['job_description'])