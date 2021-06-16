from datetime import date
import pandas as pd 
import matplotlib.pyplot as plt
import itertools as it
from typing import List
from toolz.itertoolz import sliding_window

#Asking the user for a url of the match
url = input("Enter url of the match [frebf]: ")

#The url is cut in order to get the information of the match
matchInfo = url[38:]

#Location of the information of the matches
location ='D:/Chamba/Analysis/Directory/UEFA-Euro-2020/Matches/' + matchInfo + '/'

#Taking away the information of the match through the url
matchInfo = matchInfo.split('-')

localTeam = matchInfo[0]
awayTeam = matchInfo[1]
competition = matchInfo[5] + "-" + matchInfo[6]
date = matchInfo[2]+'-'+matchInfo[3]+'-'+matchInfo[4]

#Methods to remove the duplicated columns in the dataframes
def get_duplicate_cols(df: pd.DataFrame) -> pd.Series:
    return pd.Series(df.columns).value_counts()[lambda x: x>1]

def get_dup_col_indices(df: pd.DataFrame, col: str) -> List[int]:
    return [x[0] for x in enumerate(df.columns)
            if x[1]==col][1:]

def get_all_dup_col_indices(df: pd.DataFrame) -> List[int]:
    dup_cols = get_duplicate_cols(df).index

    return sorted(list(it.chain.from_iterable(get_dup_col_indices(df, x)
                           for x in dup_cols)))

def remove_dup_cols(df: pd.DataFrame) -> pd.DataFrame:
    indices_to_remove =  get_all_dup_col_indices(df)

    if len(indices_to_remove)==0:
        return df
    window = list(sliding_window(2, indices_to_remove))

    first = df.iloc[:, :indices_to_remove[0]]
    middle = [df.iloc[:, x[0] + 1 : x[1]] for x in window]
    last = df.iloc[:, indices_to_remove[-1] + 1:]

    if (indices_to_remove[-1]) == (df.shape[1]-1):
        return pd.concat([first] + middle, axis=1)
    else:
        return pd.concat([first] + middle + [last], axis=1)

print('Loading local team info...')
#Creating the dataframes for each one of the .csv files
#Match information is used to name the different files
generalLocal = pd.read_csv(location + localTeam + "GeneralStats" + "vs" + awayTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5) 
generalLocal = generalLocal.iloc[:-1]


passingLocal = pd.read_csv(location + localTeam + "PassingStats" + "vs" + awayTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5) 
passingLocal = passingLocal.iloc[:-1]

passingTypeLocal = pd.read_csv(location + localTeam + "PassingTypeStats" + "vs" + awayTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
passingTypeLocal = passingTypeLocal.iloc[:-1]

defenseLocal = pd.read_csv(location + localTeam + "DefenseStats" + "vs" + awayTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
defenseLocal = defenseLocal.iloc[:-1]

possessionLocal = pd.read_csv(location + localTeam+ "PossessionStats" + "vs" + awayTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
possessionLocal = possessionLocal.iloc[:-1]

cardsLocal = pd.read_csv(location + localTeam + "MiscStats" + "vs" + awayTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
cardsLocal = cardsLocal.iloc[:-1]

print('Local team info loaded.')

print('Merging local team info...')
#Merging all the dataframes into a single one
dataLocal = pd.merge(generalLocal, passingLocal, on=['Player', 'Pos', '#', 'Age', 'Min', 'Att', 'Ast', 'Cmp%', 'Cmp',  'xA', 'Prog'])
dataLocal = pd.merge(dataLocal, passingTypeLocal, on=['Player', 'Pos', '#', 'Age', 'Min'])
dataLocal = pd.merge(dataLocal, defenseLocal, on=['Player', 'Pos', '#', 'Age', 'Min'])
dataLocal = pd.merge(dataLocal, possessionLocal, on=['Player', 'Pos', '#', 'Age', 'Min'])
dataLocal = pd.merge(dataLocal, cardsLocal, on=['Player', 'Pos', '#', 'Age', 'Min'])

#Removing the duplicated columns
dataLocal = remove_dup_cols(dataLocal)
print('Successful merge.')

#Saving the resume of the team previously mentioned
print('Creating local team resume...')
dataLocal.to_csv(r'D:/Chamba/Analysis/Directory/UEFA-Euro-2020/Matches/' + localTeam + '-' + awayTeam + '-' + date + '-' + competition + '/' + localTeam + 'ResumeVs' +awayTeam+ '.csv')
print('Local team resume done.')

print('Loading away team info...')
#Creating the dataframes for each one of the .csv files
#Match information is used to name the different files
generalAway = pd.read_csv(location + awayTeam + "GeneralStats" + "vs" + localTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5) 
generalAway = generalAway.iloc[:-1]

passingAway = pd.read_csv(location + awayTeam + "PassingStats" + "vs" + localTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5) 
passingAway = passingAway.iloc[:-1]

passingTypeAway = pd.read_csv(location + awayTeam + "PassingTypeStats" + "vs" + localTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
passingTypeAway = passingTypeAway.iloc[:-1]

defenseAway = pd.read_csv(location + awayTeam + "DefenseStats" + "vs" + localTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
defenseAway = defenseAway.iloc[:-1]

possessionAway = pd.read_csv(location + awayTeam+ "PossessionStats" + "vs" + localTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
possessionAway = possessionAway.iloc[:-1]

cardsAway = pd.read_csv(location + awayTeam + "MiscStats" + "vs" + localTeam + ".csv", encoding = "ISO-8859-1", skiprows = 5)
cardsAway = cardsAway.iloc[:-1]

print('Away team info loaded.')

print('Merging away team info...')
#Merging all the dataframes into a single one
dataAway = pd.merge(generalAway, passingAway, on=['Player', 'Pos', '#', 'Age', 'Min', 'Att', 'Ast', 'Cmp%', 'Cmp',  'xA', 'Prog'])
dataAway = pd.merge(dataAway, passingTypeAway, on=['Player', 'Pos', '#', 'Age', 'Min'])
dataAway = pd.merge(dataAway, defenseAway, on=['Player', 'Pos', '#', 'Age', 'Min'])
dataAway = pd.merge(dataAway, possessionAway, on=['Player', 'Pos', '#', 'Age', 'Min'])
dataAway = pd.merge(dataAway, cardsAway, on=['Player', 'Pos', '#', 'Age', 'Min'])

#Removing the duplicated columns
dataAway = remove_dup_cols(dataAway)
print('Successful merge.')

#Saving the resume of the team previously mentioned
print('Creating away team resume...')
dataAway.to_csv(r'D:/Chamba/Analysis/Directory/UEFA-Euro-2020/Matches/' + localTeam + '-' + awayTeam + '-' + date + '-' + competition + '/' + awayTeam + 'ResumeVs' +localTeam+ '.csv')
print('Away team resume done.')

#Merging all the dataframes of both teams into a single one
print('Merging both teams info...')
dataGeneralBothTeams = pd.merge(dataLocal, dataAway, how='outer')
print('Successful merge.')

#Saving the resume of both teams
print('Creating match resume...')
dataGeneralBothTeams.to_csv(r'D:/Chamba/Analysis/Directory/UEFA-Euro-2020/Matches/' + localTeam + '-' + awayTeam + '-' + date + '-' + competition + '/' + 'Resume'+ localTeam + 'Vs' +awayTeam+ '.csv')
print('Match resume done.')