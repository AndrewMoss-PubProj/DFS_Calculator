import PrepSolve
import pandas as pd
import numpy as np
import selenium_Nav
import Utils


selenium_Nav.driver.close()
def LineupGen(lineupNumber):
    Lineups = pd.DataFrame(columns=['Lineup'])
    sheet = PrepSolve.SimPrep(2)
    sheet['Lineups'] = 0
    Positions = ['P', 'C', '1B', '2B', '3B', 'SS', 'OF']
    RosterLims = [2, 1, 1, 1, 1, 1, 3]
    sheet = sheet.reset_index()
    sheet = sheet.iloc[:, 1:]
    sheet.to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\MasterSheet.csv')
    while len(Lineups) < lineupNumber:
        sampleSheet = sheet.copy()
        TempLineup = pd.DataFrame()
        for num, Position in zip(RosterLims, Positions):
            TempLineup = TempLineup.append(sampleSheet[sampleSheet.Roster_Position.str.contains(Position, case=False)].sample(n=num, weights=sampleSheet['Ownership']), ignore_index=True)
        if sum(TempLineup['Price']) > 48500 and sum(TempLineup['Price']) <= 50000 and  len(TempLineup) != len(set(TempLineup)):
            tempList = TempLineup['ID'].tolist()
            Lineups.at[len(Lineups), 'Lineup'] = tempList
            print('Good Lineup Found ' + str(sum(TempLineup['Price'])))
            sheet['Lineups'] = np.where(np.isin(sheet['ID'], TempLineup['ID']), sheet['Lineups'] + 1, sheet['Lineups'])
            print(len(Lineups))
        else:
            print('Lineup Did not Qualify ' + str(sum(TempLineup['Price'])))

    Lineups.to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\MarketLineups.csv')

def RunSim(runs):
    Covs = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\Covariance", delim_whitespace=True)
    sheet = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\Simulation\\MasterSheet.csv")
    sheet = sheet.loc[:, ['ID', 'TeamAbbrev', 'Pos', 'FP', 'Variance']]
    finalSheet = pd.DataFrame()
    BatterScores = pd.DataFrame(columns=['Name'])
    PitcherScores = pd.DataFrame(columns=['Name'])
    teamList = sheet['TeamAbbrev'].tolist()
    teamList = Utils.removeDupes(teamList)
    for team in teamList:
        print(team)
        BatterScores = BatterScores.iloc[0:0, :]
        PitcherScores = PitcherScores.iloc[0:0, :]
        activeTeam = sheet[sheet['TeamAbbrev'] == team]
        activeTeam = activeTeam.drop_duplicates()
        activePitcher = activeTeam[activeTeam['Pos'] == 0]
        activeBatters = activeTeam[activeTeam['Pos'] != 0]
        activeBatters = activeBatters.reset_index()
        activeBatters = activeBatters.drop_duplicates()
        BatterScores['Name'] = activeBatters['ID'].tolist()
        PitcherScores['Name'] = activePitcher['ID'].tolist()
        BatterNums = activeBatters['Pos'].tolist()

        tempCovs = Covs.copy()

        count = 0
        for x in range(0, 9):
            if x in BatterNums:
                tempCovs.iloc[x-1, x-1] = activeBatters.loc[count, 'Variance']
                count = count+1
        for x in range(0, 9):
            if x+1 not in BatterNums:
                tempCovs = tempCovs.drop(['DK'+str(x+1)], axis=1)
                tempCovs = tempCovs.drop(index='DK'+str(x+1))
        for number in range(0, runs):
            PitcherScores[str(number+1)] = np.random.normal(activePitcher['FP'], np.sqrt(activePitcher['Variance']))
            BatterTemp = np.random.multivariate_normal(activeBatters['FP'],tempCovs)
            BatterTemp = np.where(BatterTemp < 0, 0, BatterTemp).tolist()
            BatterScores[str(number+1)] = BatterTemp
        finalSheet = finalSheet.append(PitcherScores)
        finalSheet = finalSheet.append(BatterScores)
        finalSheet = finalSheet.reset_index()
        finalSheet = finalSheet.iloc[:, 1:]
    finalSheet.to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\SimPreds.csv')

def ScoreLineups ():
    Lineups = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\MarketLineups.csv')
    Lineups = Lineups['Lineup']
    Preds = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\Simpreds.csv')
    FinalFrame = pd.DataFrame()
    for Lineup in Lineups:
        Lineup = Utils.reprocessList(Lineup)
        LineupFrame = pd.DataFrame(data=Lineup, columns=['ID'])
        LineupFrame.to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\test.csv')
        LineupFrame = pd.merge(LineupFrame, Preds, how='left', left_on='ID', right_on='Name')
        LineupFrame = LineupFrame.iloc[:, 3:]
        tempScores = LineupFrame.sum(axis=0)
        FinalFrame = FinalFrame.append(tempScores, ignore_index=True)
    FinalFrame['Lineup'] = Lineups
    FinalFrame = FinalFrame.sort_index(axis=1,ascending=False)
    FinalFrame.to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\LineupPreds.csv')

def Debrief(Lineups,runs):
    sheet = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\LineupPreds.csv')
    Runs = sheet.iloc[:, 2:].copy()
    WinList = Runs.idxmax()
    WinList = WinList.value_counts()
    WinList = pd.DataFrame(WinList.sort_index())
    tempList = pd.DataFrame(np.zeros(Lineups))
    WinList = pd.merge(WinList, tempList, how='right', left_index=True, right_index=True)
    WinList = WinList.iloc[:, 0]
    WinList = WinList.fillna(0)
    sheet['Wins'] = WinList

    cashArray = []
    fiftyArray = []
    tenArray = []
    oneArray = []
    tournCashArray = []
    for run in range(0, runs):
        tournCashList = Runs.nlargest(int(round(.25*len(sheet))), str(run+1))
        tournCashList = tournCashList.loc[:, str(run+1)].index.tolist()
        tournCashArray.append(tournCashList)

        cashList = Runs.nlargest(int(round(.45*len(sheet))), str(run+1))
        cashList = cashList.loc[:, str(run+1)].index.tolist()
        cashArray.append(cashList)
        fiftyList = Runs.nlargest(int(round(.5*len(sheet))), str(run+1))
        fiftyList = fiftyList.loc[:, str(run+1)].index.tolist()
        fiftyArray.append(fiftyList)

        tenList = Runs.nlargest(int(round(.1*len(sheet))), str(run+1))
        tenList = tenList.loc[:, str(run+1)].index.tolist()
        tenArray.append(tenList)

        oneList = Runs.nlargest(int(round(.01*len(sheet))), str(run+1))
        oneList = oneList.loc[:, str(run+1)].index.tolist()
        oneArray.append(oneList)

    flatten = lambda l: [item for sublist in l for item in sublist]
    cashArray = flatten(cashArray)
    cashArray = pd.Series(cashArray).value_counts()
    cashArray = pd.DataFrame(cashArray.sort_index())
    cashArray = pd.merge(cashArray, tempList, how='right', left_index=True, right_index=True)
    cashArray = cashArray.iloc[:, 0]
    cashArray = cashArray.fillna(0)
    sheet['Cashes'] = cashArray

    fiftyArray = flatten(fiftyArray)
    fiftyArray = pd.Series(fiftyArray).value_counts()
    fiftyArray = pd.DataFrame(fiftyArray.sort_index())
    fiftyArray = pd.merge(fiftyArray, tempList, how='right', left_index=True, right_index=True)
    fiftyArray = fiftyArray.iloc[:, 0]
    fiftyArray = fiftyArray.fillna(0)
    sheet['50/50s'] = fiftyArray

    oneArray = flatten(oneArray)
    oneArray = pd.Series(oneArray).value_counts()
    oneArray = pd.DataFrame(oneArray.sort_index())
    oneArray = pd.merge(oneArray, tempList, how='right', left_index=True, right_index=True)
    oneArray = oneArray.iloc[:, 0]
    oneArray = oneArray.fillna(0)
    sheet['OnePercent'] = oneArray

    tenArray = flatten(tenArray)
    tenArray = pd.Series(tenArray).value_counts()
    tenArray = pd.DataFrame(tenArray.sort_index())
    tenArray = pd.merge(tenArray, tempList, how='right', left_index=True, right_index=True)
    tenArray = tenArray.iloc[:, 0]
    tenArray = tenArray.fillna(0)
    sheet['TenPercent'] = tenArray

    tournCashArray = flatten(tournCashArray)
    tournCashArray = pd.Series(tournCashArray).value_counts()
    tournCashArray = pd.DataFrame(tournCashArray.sort_index())
    tournCashArray = pd.merge(tournCashArray, tempList, how='right', left_index=True, right_index=True)
    tournCashArray = tournCashArray.iloc[:, 0]
    tournCashArray = tournCashArray.fillna(0)
    sheet['TournCash'] = tournCashArray


    sheet['SimOwned'] = 1
    sheet['>100'] = Runs.T[Runs.T > 100].count().values
    sheet['>110'] = Runs.T[Runs.T > 110].count().values
    sheet['>120'] = Runs.T[Runs.T > 120].count().values
    sheet['>125'] = Runs.T[Runs.T > 125].count().values
    sheet['>150'] = Runs.T[Runs.T > 150].count().values
    sheet['>175'] = Runs.T[Runs.T > 175].count().values
    sheet['Mean'] = Runs.mean(axis=1).values
    sheet['Variance'] = Runs.std(axis=1).values
    sheet['Max'] = Runs.max(axis=1).values
    sheet['MaxZ'] = (sheet.Max-sheet.Mean)/sheet.Variance

    sheet.iloc[:, 1:].to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\LineupPredsDash.csv')


def GetPlayerFrequency(runs):
    sheet = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\LineupPredsDash.csv')
    playerList = pd.read_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\MasterSheet.csv')
    statList = ['SimOwned', 'Wins', 'Cashes', 'TournCash', '50/50s', 'TenPercent', 'OnePercent', '>100', '>110', '>120', '>125', '>150', '>175']
    PlayFreqs = pd.DataFrame()
    for index, row in sheet.iterrows():
        Lineup = Utils.reprocessList(row['Lineup'])
        TempLineupDF = pd.DataFrame(data=Lineup, columns=['Player'])
        for stat in statList:
            TempLineupDF[stat] = row[stat]/sum(sheet[stat])*100
        PlayFreqs = PlayFreqs.append(TempLineupDF, ignore_index=True)
    PlayFreqs = PlayFreqs.groupby(['Player']).agg({'SimOwned': 'sum', 'Wins': 'sum', 'Cashes': 'sum', '50/50s': 'sum',
                                                   'TenPercent': 'sum', 'OnePercent': 'sum', '>100': 'sum', '>110': 'sum',
                                                   '>120': 'sum', '>125': 'sum', '>150': 'sum', '>175': 'sum', 'TournCash': 'sum'}).reset_index()
    playerList = pd.merge(PlayFreqs, playerList, how='inner', left_on='Player',right_on='ID')
    playerList = playerList.loc[:, ['Player', 'Roster_Position', 'FP', 'Variance', 'Price', 'Ownership', 'SimOwned', 'Wins', 'Cashes',
                                   'TournCash', '50/50s', 'TenPercent', 'OnePercent', '>100', '>110', '>120', '>125', '>150', '>175']]
    playerList['CashRat'] = playerList.Cashes/playerList.SimOwned
    playerList['TournRat'] = playerList.OnePercent/playerList.SimOwned
    playerList.to_csv('C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Simulation\\Frequencies.csv')








def Driver(Lineups,Runs):
    PrepSolve.CombinePredictions()
    LineupGen(Lineups)
    RunSim(Runs)
    print('Scoring Lineups')
    ScoreLineups()
    print('Getting Summary Stats')
    Debrief(Lineups, Runs)
    print('Generating frequencies')
    GetPlayerFrequency(Runs)

Driver(10000,1000)
