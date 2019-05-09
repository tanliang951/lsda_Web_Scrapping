#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 16:56:46 2018

@author: air
"""

import requests
import csv
import json

#This part of global variables is for users' definition.
PAGE_URL = "http://www.lsdag.com/COMMON/ajax/Ajax.ashx?obj=Lsda&type=LsdaSearch&mulu=03"
CSV_FILE_NAME = "lsda2_"
CSV_TITLE = ["档号", "官职爵位A", "责任者A", "题名", "原纪年"]
NUM_PER_PAGE = 10000
MAX_COUNT_PER_CSV = 100000

def main():
     global CSV_FILE_NAME, NUM_PER_PAGE, MAX_COUNT_PER_CSV
     print("Data collection starts.")
     page = 1
     while True:
         lst_data = get_data(page)
         if not lst_data:
             break
         write_title = False
         if page % (MAX_COUNT_PER_CSV // NUM_PER_PAGE) == 1:
             write_title = True
         csv_no = page * NUM_PER_PAGE // MAX_COUNT_PER_CSV + (0 if page % (MAX_COUNT_PER_CSV // NUM_PER_PAGE) == 0 else 1)
         csv_file_name = CSV_FILE_NAME + str(csv_no) + ".csv"
         save_csv(lst_data, csv_file_name, write_title)
         page += 1
     print("Data collection finished.")
         
def get_data(page):
    global PAGE_URL, NUM_PER_PAGE
    print("Page %d, %d entries per page" % (page, NUM_PER_PAGE))
    url = PAGE_URL + "&curr=" + str(page) + "&numPerPage=" + str(NUM_PER_PAGE)
    try:
        response = requests.get(url)
        text = response.text
        lst_data = json.loads(text)
    except Exception as e:
        print(e)
        lst_data = []
    return lst_data

def save_csv(lst_data, csv_file_name, write_title):
    global CSV_TITLE
    if not lst_data:
        return
    #Here path is for users' own definition.
    path = "/Users/air/Desktop/lsda/" + csv_file_name
    with open(path, "a", encoding="GB18030", newline="") as file:
        if write_title:
            csv.writer(file).writerow(CSV_TITLE)
        for data in lst_data:
            
            sn = data.get("sn")
            """if not sn:
                sn = """""
            
            guanzhi = data.get("guanzhi")
            """if not guanzhi:
                guanzhi = """""
            
            zerenzhe = data.get("zerenzhe")
            """if not zerenzhe:
                zerenzhe = """""
            
            title = data.get("title")
            """if not title:
                title = """""
                
            yuanjinian = data.get("yuanjinian")
            """if not yuanjinian:
                yuanjinian = """""
            csv.writer(file).writerow([sn, guanzhi, zerenzhe, title, yuanjinian])
            
if __name__ == '__main__':
    main()