from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd 
import os

#Get current location of the script
cwd = os.getcwd()

#Ask the user for the fbref url of the match
url = input("Enter url of the match [frebf]: ")

# Setup the Selenium webdriver to open the url in a icognito Chrome window
browser = webdriver.ChromeOptions()
browser.add_argument('--ignore-certificate-errors')
browser.add_argument('--incognito')
browser.add_argument('--headless')

#Location of the chromedriver executable to open the browser
driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver.exe", options=browser)

print("Opening browser...")
#The driver will wait until the webpage is loaded, it will maximize it and finally get the url given by the user
driver.implicitly_wait(5)
driver.maximize_window()
driver.get(url)

#The url is cut in order to get the information of the match
matchInfo = url[38:]

# Directory
directory = matchInfo
  
# Parent Directory path
parent_dir = cwd + "/Directory/UEFA-Euro-2020/Matches/"
  
# Path
path = os.path.join(parent_dir, directory)

#Creation of the folder to save the information in
if(os.path.exists(path) == False):
  os.mkdir(path)
  print('Creating new folder named: ' + directory)

#Opening the path to the match list .csv
matchListPath = cwd + "/Directory/UEFA-Euro-2020/"

#Taking away the information of the match through the url
matchInfo = matchInfo.split('-')

localTeamName = matchInfo[0]
awayTeamName = matchInfo[1]
date = matchInfo[2]+'-'+matchInfo[3]+'-'+matchInfo[4]
competition = matchInfo[5] + " " + matchInfo[6]

#Adding the match to a list .csv
print('Adding match to the list...')
matchList = pd.read_csv(matchListPath + 'MatchList.csv')
new_row = {'Url': url, 'LocalTeam': localTeamName, 'AwayTeam': awayTeamName, 'Date': date, 'Competition': competition}
matchList = matchList.append(new_row, ignore_index=True)
matchList.to_csv(matchListPath + 'MatchList.csv')
print('Match added to the list!')

#Finding the id of the teams in order to find their stats, this by using Selenium
#Using the local team name to find the link with the id
localTeam = driver.find_element_by_link_text(localTeamName)

#Taking the id out of the hyperlink in their attributes
localTeamId = localTeam.get_attribute('href')
localTeamId = localTeamId[28:36]

#Using the away team name to find the link with the id
awayTeam = driver.find_element_by_link_text(awayTeamName)

#Taking the id out of the hyperlink in their attributes
awayTeamId = awayTeam.get_attribute('href')
awayTeamId = awayTeamId[28:36]

#Finding the buttons that get the information to .csv
more_buttons = driver.find_elements_by_class_name("tooltip")


#Local Team Stats
#Clicking the different buttons to get the information into .csv
driver.execute_script("arguments[0].click(); arguments[1].click(); arguments[2].click(); arguments[3].click(); arguments[4].click(); arguments[5].click();", more_buttons[3], more_buttons[13], more_buttons[22], more_buttons[31], more_buttons[40], more_buttons[49])

#Loading the page after clicking the buttons
page_source = driver.page_source

#Using BeautifulSoup to find the different stats of the teams with their id and creating a new .csv file with the information
soup = BeautifulSoup(page_source, 'lxml')

print('Getting information from the local team...')
LocalGeneral = soup.find("pre", {"id": "csv_stats_"+ localTeamId +"_summary"})

text_file = open(path + "/" + localTeamName + "GeneralStats" + "vs" + awayTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(LocalGeneral.text)
text_file.close()

LocalPassing = soup.find("pre", {"id": "csv_stats_"+ localTeamId +"_passing"}) 

text_file = open(path + "/" + localTeamName + "PassingStats" + "vs" + awayTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(LocalPassing.text)
text_file.close()

LocalPassingType = soup.find("pre", {"id": "csv_stats_"+ localTeamId +"_passing_types"}) 

text_file = open(path + "/" + localTeamName + "PassingTypeStats" + "vs" + awayTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(LocalPassingType.text)
text_file.close()

LocalDefending = soup.find("pre", {"id": "csv_stats_"+ localTeamId +"_defense"}) 

text_file = open(path + "/" + localTeamName + "DefenseStats" + "vs" + awayTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(LocalDefending.text)
text_file.close()

LocalPossession = soup.find("pre", {"id": "csv_stats_"+ localTeamId +"_possession"}) 

text_file = open(path + "/" + localTeamName + "PossessionStats" + "vs" + awayTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(LocalPossession.text)
text_file.close()

LocalMisc = soup.find("pre", {"id": "csv_stats_"+ localTeamId +"_misc"}) 

text_file = open(path + "/" + localTeamName + "MiscStats" + "vs" + awayTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(LocalMisc.text)
text_file.close()
print('Local team information completed!')

#Away Team Stats
#Clicking the different buttons to get the information into .csv
driver.execute_script("arguments[0].click(); arguments[1].click(); arguments[2].click(); arguments[3].click(); arguments[4].click(); arguments[5].click();", more_buttons[68], more_buttons[78], more_buttons[87], more_buttons[96], more_buttons[105], more_buttons[114])

#Loading the page after clicking the buttons
page_source = driver.page_source

#Using BeautifulSoup to find the different stats of the teams with their id and creating a new .csv file with the information
soup = BeautifulSoup(page_source, 'lxml')

print('Getting information from the away team...')
AwayGeneral = soup.find("pre", {"id": "csv_stats_"+ awayTeamId +"_summary"})

text_file = open(path + "/" + awayTeamName + "GeneralStats" + "vs" + localTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(AwayGeneral.text)
text_file.close()

AwayPassing = soup.find("pre", {"id": "csv_stats_"+ awayTeamId +"_passing"}) 

text_file = open(path + "/" + awayTeamName + "PassingStats" + "vs" + localTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(AwayPassing.text)
text_file.close()

AwayPassingType = soup.find("pre", {"id": "csv_stats_"+ awayTeamId +"_passing_types"}) 

text_file = open(path + "/" + awayTeamName + "PassingTypeStats" + "vs" + localTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(AwayPassingType.text)
text_file.close()

AwayDefending = soup.find("pre", {"id": "csv_stats_"+ awayTeamId +"_defense"}) 

text_file = open(path + "/" + awayTeamName + "DefenseStats" + "vs" + localTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(AwayDefending.text)
text_file.close()

AwayPossession = soup.find("pre", {"id": "csv_stats_"+ awayTeamId +"_possession"}) 

text_file = open(path + "/" + awayTeamName + "PossessionStats" + "vs" + localTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(AwayPossession.text)
text_file.close()

AwayMisc = soup.find("pre", {"id": "csv_stats_"+ awayTeamId +"_misc"}) 

text_file = open(path + "/" + awayTeamName + "MiscStats" + "vs" + localTeamName + ".csv", "w", encoding='utf-8')
n = text_file.write(AwayMisc.text)
text_file.close()
print('Away team information completed!')

#Closing the driver
driver.quit
print('Scraping completed!')