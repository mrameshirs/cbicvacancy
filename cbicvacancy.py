# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 15:37:18 2022

@author: hp
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import time
import requests
import json
import moment
import xlrd

import math
import datetime 
import pandas as pd
import telegram

#import python-telegram-bot
from selenium import webdriver
import chromedriver_autoinstaller
from pymongo import MongoClient
from datetime import datetime


def sendmsg(msg):
    bot=telegram.Bot(token='5322151248:AAEqSMzZrgGYGFpNlbPUP-wOGePS4gLxbC8')
    bot.send_message(chat_id='@cbicvacancy',text=msg,parse_mode='MarkDown')
  



def main():   
    while True:
        #time.sleep(60*60*2)
        time.sleep(5)
        # datetime object containing current date and time
        now = datetime.now()
         
        print("now =", now)

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("date and time =", dt_string)	

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

        #chrome_options = Options()
        # chrome_options.add_argument("download.default_directory=/home/kannan2/virtualenvironment/twitter/scripts/excels/")
        #chrome_options.add_argument("--user-data-dir=chrome-data")
        
        url="https://www.cbic.gov.in/htdocs-cbec/deptt_offcr/vacancy_circ" 
        
        #browser = webdriver.Chrome(chromedriver_autoinstaller.install())
        browser.get(url);
        
        dfs = pd.read_html(url)
        df_new=dfs[1]
        df_top_new=df_new[:10]
        df_top_new['Full text']=df_top_new['Date of Uploading']+df_top_new['Brief Description']
        
        
        
        #_______________
        
        df_new['Status']='Exists'
        
        
        
        
        
        
        client=MongoClient("mongodb://mrameshirs:StaleMate@rjd-shard-00-00.czntg.mongodb.net:27017,rjd-shard-00-01.czntg.mongodb.net:27017,rjd-shard-00-02.czntg.mongodb.net:27017/?ssl=true&replicaSet=atlas-7dvvwj-shard-0&authSource=admin&retryWrites=true&w=majority")
        db=client.get_database('CBIC')
        records=db.vacancy
        count=records.count_documents({})
        lst=list(records.find({}).sort("_id",-1).limit(10))
        df_old=pd.DataFrame.from_dict(lst)
        df_old['Full text']=df_old['Date of Uploading']+df_old['Brief Description']
        
        #_______COMPARE TWO DFs
        temp=df_top_new[~df_top_new['Full text'].isin(df_old['Full text'].values.tolist())]
        temp['Status']="Exists"
        diff_df=temp.iloc[:,[0,1,3]]
        new_index=diff_df.index.tolist()
        print('New Items:',len(new_index))
        
        print('Every 2 hours Update:',dt_string,': New Items:-',len(new_index))
        sendmsg('Every 2 hours Update:'+str(dt_string)+': *New Items: '+str(len(new_index))+'*')
        if len(new_index)!=0:
            #_______PUSH NEW ROWS TO MONGODB
            records.insert_many(diff_df.to_dict('records'))
            
            #_______EXTRACT URLS OF NEW ROWS
            for i in new_index:
                
                
                column=browser.find_elements("xpath",'//*[@id="id1"]/tbody/tr['+str(i+1)+']/td[2]/a')
                #print(column[0].text)
                #print(column[0].get_attribute('href'))
                for col in column:
                    print(diff_df.iloc[i][0])
                    sendmsg(diff_df.iloc[i][0])
                    print(col.text)
                    sendmsg(col.text)
                    print(col.get_attribute('href'))
                    sendmsg(col.get_attribute('href'))
                      
            #_______Send telegram message

if __name__ == '__main__':
    main()
