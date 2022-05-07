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
    sleep(30)
    clear()

    #Grab the needed page source and close the browser
    res = browser.page_source
    browser.close()

    print("Info retrieved from the site.\nDoing the job ...")
    sleep(2)
    #Parse the load
    info = BeautifulSoup(res,'html.parser') 

    #Get the Worldwide figures at the nav item
    country_list = info.find_all('div', {'class': "flex-auto list-item-content overflow-hidden"})

    covid = {}
    doses = {}
    try:
        for country in country_list:
            try:
                holder = country.text.replace('\n', ' ').replace('\xa0', '').strip().split(':')
                country_name = holder[0].replace(' In the Past 28 Days', '')
                past28_0 = int(holder[1].split('|')[0].replace(',', '').strip())
                past28_1 = int(holder[1].split('|')[-1].replace(' Totals', '').replace(',', ''))
                totals0 = int(holder[2].split('|')[0].replace(',', '').strip())
                totals1 = int(holder[2].split('|')[-1].replace(' Total Incidence Rate', '').replace(',', ''))
                rate_ = holder[3].split('people')[0]
                covid[country_name] = {
                    'in the past 28 red': past28_0,
                    'in the past 28 white': past28_1,
                    'totals red': totals0,
                    'totals white': totals1,
                    'rate': rate_
                }
            except IndexError: #We get into doses section
                holder = country.text.split()
                country_name = holder[0]
                doses_per_100k = holder[1]
                total_doses = holder[6]
                doses[country_name] = {
                    'does per 100k': doses_per_100k,
                    'total doses': total_doses
                }

        covid_df = pd.DataFrame(covid).T.reset_index()
        covid_df.columns = ['Country', 'in the past 28 red', 'in the past 28 white', 'totals red', 'totals white', 'rate']
        doses_df = pd.DataFrame(doses).T.reset_index()
        doses_df.columns = ['Country', 'does per 100k', 'total doses']

        try:
            os.makedirs('data')
            print("We just made a 'Data' folder as it didn't exist before")
        except:
            print("The folder exists!")
            sleep(3)
        timestampStr = d_time()
        covid_df.to_csv('data\\' + 'JHU_' + timestampStr + '_covid_cases' + '.csv', index=False)
        print("World Data written to data folder.\n")
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
        print(f"\nThe current covid-19 global death rate according to this data is ~{df.death_rate.mean():.2f}")
        print(f"\nThe current covid-19 global death rate according to this data is ~{df.recovery_rate.mean():.2f}")

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
    line1.insert(0, line)
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
miss = []
countries_x = []
for line in countries:
    line = line.lower()
    x = line.split()
    if len(x) == 1:
        countries_x.append(line)
    elif len(x) == 2:
        countries_x.append(x[0].replace('.', '') + '-' + x[1].replace('(', '').replace(')', ''))
    elif len(x) == 3:
        countries_x.append(x[0].replace('.', '') + '-' + x[1] + '-' + x[2])
    elif len(x) == 4:
        countries_x.append(x[0].replace('.', '') + '-' + x[1] + '-' + x[2] + '-' + x[3])
    else:
        miss.append(line)

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

x = d_time()
with open('data\\' +'failed_' + x + '.txt', 'a') as failures:
    
    for line in failed:
        failures.write(line + '\n')
combo = pd.concat(chai).reset_index(drop=True)
timestampStr = d_time()
combo.to_csv('data\\' + 'worldwide_' + timestampStr + '.csv', index=False)