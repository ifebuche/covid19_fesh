from bs4 import BeautifulSoup
import requests
from selenium import webdriver 
import pandas as pd
from datetime import datetime
from time import sleep

#date object and string from it to use as files name for order
dateTimeObj = datetime.now()
timestampStr = dateTimeObj.strftime("%d-%b-%Y")

url = 'https://www.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61'

#Make a chrome browser
browser = webdriver.Chrome('chromedriver.exe')

#Load the url and wait 10 seconds to finish populating dynamically
print("We will load the url and hold for some seconds to ensure the page fully loads")
browser.get(url)
sleep(3)

#Grab the needed page source and close the browser
res = browser.page_source
browser.close()

print("Info retrieved from the site.\nDoing the job ...")
sleep(2)
#Parse the load
info = BeautifulSoup(res,'html.parser') 

#Get the Worldwide figures at the nav item
nav = info.find_all('nav', {'class':'feature-list'})

print("Attempting to create and save the tables...")
sleep(2)
try:
    for item in nav[:1]:
        holder = item.text.strip()
        #print(x)

    #cleanup the result  
    list_container = holder.replace('\xa0 \xa0', '|').replace('\n', ' ').split()  


    #Organise into two lists of country and totals
    country = []
    total = []
    incrementer = 1

    for i, item in enumerate(list_container):
        x = item.split('|')
        if len(x) > 1:
            country.append(x[1].replace(',', ''))
            total.append(x[0])
        else:
            country[i-incrementer] = country[i-incrementer] + ' ' + item #take the last item in country and concat to it as it is the latter part of it
            incrementer += 1

    #Confirm len of both arrays and if true, make a df
    if len(country) == len(total):
        #make a dataframe
        cases = {}
        for cont, tot in zip(country, total):
            cases[cont] = [int(tot.replace(',',''))]
        cases
        df = pd.DataFrame(cases)

        #drop a quick bar plot of the top ten
        # df.T.head(10).plot(kind='bar', figsize=(19,5))

        #Tranpost table, reset index and change col names
        df1 = df.T.reset_index()
        df1.columns = ['Country', 'Count']

        #save to file
        namer = timestampStr
        df.to_csv('data\\' + namer + '.csv', index=False)

    #Get and save data for US
    for item in nav[1:2]:
        holder_us = item.text.strip()

    #clean out the list   
    list_container_us = holder_us.replace('\xa0 \xa0', '|').replace('\n', ' ').split()  

    #initialize empty lists to hold items
    state = []
    confirmed = []
    dead = []

    for i, item in enumerate(list_container_us):
        x = item.split('|')
        if len(x) > 1: #if it is more than one, the first is total and second is state
            state.append(x[1])
            confirmed.append(x[0])
        else:
            try:
                died = int(item.replace('(','').replace(')',''))#will work for dead count:they have braces
                dead.append(died)
            except:
                state[-1] = state[-1] + ' ' + item #Get last item in country and concat to it as it is the latter part of it            

    # confirm matching length and make df and save to file
    if len(state) == len(confirmed) == len(dead):
        df_us = pd.DataFrame()

        df_us['state'] = state
        df_us['confirmed'] = [int(i.replace(',','')) for i in confirmed]
        df_us['dead'] = dead

        #save to file
        namer = timestampStr + '_us'
        df_us.to_csv('data\\' + namer + '.csv', index=False)
        print("Successfully!\nCheck the data folder for your files.")
except Exception as e:
    print("We hit a snag! See details below.\n{}".format(e))