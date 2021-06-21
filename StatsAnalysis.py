from datetime import date
from os import stat
from numpy.lib.function_base import select
import pandas as pd 
import os

#Get current location of the script
cwd = os.getcwd()

#Interactive menu to see the different stats of the teams, loading information by url
menu = True
listStats = ['1.Shooting', '2.Passing', '3.Receiving', '4.Creativity', '5.Dribbles', '6.Carries', '7.Tackles', '8.Pressures', '9.Aerial Duels', '10.Fouls & Cards']
while menu:
    print('===============================================================================')
    print('Welcome to my analysis machine!')
    print('===============================================================================')
    print('What do you want to do?')
    print('1.Select match.')
    print('2.Exit.')
    answer = input('Choose an option [Number]: ')
    if(answer == '1'):
        print('===============================================================================')
        matchList = pd.read_csv(cwd +'/Directory/UEFA-Euro-2020/MatchList.csv')

        for index, row in matchList.iterrows():
            print(index + 1, row.LocalTeam + ' Vs '+ row.AwayTeam + ' ' + row.Date + ' ' + row.Competition)
        
        matchAnswer = input('Select number of the desired match: ')

        url = matchList.Url[int(matchAnswer)-1]
        matchInfo = url[38:]

        location = cwd + '/Directory/UEFA-Euro-2020/Matches/' + matchInfo + '/'

        matchInfo = matchInfo.split('-')

        if(matchInfo[0] == 'Czech' or matchInfo[0] == 'North'):
            localTeam = matchInfo[0] + '-' + matchInfo[1]
            if(matchInfo[2] == 'Czech' or matchInfo[2] == 'North'):
                awayTeam = matchInfo[2] + '-' + matchInfo[3]
                date = matchInfo[4]+'-'+matchInfo[5]+'-'+matchInfo[6]
                competition = matchInfo[7] + '-' + matchInfo[8]
            else: 
                awayTeam = matchInfo[2]
                date = matchInfo[3]+'-'+matchInfo[4]+'-'+matchInfo[5]
                competition = matchInfo[6] + ' ' + matchInfo[7]
        else:
                localTeam = matchInfo[0]
                if(matchInfo[1] == 'Czech' or matchInfo[1] == 'North'):
                    awayTeam = matchInfo[1] + '-' + matchInfo[2]
                    date = matchInfo[3]+'-'+matchInfo[4]+'-'+matchInfo[5]
                    competition = matchInfo[6] + '-' + matchInfo[7]
                else: 
                    awayTeam = matchInfo[1]
                    date = matchInfo[2]+'-'+matchInfo[3]+'-'+matchInfo[4]
                    competition = matchInfo[5] + ' ' + matchInfo[6]

        dataLocalTeam = pd.read_csv(location + localTeam + 'ResumeVs' +awayTeam+ '.csv', encoding = 'utf-8')  
        dataAwayTeam = pd.read_csv(location + awayTeam + 'ResumeVs' + localTeam+ '.csv', encoding = 'utf-8')
        dataBothTeams = pd.read_csv(location + 'Resume' +localTeam + 'Vs' + awayTeam+ '.csv', encoding = 'utf-8')
        print('===============================================================================')
        print('Match information was loaded successfully!')
        
        while(answer == '1'):
            print('===============================================================================')
            print('Team options:')
            print('1.' + localTeam)
            print('2.' + awayTeam)
            print('3.Both')
            print('4.Go back')
            print('===============================================================================')
            teamAnswer = input('Choose an option [Number]: ')
            if(teamAnswer != '4'):
                selectionLoop = True
            else: 
                selectionLoop = False
                answer = -1

            while(selectionLoop):
                print('===============================================================================')
                print('Which stats do you wan to see?')
                print('1.Top players stats.')
                print('2.Particular player stats.')
                print('3.Go back.')
                print('===============================================================================')
                selectionAnswer = input('Choose an option [Number]: ')
                if(selectionAnswer != '3'):
                    statsLoop = True
                else: 
                    statsLoop = False
                    selectionLoop = False
                
                while(selectionAnswer == '1'):
                    print('===============================================================================')
                    print('Stats options: ')

                    for stat in listStats:
                        print(stat)
                    print('-1.Go back.')
                    print('===============================================================================')
                    statType = input('Enter stats to see [Number]: ')

                    if(statType == '1'):
                        if(teamAnswer == '1'):
                            shootingDataLocalTeam = dataLocalTeam[dataLocalTeam.Sh_x > 0]
                            shootingDataLocalTeam = dataLocalTeam.sort_values(['Gls','Sh_x'], ascending=False)

                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam + ' with most shots in the game')
                            print('===============================================================================')
                            print(shootingDataLocalTeam[['Player', 'Pos', 'Min', 'Gls', 'Sh_x', 'SoT','xG', 'npxG']].head(5))
                        
                        elif(teamAnswer == '2'):
                            shootingDataAwayTeam = dataAwayTeam[dataAwayTeam.Sh_x > 0]
                            shootingDataAwayTeam = dataAwayTeam.sort_values(['Gls','Sh_x'], ascending=False)

                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam + ' with most shots in the game')
                            print('===============================================================================')
                            print(shootingDataAwayTeam[['Player', 'Pos', 'Min', 'Gls', 'Sh_x', 'SoT','xG', 'npxG']].head(5))

                        elif(teamAnswer == '3'):
                            shootingDataBothTeams = dataBothTeams[dataBothTeams.Sh_x > 0]
                            shootingDataBothTeams = dataBothTeams.sort_values(['Gls','Sh_x'], ascending=False)

                            print('===============================================================================')
                            print('Top 10 players with most shots in the game ' + localTeam + ' Vs ' + awayTeam)
                            print('===============================================================================')
                            print(shootingDataBothTeams[['Player', 'Pos', 'Min', 'Gls', 'Sh_x', 'SoT','xG', 'npxG', 'Team']].head(10))

                    elif(statType == '2'):

                        if(teamAnswer == '1'):
                            passingDataLocalTeam = dataLocalTeam.sort_values(by='Cmp%', ascending=False)
                            mean = dataLocalTeam['Att_x'].mean()
                            passingDataLocalTeam = passingDataLocalTeam[passingDataLocalTeam.Att_x > mean]
                    
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam + ' with higher pass conversion than team average ')
                            print('===============================================================================')
                            print(passingDataLocalTeam[['Player', 'Pos', 'Min','Att_x', 'Cmp_x', 'Cmp%','TotDist_x', 'PrgDist_x', 'Att.1_y', 'Cmp.1', 'Cmp%.1', 'Att.2', 'Cmp.2', 'Cmp%.2', 'Att.3', 'Cmp.3', 'Cmp%.3']].head(5))

                        elif(teamAnswer == '2'):
                        
                            passingDataAwayTeam = dataAwayTeam.sort_values(by='Cmp%', ascending=False)

                            mean = dataAwayTeam['Att_x'].mean()

                            passingDataAwayTeam = passingDataAwayTeam[passingDataAwayTeam.Att_x > mean]

                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam + ' with higher pass conversion than team average ')
                            print('===============================================================================')
                            print(passingDataAwayTeam[['Player', 'Pos', 'Min', 'Att_x', 'Cmp_x', 'Cmp%','TotDist_x', 'PrgDist_x', 'Att.1_y', 'Cmp.1', 'Cmp%.1', 'Att.2', 'Cmp.2', 'Cmp%.2', 'Att.3', 'Cmp.3', 'Cmp%.3']].head(5))

                        elif(teamAnswer == '3'):
                        
                            passingDataBothTeams = dataBothTeams.sort_values(by='Cmp%', ascending=False)

                            mean = dataBothTeams['Att_x'].mean()

                            passingDataBothTeams = passingDataBothTeams[passingDataBothTeams.Att_x > mean]

                            print('===============================================================================')
                            print('Top 10 players with most pass convertion rate in the game ' + localTeam + ' Vs ' + awayTeam )
                            print('===============================================================================')
                            print(passingDataBothTeams[['Player', 'Pos', 'Min', 'Att_x', 'Cmp_x', 'Cmp%','TotDist_x', 'PrgDist_x', 'Att.1_y', 'Cmp.1', 'Cmp%.1', 'Att.2', 'Cmp.2', 'Cmp%.2', 'Att.3', 'Cmp.3', 'Cmp%.3', 'Team']].head(10))


                    elif(statType == '3'):
                        if(teamAnswer == '1'):

                            receivingDataLocalTeam = dataLocalTeam.sort_values(by='Targ', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam + ' that were targeted the most by passes')
                            print('===============================================================================')
                            print(receivingDataLocalTeam[['Player', 'Pos', 'Min', 'Touches_x', 'Targ', 'Rec', 'Rec%', 'Prog.1_y']].head(5))
                    
                        elif(teamAnswer == '2'):
                            receivingDataAwayTeam = dataAwayTeam.sort_values(by='Targ', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam + ' that were targeted the most by passes')
                            print('===============================================================================')
                            print(receivingDataAwayTeam[['Player', 'Pos', 'Min', 'Touches_x','Targ', 'Rec', 'Rec%', 'Prog.1_y']].head(5))
                        
                        elif(teamAnswer == '3'):
                            receivingDataBothTeams = dataBothTeams.sort_values(by='Targ', ascending=False)
                            print('===============================================================================')
                            print('Top 10 players that were targeted the most by passes in the game ' + localTeam + ' Vs ' + awayTeam)
                            print('===============================================================================')
                            print(receivingDataBothTeams[['Player', 'Pos', 'Min', 'Touches_x','Targ', 'Rec', 'Rec%', 'Prog.1_y', 'Team']].head(10))
                    
                    elif(statType == '4'):
                        if(teamAnswer == '1'):
                            creativityDataLocalTeam = dataLocalTeam.sort_values(by='SCA', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam + ' that created more opportunities')
                            print('===============================================================================')
                            print(creativityDataLocalTeam[['Player', 'Pos', 'Min', 'Gls', 'xG', 'Sh_x', 'SoT', 'Ast','xA', 'SCA', 'GCA', 'KP', 'CPA', 'PPA']].head(5))

                        elif(teamAnswer == '2'):
                            creativityDataAwayTeam = dataAwayTeam.sort_values(by='SCA', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam + ' that created more opportunities')
                            print('===============================================================================')
                            print(creativityDataAwayTeam[['Player', 'Pos', 'Min', 'Gls', 'xG', 'Sh_x', 'SoT', 'SCA', 'GCA','Ast','xA', 'KP', 'CPA', 'PPA']].head(5))
                    
                        elif(teamAnswer == '3'):
                            creativityDataBothTeams = dataBothTeams.sort_values(by='SCA', ascending=False)
                            print('===============================================================================')
                            print('Top 10 players that created more opportunities in the game ' + localTeam + ' Vs ' + awayTeam)
                            print('===============================================================================')
                            print(creativityDataBothTeams[['Player', 'Pos', 'Min', 'Gls', 'xG', 'Sh_x', 'SoT', 'SCA', 'GCA','Ast','xA', 'KP', 'CPA', 'PPA', 'Team']].head(10))

                    elif(statType == '5'):
                        if(teamAnswer == '1'):
                            dribblingDataLocalTeam = dataLocalTeam.sort_values(['Att.1_x', 'Succ%'], ascending=False)
                            print('===============================================================================')
                            print('Top 5 dribblers of ' +localTeam )
                            print('===============================================================================')
                            print(dribblingDataLocalTeam[['Player', 'Pos', 'Min', 'Att.1_x', 'Succ', 'Succ%', '#Pl', 'Megs', 'Fld']].head(5))

                        elif(teamAnswer == '2'):
                            dribblingDataAwayTeam = dataAwayTeam.sort_values(['Att.1_x', 'Succ%'], ascending=False)
                            print('===============================================================================')
                            print('Top 5 dribblers of ' +awayTeam )
                            print('===============================================================================')
                            print(dribblingDataAwayTeam[['Player', 'Pos', 'Min', 'Att.1_x', 'Succ', 'Succ%', '#Pl', 'Megs', 'Fld']].head(5))
                        
                        elif(teamAnswer == '3'):
                            dribblingDataBothTeams = dataBothTeams.sort_values(['Att.1_x', 'Succ%'], ascending=False)
                            print('===============================================================================')
                            print('Top 10 dribblers of in the game ' + localTeam + ' Vs ' + awayTeam )
                            print('===============================================================================')
                            print(dribblingDataBothTeams[['Player', 'Pos', 'Min', 'Att.1_x', 'Succ', 'Succ%', '#Pl', 'Megs', 'Fld', 'Team']].head(10))
                    
                    elif(statType == '6'):
                        if(teamAnswer == '1'):
                            carriesDataLocalTeam = dataLocalTeam.sort_values(by='Carries_y', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam+ ' with the most carries' )
                            print('===============================================================================')
                            print(carriesDataLocalTeam[['Player', 'Pos', 'Min', 'Carries_y', 'TotDist_y', 'PrgDist_y', 'Prog_y', '1/3_y', 'CPA', 'Mis', 'Dis']].head(5))

                        elif(teamAnswer == '2'):
                            carriesDataAwayTeam = dataAwayTeam.sort_values(by='Carries_y', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam+ ' with the most carries' )
                            print('===============================================================================')
                            print(carriesDataAwayTeam[['Player', 'Pos', 'Min', 'Carries_y', 'TotDist_y', 'PrgDist_y', 'Prog_y', '1/3_y', 'CPA', 'Mis', 'Dis']].head(5))

                        elif(teamAnswer == '3'):
                            carriesDataBothTeams = dataBothTeams.sort_values(by='Carries_y', ascending=False)
                            print('===============================================================================')
                            print('Top 10 players with the most carries in the game ' + localTeam + ' Vs ' + awayTeam )
                            print('===============================================================================')
                            print(carriesDataBothTeams[['Player', 'Pos', 'Min', 'Carries_y', 'TotDist_y', 'PrgDist_y', 'Prog_y', '1/3_y', 'CPA', 'Mis', 'Dis', 'Team']].head(10))

                    elif(statType == '7'):
                        if(teamAnswer == '1'):
                            tacklesDataLocalTeam = dataLocalTeam.sort_values(by='Tkl_y', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam+ ' with the most tackles' )
                            print('===============================================================================')
                            print(tacklesDataLocalTeam[['Player', 'Pos', 'Min', 'Tkl_y', 'TklW_x', 'Tkl.1', 'Tkl%', 'Past', 'Int_x', 'Tkl+Int', 'Clr', 'Mis']].head(5))

                        elif(teamAnswer == '2'):
                            tacklesDataAwayTeam = dataAwayTeam.sort_values(by='Tkl_y', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam+ ' with the most tackles' )
                            print('===============================================================================')
                            print(tacklesDataAwayTeam[['Player', 'Pos', 'Min', 'Tkl_y', 'TklW_x', 'Tkl.1', 'Tkl%', 'Past', 'Int_x', 'Tkl+Int', 'Clr', 'Mis']].head(5))
                    
                        elif(teamAnswer == '3'):
                            tacklesDataBothTeams = dataBothTeams.sort_values(by='Tkl_y', ascending=False)
                            print('===============================================================================')
                            print('Top 10 players with the most tackles in the game ' + localTeam + ' Vs ' + awayTeam)
                            print('===============================================================================')
                            print(tacklesDataBothTeams[['Player', 'Pos', 'Min', 'Tkl_y', 'TklW_x', 'Tkl.1', 'Tkl%', 'Past', 'Int_x', 'Tkl+Int', 'Clr', 'Mis', 'Team']].head(10))

                    elif(statType == '8'):
                        if(teamAnswer == '1'):
                            pressingDataLocalTeam = dataLocalTeam.sort_values(by='Press', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam+ ' with the most pressings' )
                            print('===============================================================================')
                            print(pressingDataLocalTeam[['Player', 'Pos', 'Min', 'Press', 'Succ_y', '%', 'Def 3rd.1', 'Recov', 'Att 3rd.1', 'Blocks', 'Sh_y', 'ShSv', 'Pass']].head(5))

                        elif(teamAnswer == '2'):
                            pressingDataAwayTeam = dataAwayTeam.sort_values(by='Press', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam+ ' with the most pressings' )
                            print('===============================================================================')
                            print(pressingDataAwayTeam[['Player', 'Pos', 'Min', 'Press', 'Succ_y', '%', 'Def 3rd.1', 'Att 3rd.1', 'Recov', 'Blocks', 'Sh_y', 'ShSv', 'Pass']].head(5))
                    
                        elif(teamAnswer == '3'):
                            pressingDataBothTeams = dataBothTeams.sort_values(by='Press', ascending=False)
                            print('===============================================================================')
                            print('Top 10 players with the most pressings in the game ' + localTeam + ' Vs ' + awayTeam)
                            print('===============================================================================')
                            print(pressingDataBothTeams[['Player', 'Pos', 'Min', 'Press', 'Succ_y', '%', 'Def 3rd.1', 'Att 3rd.1', 'Recov', 'Blocks', 'Sh_y', 'ShSv', 'Pass', 'Team']].head(10))

                    elif(statType == '9'):
                        if(teamAnswer == '1'):
                            aerialDuelsDataLocalTeam = dataLocalTeam.sort_values(by='Won%', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam+ ' with the highest percentage of aerial duels won' )
                            print('===============================================================================')
                            print(aerialDuelsDataLocalTeam[['Player', 'Pos', 'Min', 'Won', 'Lost', 'Won%']].head(5))

                        elif(teamAnswer == '2'):
                            aerialDuelsDataAwayTeam = dataAwayTeam.sort_values(by='Won%', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam+ ' with the highest percentage of aerial duels won' )
                            print('===============================================================================')
                            print(aerialDuelsDataAwayTeam[['Player', 'Pos', 'Min', 'Won', 'Lost', 'Won%']].head(5))

                        elif(teamAnswer == '3'):
                            aerialDuelsDataBothTeams = dataBothTeams.sort_values(by='Won%', ascending=False)
                            print('===============================================================================')
                            print('Top 10 players of with the highest percentage of aerial duels won in the game ' + localTeam + ' Vs ' + awayTeam )
                            print('===============================================================================')
                            print(aerialDuelsDataBothTeams[['Player', 'Pos', 'Min', 'Won', 'Lost', 'Won%', 'Team']].head(10))

                    elif(statType == '10'):
                        if(teamAnswer == '1'):
                            cardsDataLocalTeam = dataLocalTeam.sort_values(by='Fls', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +localTeam+ ' with most fouls committed' )
                            print('===============================================================================')
                            print(cardsDataLocalTeam[['Player', 'Pos', 'Min', 'Fls', 'CrdY_y', 'CrdR_y', '2CrdY']].head(5))

                        elif(teamAnswer == '2'):
                            cardsDataAwayTeam = dataAwayTeam.sort_values(by='Fls', ascending=False)
                            print('===============================================================================')
                            print('Top 5 players of ' +awayTeam+ ' with with most fouls committed' )
                            print('===============================================================================')
                            print(cardsDataAwayTeam[['Player', 'Pos', 'Min', 'Fls', 'CrdY_y', 'CrdR_y', '2CrdY']].head(5))

                        elif(teamAnswer == '3'):
                            cardsDataBothTeams = dataBothTeams.sort_values(by='Fls', ascending=False)
                            print('===============================================================================')
                            print('Top 10 players with with most fouls committed in the game ' + localTeam + ' Vs ' + awayTeam)
                            print('===============================================================================')
                            print(cardsDataBothTeams[['Player', 'Pos', 'Min', 'Fls', 'CrdY_y', 'CrdR_y', '2CrdY', 'Team']].head(10))

                    elif(statType == '-1'):
                        selectionAnswer = '-1'
                
                while(selectionAnswer == '2'):
                    if(teamAnswer == '1'):
                        print('Players of ' + localTeam)
                        for index, row in dataLocalTeam.iterrows():
                            row.Player = row.Player.split('\\')
                            print(index + 1, row.Player[0])
                        print('-1.Go back.')
                        playerAnswer = input('Select player to see their stats: ')
                        if(playerAnswer != '-1'):
                            player = dataLocalTeam.loc[[int(playerAnswer) - 1]]
                            playerName = player[['Player']].to_string(index = False,header=False)
                            playerName = playerName.split('\\')
                            playerName = playerName[0]
                            statsLoop = True
                        else: 
                            selectionAnswer = '-1'
                            statsLoop = False
                    
                    elif(teamAnswer == '2'):
                        print('Players of ' + awayTeam)
                        for index, row in dataAwayTeam.iterrows():
                            row.Player = row.Player.split('\\')
                            print(index + 1, row.Player[0])
                        print('-1.Go back.')
                        playerAnswer = input('Select player to see their stats: ')
                        if(playerAnswer != '-1'):
                            player = dataAwayTeam.loc[[int(playerAnswer) - 1]]
                            playerName = player[['Player']].to_string(index = False,header=False)
                            playerName = playerName.split('\\')
                            playerName = playerName[0]
                            statsLoop = True
                        else: 
                            selectionAnswer = '-1'
                            statsLoop = False
                    
                    elif(teamAnswer == '3'):
                        print('Players of the match')
                        for index, row in dataBothTeams.iterrows():
                            row.Player = row.Player.split('\\')
                            print(index + 1, row.Player[0])
                        print('-1.Go back.')
                        playerAnswer = input('Select player to see their stats: ')
                        if(playerAnswer != '-1'):
                            player = dataBothTeams.loc[[int(playerAnswer) - 1]]
                            playerName = player[['Player']].to_string(index = False,header=False)
                            playerName = playerName.split('\\')
                            playerName = playerName[0]
                            statsLoop = True
                        else: 
                            selectionAnswer = '-1'
                            statsLoop = False

                    

                    while(statsLoop):
                        print('===============================================================================')
                        print('Stats options: ')

                        for stat in listStats:
                            print(stat)
                        print('-1.Go back.')
                        print('===============================================================================')
                        statType = input('Enter stats to see [Number]: ')

                        if(statType == '1'):
                        
                            shootingPlayer = player.sort_values(['Gls','Sh_x'], ascending=False)

                            print('===============================================================================')
                            print('Shooting stats of: ' + playerName)
                            print('===============================================================================')
                            print(shootingPlayer[['Player', 'Pos', 'Min', 'Gls', 'Sh_x', 'SoT','xG', 'npxG']])

                        elif(statType == '2'):
                            passingPlayer = player.sort_values(by='Cmp%', ascending=False)
                    
                            print('===============================================================================')
                            print('Passing stats of: ' + playerName)
                            print('===============================================================================')
                            print(passingPlayer[['Player', 'Pos', 'Min','Att_x', 'Cmp_x', 'Cmp%','TotDist_x', 'PrgDist_x', 'Att.1_y', 'Cmp.1', 'Cmp%.1', 'Att.2', 'Cmp.2', 'Cmp%.2', 'Att.3', 'Cmp.3', 'Cmp%.3']])
                        
                        elif(statType == '3'):
                            
                            receivingPlayer = player.sort_values(by='Targ', ascending=False)
                            print('===============================================================================')
                            print('Recieving stats of: ' + playerName)
                            print('===============================================================================')
                            print(receivingPlayer[['Player', 'Pos', 'Min', 'Touches_x', 'Targ', 'Rec', 'Rec%', 'Prog.1_y']])

                        elif(statType == '4'):
                        
                            creativityPlayer = player.sort_values(by='SCA', ascending=False)
                            print('===============================================================================')
                            print('Creativity stats of: ' + playerName)
                            print('===============================================================================')
                            print(creativityPlayer[['Player', 'Pos', 'Min', 'Gls', 'xG', 'Sh_x', 'SoT', 'Ast','xA', 'SCA', 'GCA', 'KP', 'CPA', 'PPA']])

                        elif(statType == '5'):

                            dribblingPlayer = player.sort_values(['Att.1_x', 'Succ%'], ascending=False)
                            print('===============================================================================')
                            print('Dribbling stats of ' + playerName )
                            print('===============================================================================')
                            print(dribblingPlayer[['Player', 'Pos', 'Min', 'Att.1_x', 'Succ', 'Succ%', '#Pl', 'Megs', 'Fld']])
                        
                        elif(statType == '6'):
                            carriesPlayer = player.sort_values(by='Carries_y', ascending=False)
                            print('===============================================================================')
                            print('Carrying stats of '  + playerName)
                            print('===============================================================================')
                            print(carriesPlayer[['Player', 'Pos', 'Min', 'Carries_y', 'TotDist_y', 'PrgDist_y', 'Prog_y', '1/3_y', 'CPA', 'Mis', 'Dis']])

                        elif(statType == '7'):
                            tacklesPlayer = player.sort_values(by='Tkl_y', ascending=False)
                            print('===============================================================================')
                            print('Tackling stats of ' + playerName )
                            print('===============================================================================')
                            print(tacklesPlayer[['Player', 'Pos', 'Min', 'Tkl_y', 'TklW_x', 'Tkl.1', 'Tkl%', 'Past', 'Int_x', 'Tkl+Int', 'Clr', 'Mis']])

                        elif(statType == '8'):
                            pressingPlayer = player.sort_values(by='Press', ascending=False)
                            print('===============================================================================')
                            print('Pressing stats of ' + playerName )
                            print('===============================================================================')
                            print(pressingPlayer[['Player', 'Pos', 'Min', 'Press', 'Succ_y', '%', 'Def 3rd.1', 'Recov', 'Att 3rd.1', 'Blocks', 'Sh_y', 'ShSv', 'Pass']])

                        elif(statType == '9'):
                            aerialDuelsPlayer = player.sort_values(by='Won%', ascending=False)
                            print('===============================================================================')
                            print('Aerial duels stats of ' + playerName )
                            print('===============================================================================')
                            print(aerialDuelsPlayer[['Player', 'Pos', 'Min', 'Won', 'Lost', 'Won%']])

                        elif(statType == '10'):
                            cardsPlayers = player.sort_values(by='Fls', ascending=False)
                            print('===============================================================================')
                            print('Fouling stats of ' + playerName)
                            print('===============================================================================')
                            print(cardsPlayers[['Player', 'Pos', 'Min', 'Fls', 'CrdY_y', 'CrdR_y', '2CrdY']].head(5))

                        elif(statType == '-1'):
                            statsLoop = False

    elif(answer == '2'):
        print('Machine closed.')
        menu = False