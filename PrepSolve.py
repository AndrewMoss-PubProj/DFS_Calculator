import Utils
import ScheduleScrape
import pandas as pd
import numpy as np


def PrepSolveMLB(site):
    CombinePredictions()
    pitchers = Utils.MLBvarAdjPits(pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\PitcherCombined.csv"),
                                   site)
    batters = Utils.MLBvarAdjBats(pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\BatterCombined.csv"),
                                  site)
    Schedule = ScheduleScrape.Driver()
    sheet = pd.concat([batters, pitchers], axis=0, sort=False)
    sheet = sheet.loc[:, ['Name', 'FP', 'VarAdj']]
    sheet['Name'] = sheet['Name'].str.strip()
    sheet['Name'] = Utils.nameChange(sheet['Name'])
    Solve_sheet = pd.DataFrame()
    PositionList = []
    if site == 1:
        refs = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\FDSalariesMLB.csv", skiprows=6,
                             usecols=["Nickname", "Player ID + Player Name", "Position", "Team"])
        Solve_sheet = pd.merge(left=sheet, right=refs, how="left", left_on='Name', right_on='Nickname')
        Solve_sheet = pd.merge(left=Solve_sheet, right=Schedule, how="left", left_on='Team', right_on='Team')
        Solve_sheet = Solve_sheet.rename(columns={'Position': 'Roster_Position'})
        Solve_sheet = Solve_sheet.rename(columns={'Player ID + Player Name': 'ID'})
        Solve_sheet = Solve_sheet.rename(columns={'Team': 'TeamAbbrev'})
        Solve_sheet['ID'] = Solve_sheet['ID'].astype(str)
        # ownership = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\OwnershipMLB.csv")
        # ownership = ownership.loc['Name', 'Ownership %']
        Solve_sheet = pd.merge(left=sheet, right=refs, how="left", left_on='Name', right_on='Name')
        # Solve_sheet = pd.merge(left=Solve_sheet, right=ownership, how="left", left_on='Team', right_on='Team')
        Solve_sheet = Utils.fixPositions(Solve_sheet)
        Solve_sheet = Utils.processMults(Solve_sheet, site)
        Solve_sheet = Utils.tournPrep(Solve_sheet)
        Solve_sheet['Lineups'] = 0
        Solve_sheet['Max_Exposure'] = 0
        PositionList = ["P", "C/1B", "1B", "2B", "3B", "SS", "OF", "UTIL"]
    elif site == 2:
        refs = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\DKSalariesMLB.csv", skiprows=7,
                             usecols=["Name", "Name + ID", "Salary", "Roster Position", "TeamAbbrev"])
        refs = refs.rename(columns={'Salary': 'Price'})
        Solve_sheet = pd.merge(left=sheet, right=refs, how="left", left_on='Name', right_on='Name')
        Solve_sheet = Solve_sheet.dropna(axis=0)
        Solve_sheet = pd.merge(left=Solve_sheet, right=Schedule, how="left", left_on='TeamAbbrev', right_on='Team')
        Solve_sheet = Solve_sheet.drop(columns=['Team'])
        Solve_sheet = Solve_sheet.rename(columns={'Roster Position': 'Roster_Position'})
        Solve_sheet = Solve_sheet.rename(columns={'Name + ID': 'ID'})
        Solve_sheet['ID'] = Solve_sheet['ID'].astype(str)
        Solve_sheet = Utils.processMults(Solve_sheet, site)
        PositionList = ["P", "C", "1B", "2B", "3B", "SS", "OF"]
    IDs = Utils.removeDupes(Solve_sheet['ID'].tolist())
    TeamList = Utils.removeDupes(Solve_sheet['TeamAbbrev'].tolist())
    Solve_sheet = Utils.PosIdentifiers(Solve_sheet, PositionList)
    Solve_sheet = Utils.idIdentifiers(Solve_sheet, IDs)
    Solve_sheet = Utils.idTeam(Solve_sheet, TeamList)
    Solve_sheet = Utils.tournPrep(Solve_sheet)
    Solve_sheet['Lineups'] = 0
    Solve_sheet['Max_Exposure'] = 0
    return Solve_sheet, IDs, TeamList

def PrepSolveNBA(site,sheet):
    sheet = sheet.iloc[:, 0:3]
    sheet['Name'] = sheet['Name'].str.strip()
    sheet['Name'] = Utils.nameChangeNBA(sheet['Name'])
    Solve_sheet = pd.DataFrame()
    PositionList = []
    if site == 1:
        refs = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\FDSalariesNBA.csv", skiprows=6,
                           usecols=["Nickname", "Player ID + Player Name", "Position", "Team"])
        Solve_sheet = pd.merge(left=sheet, right=refs, how="left", left_on='Name', right_on='Nickname')
        Solve_sheet = Solve_sheet.rename(columns={'Position': 'Roster_Position'})
        Solve_sheet = Solve_sheet.rename(columns={'Player ID + Player Name': 'ID'})
        Solve_sheet = Solve_sheet.rename(columns={'Team': 'TeamAbbrev'})
        Solve_sheet['ID'] = Solve_sheet['ID'].astype(str)
        Solve_sheet = Utils.processMults(Solve_sheet, site)
        PositionList = ["PG", "SG", "SF", "PF", "C"]
    elif site == 2:
        refs = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\DKSalariesNBA.csv", skiprows=7,
                           usecols=["Name", "Name + ID", "Roster Position", "TeamAbbrev"])
        Solve_sheet = pd.merge(left=sheet, right=refs, how="left", left_on='Name', right_on='Name')
        Solve_sheet = Solve_sheet.rename(columns={'Roster Position': 'Roster_Position'})
        Solve_sheet = Solve_sheet.rename(columns={'Name + ID': 'ID'})
        Solve_sheet['ID'] = Solve_sheet['ID'].astype(str)
        Solve_sheet = Utils.processMults(Solve_sheet, site)
        PositionList = ["PG", "SG", "SF", "PF", "C", "G", "F", "UTIL"]
    IDs = Utils.removeDupes(Solve_sheet['ID'].tolist())
    TeamList = Utils.removeDupes(Solve_sheet['TeamAbbrev'].tolist())
    Solve_sheet = Utils.PosIdentifiers(Solve_sheet, PositionList)
    Solve_sheet = Utils.idIdentifiers(Solve_sheet, IDs)
    Solve_sheet = Utils.idTeam(Solve_sheet, TeamList)
    return Solve_sheet, IDs, TeamList

def PrepDriver(sport,site):
    sheet, IDs, Teams = 0, 0, 0
    if sport == 1:
        sheet, IDs, Teams = PrepSolveMLB(site)
    elif sport == 2:
        sheet, IDs, Teams = PrepSolveNBA(site, sheet=pd.read_csv(
            "C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\NBA.csv"))
    return sheet, IDs, Teams


def CombinePredictions():
    NFBatters = pd.read_csv(
        'C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\NFProjections\\batters.csv',
        usecols=['Name', 'FP', 'PA', 'BB', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'SB'])
    FGBatters = pd.read_csv(
        'C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\FangraphsProjections\\FangraphsBatters.csv',
        usecols=['Name', 'DraftKings', 'Game', 'PA', 'BB', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'SB'])
    FGBatters = FGBatters.drop(FGBatters[FGBatters['Game'].str.contains('(2)',regex=False)].index)
    FGBatters = FGBatters.drop(['Game'], axis=1)
    FGBatters = FGBatters.rename(columns={'DraftKings': 'FP'})
    NFBatters['Name'] = Utils.nameChange(NFBatters['Name'])
    FGBatters['Name'] = Utils.nameChange(FGBatters['Name'])

    CombinedBatters = pd.merge(NFBatters, FGBatters, right_on='Name', left_on='Name',how='outer')
    BatterBoth = CombinedBatters[CombinedBatters['FP_x'].notna() & CombinedBatters['FP_y'].notna()]
    TempdfB = pd.DataFrame()
    TempdfB['Name'] = BatterBoth['Name']
    for col in ['FP', 'PA', 'BB', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'SB']:
        my_list = np.divide(pd.Series(BatterBoth[col+'_x'] + BatterBoth[col+'_y']),2)
        TempdfB[col] = my_list.values
    BatterBoth = TempdfB.copy()

    BatterNF = CombinedBatters[CombinedBatters['FP_x'].notna() & CombinedBatters['FP_y'].isna()]
    if len(BatterNF) > 0:
        BatterNF = BatterNF.dropna(axis=1)
        BatterNF.columns = ['Name', 'FP', 'PA', 'BB', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'SB']
    BatterFG = CombinedBatters[CombinedBatters['FP_y'].notna() & CombinedBatters['FP_x'].isna()]
    BatterFG = BatterFG.dropna(axis=1)
    BatterFG.columns = ['Name', 'PA', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'SB', 'BB', 'FP']
    BatterFinal = pd.concat([BatterBoth, BatterFG, BatterNF], ignore_index=True)




    NFPitchers = pd.read_csv(
        'C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\NFProjections\\pitchers.csv',
        usecols=['Name', 'FP', 'W', 'IP', 'Ha', 'K', 'BBa', 'ER'])
    FGPitchers = pd.read_csv(
        'C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\FangraphsProjections\\FangraphsPitchers.csv',
        usecols=['Name', 'DraftKings', 'W', 'IP', 'TBF', 'Ha', 'K', 'BBa'])
    NFPitchers['TBF'] = NFPitchers.IP*3 + NFPitchers.Ha + NFPitchers.BBa
    FGPitchers['ER'] = ((FGPitchers.Ha + FGPitchers.BBa)/FGPitchers.IP * 6.8 - 5)/9*FGPitchers.IP
    FGPitchers = FGPitchers.dropna(axis=0)
    FGPitchers = FGPitchers[FGPitchers['ER'] > 0]
    FGPitchers = FGPitchers[FGPitchers['DraftKings'] > 7]

    FGPitchers = FGPitchers.rename(columns={'DraftKings': 'FP'})
    NFPitchers['Name'] = Utils.nameChange(NFPitchers['Name'])
    FGPitchers['Name'] = Utils.nameChange(FGPitchers['Name'])




    CombinedPitchers = pd.merge(NFPitchers, FGPitchers, right_on='Name', left_on='Name', how='outer')
    CombinedPitchers['Name'] = Utils.nameChange(CombinedPitchers['Name'])
    PitcherBoth = CombinedPitchers[CombinedPitchers['FP_x'].notna() & CombinedPitchers['FP_y'].notna()]

    TempdfP = pd.DataFrame()
    TempdfP['Name'] = PitcherBoth['Name']
    for col in ['FP', 'W', 'IP', 'TBF','Ha', 'K', 'BBa','ER']:
        my_list = np.divide(pd.Series(PitcherBoth[col+'_x'] + PitcherBoth[col+'_y']),2)
        TempdfP[col] = my_list.values
    PitcherBoth = TempdfP.copy()
    PitcherNF = CombinedPitchers[CombinedPitchers['FP_x'].notna() & CombinedPitchers['FP_y'].isna()]
    PitcherNF = PitcherNF.dropna(axis=1)
    if len(PitcherNF) > 0:
        PitcherNF.columns = ['Name', 'FP', 'W', 'IP', 'TBF', 'Ha', 'K', 'ER', 'BBa']
    PitcherFG = CombinedPitchers[CombinedPitchers['FP_y'].notna() & CombinedPitchers['FP_x'].isna()]
    PitcherFG = PitcherFG.dropna(axis=1)
    PitcherFG.columns = ['Name', 'W', 'IP', 'TBF', 'Ha', 'BBa', 'K','FP', 'ER']
    PitcherFinal = pd.concat([PitcherBoth, PitcherFG, PitcherNF], ignore_index=True)

    BatterFinal = BatterFinal.loc[:, ['Name', 'FP', 'PA', 'BB', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'SB']]
    PitcherFinal = PitcherFinal.loc[:, ['Name', 'FP', 'TBF', 'IP', 'W', 'Ha', 'BBa', 'ER', 'K']]


    PitcherFinal.to_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\PitcherCombined.csv")
    BatterFinal.to_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\BatterCombined.csv")

def SimPrep(site):
    batters = Utils.MLBvarAdjBats(pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\BatterCombined.csv"),2)
    pitchers = Utils.MLBvarAdjPits(pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\Projections\\PitcherCombined.csv"),2)
    ownership = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\ownershipMLB.csv",
                            usecols=['Name', 'Salary', 'Team', 'Opponent', 'Ownership %'])

    ownership = ownership.rename(columns={'Ownership %': 'Ownership'})
    ownership['Name'] = Utils.nameChange(ownership['Name'])
    orderPos = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\BattingOrders.csv")
    orderPos['Name'] = Utils.nameChange(orderPos['Name'])
    pitchers = pitchers[pitchers['FP'] > 8]
    sheet = pd.concat([batters, pitchers], axis=0, sort=False)
    sheet['Name'] = Utils.nameChange(sheet['Name'])
    refs = pd.read_csv("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\DKSalariesMLB.csv", skiprows=7,
                       usecols=["Name", "Name + ID", 'Salary', "Roster Position", "TeamAbbrev"])
    refs = refs.rename(columns={'Salary': 'Price'})
    Solve_sheet = pd.merge(left=sheet, right=refs, how="inner", left_on='Name', right_on='Name')
    Solve_sheet = pd.merge(left=Solve_sheet, right=ownership, how="left", left_on='Name', right_on='Name')

    Solve_sheet = pd.merge(left=Solve_sheet, right=orderPos, how="right", left_on='Name', right_on='Name')
    Solve_sheet = Solve_sheet.drop(Solve_sheet[((Solve_sheet['TeamAbbrev'] == 'TEX') | (Solve_sheet['TeamAbbrev'] == 'HOU') | (Solve_sheet['TeamAbbrev'] == 'ATL')) & (Solve_sheet['Pos'] != '0')].index)
    Solve_sheet = Solve_sheet.drop(Solve_sheet[(Solve_sheet['TeamAbbrev'] == 'WAS') & (Solve_sheet['Pos'] == '0')].index)
    Solve_sheet = Solve_sheet[Solve_sheet['FP'].notna()]
    Solve_sheet = Solve_sheet.rename(columns={'Roster Position': 'Roster_Position'})
    Solve_sheet = Solve_sheet.rename(columns={'Name + ID': 'ID'})
    Solve_sheet['ID'] = Solve_sheet['ID'].astype(str)
    Solve_sheet = Solve_sheet.loc[:, ['ID', 'TeamAbbrev', 'Roster_Position', 'Pos', 'FP', 'Variance', 'Price', 'Ownership']]

    return Solve_sheet



