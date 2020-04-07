from bs4 import BeautifulSoup
import requests, os
from selenium import webdriver 
import pandas as pd
from datetime import datetime
from time import sleep

#date object and string from it to use as files name for order
def d_time():
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y %H-%M-%S")

    return timestampStr

# define our clear function 
def clear(): 
    """
    For a neat console, clear console depending on the os.  
    """
    # for windows 
    if os.name == 'nt': 
        _ = os.system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = os.system('clear') 

def arcGis():
    """
    Scrape JHU covid data from the ArcGIS site.
    """
    url = 'https://www.arcgis.com/apps/opsdashboard/index.html#/85320e2ea5424dfaaa75ae62e5c06e61'

    #Make a chrome browser
    browser = webdriver.Chrome('chromedriver.exe')

    #Load the url and wait 10 seconds to finish populating dynamically
    print("We will load the url and hold for some seconds to ensure the page fully loads")
    browser.get(url)
    sleep(10)
    clear()

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

            #save to file to data folder
            clear()
            print("We will be writing the data to a folder called 'Data'.\nLet's see if folder exists...")
            sleep(5)
            try:
                os.makedirs('data')
                print("We just made a 'Data' folder as it didn't exist before")
                #Save to data folder.
                timestampStr = d_time()
                df.to_csv('data\\' + 'JHU_' + timestampStr + '.csv', index=False)
                print("Data written to data folder.\n")
                sleep(5)
                clear()
            except:
                print("The folder exists!")
                sleep(2)
                timestampStr = d_time()
                df.to_csv('data\\' + 'JHU_' + timestampStr + '.csv', index=False)
                print("Data written to data folder.\n")
                sleep(5)
                clear()

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
                    died = int(item.replace('(','').replace(')','').replace(',', ''))#will work for dead count:they have braces
                    dead.append(died)
                except:
                    state[-1] = state[-1] + ' ' + item #Get last item in country and concat to it as it is the latter part of it            

        # confirm matching length and make df and save to file
        print("len state == len confirmed and dead")
        print(len(state) == len(confirmed) == len(dead))
        sleep(5)
        if len(state) == len(confirmed) == len(dead):
            df_us = pd.DataFrame()

            df_us['state'] = state
            df_us['confirmed'] = [int(i.replace(',','')) for i in confirmed]
            df_us['dead'] = dead

            rating = lambda x,y: round((x / y) * 100, 1)
            df_us['death_rate'] = rating(df_us['dead'], df_us['confirmed'])

            clear()
            print("We will be writing the data to a folder called 'Data'.\nLet's see if folder exists...")
            sleep(5)
            try:
                os.makedirs('data')
                print("We just made a 'Data' folder as it didn't exist before")
                #Save to data folder.
                timestampStr = d_time()
                df_us.to_csv('data\\' + 'JHU_' + timestampStr + '_us' + '.csv', index=False)
                print("Data written to data folder.\n")
                sleep(5)
                clear()
            except:
                print("The folder exists!")
                sleep(3)
                timestampStr = d_time()
                df_us.to_csv('data\\' + 'JHU_' + timestampStr + '_us' + '.csv', index=False)
                print("US Data written to data folder.\n")
                sleep(5)
                clear()
    except Exception as e:
        print("We hit a snag! See details below.\n{}\n\nData not retrieved".format(e))
        print("Attempting to Commence covid-19 global data by JHU from ArcGIS...")
        sleep(59)
        arcGis()
        clear()


def covidHelp():
    """
    Scrape data from covid.help website
    """
    #site address
    url = 'https://corona.help/#countries-nav'

    print("Reading the web page ...")
    #get the page with requests
    r = requests.get(url)

    #make into a bs4 four item to lend itself to html ta searching
    soup = BeautifulSoup(r.content, "lxml")

    #From eyeballing, 'td' tags hold our data of interest .find all td tags.
    tables = soup.find_all('td')

    #Get text of each line of 'tables' and strip whitespaces
    our_list = [line.text.strip() for line in tables]

    #From observation, each country, including its name, has 10 consecutive rows
    #Make arrays to match this order
    countries = our_list[::10] #step five places through lines to get countries.
    infected = our_list[1::10]
    infected_today = our_list[2::10]
    deaths = our_list[3::10]
    deaths_today = our_list[4::10]
    recovered = our_list[5::10]
    recovered_today = our_list[6::10]
    active = our_list[7::10]
    critical = our_list[8::10]
    tests = our_list[9::10]


    df = pd.DataFrame()
    df['countries'] = countries
    df['infected'] = [int(line.replace(',','')) for line in infected]
    df['infected_today'] = [int(line.replace(',','')) for line in infected_today]
    df['deaths'] = [int(line.replace(',','')) for line in deaths]
    df['deaths_today'] = [int(line.replace(',','')) for line in deaths_today]
    df['recovered'] = [int(line.replace(',','')) for line in recovered]
    df['recovered_today'] = [int(line.replace(',','')) for line in recovered_today]
    df['active'] = [int(line.replace(',','')) for line in active]
    df['critical'] = [int(line.replace(',','')) for line in critical]
    df['tests'] = [int(line.replace(',','')) for line in tests]

    clear()
    print("Calculating recovery and death rates...")
    sleep(3)
    #Rating calculator
    #Get rate of each event(recovery/death) relative to total occurences
    #Round to a single decimal place
    rating = lambda x,y: round((x / y) * 100, 1)

    #Add rates to df with rating ;lambda
    df['death_rate'] = rating(df['deaths'], df['infected'])
    df['recovery_rate'] = rating(df['recovered'], df['infected'])

    clear()
    print("We will be writing the data to a folder called 'Data'.\nLet's see if folder exists...")
    sleep(2)
    #Check if data foler exists, if not create one
    # if not os.path.exists('my_folder'):
    #     os.makedirs('my_folder')
    try:
        os.makedirs('data')
        clear()
        print("We just made a 'Data' folder as it didn't exist before")
        #Save to data folder.
        timestampStr = d_time()
        df.to_csv('data\\' + 'covid_help_data_' + timestampStr + '.csv', index=False)
        cur_path = os.getcwd()+'\\data'
        os.startfile(cur_path)
        clear()
        print("Data written to data folder.\nWe just opened the folder.")
        sleep(2)
        clear()
        print("\nThe current covid-19 global death rate according to this data is ~{}%".format(df.iloc[-1]['death_rate']))
    except:
        #Save to data folder.
        clear()
        print("The folder exists!")
        sleep(2)
        timestampStr = d_time()
        df.to_csv('data\\' + 'covid_help_data_' + timestampStr + '.csv', index=False)
        cur_path = os.getcwd()+'\\data'
        os.startfile(cur_path)
        clear()
        print("Data written to data folder.\nWe just opened the folder.")
        sleep(2)
        clear()
        print("\nThe current covid-19 global death rate according to this data is ~{}%".format(df.iloc[-1]['death_rate']))

    return countries #for use in the collecting country by country

def oya(line, prefix = 'https://corona.help/country/'):
    url = prefix + line
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'lxml')
    target = soup.find_all('div', {'class':'col-xl-2 col-md-4 col-sm-6'})

    line1 = []
    line2 = []

    for item in target:
        hold = item.text.strip().replace('\n', '|')
        x = hold.split('|')
        line1.append(x[0])
        line2.append(x[-2])
    line1.extend(line2)
    line1.insert(0, 'USA')
    count = line1

    df = pd.DataFrame()

    df['Country'] = [count[0]]
    df['Total confirmed'] = [count[1]]
    df['Total_confirmed_today'] = [count[7]]
    df['Total_deaths'] = [count[2]]
    df['Total_deaths_today'] = [count[8]]
    df['Total_Recoveries'] = [count[3]]
    df['Total_Recoveries_today'] = [count[9]]
    df['Active_confirmed'] = [count[4]]
    df['Critical'] = [count[10]]
    df['Mortality_close'] = [count[4]]
    df['Mortality_confirmed'] = [count[11]]
    df['Total_tests'] = [count[6]]
    df['Total_tests_today'] = [count[12]]
    return df

# def get_naija():
#     url = 'https://corona.help/country/nigeria'
#     r = requests.get(url)
#     soup = BeautifulSoup(r.content, 'lxml')
#     target = soup.find_all('div', {'class':'col-xl-2 col-md-4 col-sm-6'})

#     case = []
#     count = []

#     for item in target:
#         hold = item.text.strip().replace('\n', '|')
#         x = hold.split('|')
#         case.append(x[1])
#         count.append(x[0])

#     df = pd.DataFrame()
#     df['Cases'] = case
#     df['Count'] = count
    
#     #Save 
#     df.to_csv('data\\' + 'Naija.csv', index=False)

#Execution
print("Commencing covid-19 global data by JHU from ArcGIS...")
sleep(2)
arcGis()
clear()
print("Done!")

clear()
print("Commencing covid-19 global data from covid.help...")
sleep(2)
countries = covidHelp()
clear()
print("Done!")

#All countries
countries_x = []
for line in countries:
    line = line.lower()
    x = line.split()
    if len(x) == 1:
        countries_x.append(line)
    elif len(x) == 2:
        countries_x.append(x[0].replace('.', '') + '-' + x[1].replace('(', '').replace(')', ''))
    elif len(x) == 3:
        countries_x.append(x[0] + '-' + x[1] + '-' + x[2])

countries_x = countries_x[:-1]

#Execuation for all countries table
chai = []
failed = []
for line in countries_x:
    try:
        df = oya(line)
        chai.append(df)
    except:
        try:
            print("Failed at {}\nRetrying...".format(line))
            sleep(2)
            df = oya(line)
            chai.append(df)
        except:
            print("Gave up on {} after 2 tries, so ...".format(line))
            failed.append(line)
    print("{} done.".format(line))
    sleep(2)
    clear()

with open('data\\fail_log\\' +'failed_' + timestampStr + '.txt', 'a') as failures:
    for line in failed:
        failures.write(line + '\n')
combo = pd.concat(chai).reset_index(drop=True)
timestampStr = d_time()
combo.to_csv('data\\' + 'worldwide_' + timestampStr + '.csv', index=False)