import pandas as pd
import numpy as np
import cvxpy


def MLBSolve(site,sheet,IDList,lineups):
    LineupText = ""
    totalSalary  = 0
    sheet['Max_Exposure'] = np.where((sheet.Roster_Position == 'P'), int(round(1*lineups/2)), sheet.Max_Exposure)
    sheet['Max_Exposure'] = np.where((sheet.Roster_Position == 'C'), int(round(1*lineups/2)), sheet.Max_Exposure)
    sheet['Max_Exposure'] = np.where((sheet.Roster_Position == '1B'), int(round(.4*lineups/2)), sheet.Max_Exposure)
    sheet['Max_Exposure'] = np.where((sheet.Roster_Position == '2B'), int(round(.4*lineups/2)), sheet.Max_Exposure)
    sheet['Max_Exposure'] = np.where((sheet.Roster_Position == '3B'), int(round(.4*lineups/2)), sheet.Max_Exposure)
    sheet['Max_Exposure'] = np.where((sheet.Roster_Position == 'SS'), int(round(.5*lineups/2)), sheet.Max_Exposure)
    sheet['Max_Exposure'] = np.where((sheet.Roster_Position == 'OF'), int(round(.3*lineups/2)), sheet.Max_Exposure)
    OPriceSheet = sheet.copy()
    fullSheet = sheet.copy()
    if site == 1:
        totalSalary = 35000
        LineupText = "P,C/1B,2B,3B,SS,OF,OF,OF,UTIL\n"
    elif site == 2:
        totalSalary = 50000
        LineupText = "P,P,C,1B,2B,3B,SS,OF,OF,OF\n"
    for stat in ('FP', 'VarAdj'):
        goodLineups = 0
        Threshold_Score = 0
        if stat == 'VarAdj':
            LineupText = LineupText + "GPP \n"
            fullSheet['Lineups'] = 0
            fullSheet['Exposure'] = 0
        while goodLineups < lineups/2:
            if goodLineups > 0:
                print(goodLineups)
                sheet = fullSheet.sample(frac=.7)
                fullSheet['Exposure'] = 0
            fullSheet['Price'] = np.where((fullSheet.Lineups >= fullSheet.Max_Exposure), 99999, OPriceSheet['Price'])
            selection = cvxpy.Variable(shape=len(sheet['Price']), boolean=True)
            constraint_list = []
            for item in IDList:
                constraint_list.append(sheet[item].tolist()@selection <= 1)
            constraint_list.append(sheet['Price'].tolist() @ selection <= totalSalary)
            if site == 1:
                constraint_list.append(sheet['P'].tolist() @ selection == 1)
                constraint_list.append(sheet['C/1B'].tolist() @ selection == 1)
                constraint_list.append(sheet['UTIL'].tolist() @ selection == 1)
            elif site == 2:
                constraint_list.append(sheet['P'].tolist() @ selection == 2)
                constraint_list.append(sheet['C'].tolist() @ selection == 1)
                constraint_list.append(sheet['1B'].tolist() @ selection == 1)
            constraint_list.append(sheet['2B'].tolist() @ selection == 1)
            constraint_list.append(sheet['3B'].tolist() @ selection == 1)
            constraint_list.append(sheet['SS'].tolist() @ selection == 1)
            constraint_list.append(sheet['OF'].tolist() @ selection == 3)

            points = sheet[stat].tolist() @ selection

            MLB_DFS = cvxpy.Problem(cvxpy.Maximize(points), constraint_list)
            if MLB_DFS.status in ["infeasible", "unbounded"]:
                continue
            MLB_DFS.solve(solver=cvxpy.GLPK_MI)
            sheet['Exposure'] = selection.value
            RawLineup = sheet[sheet['Exposure'] == 1]
            ##get exposure from RawLineup to fullsheet
            fullSheet['Exposure'] = np.where(np.isin(fullSheet['ID'], RawLineup['ID']),1,0)
            FixedLineup = pd.DataFrame()

            if site == 1:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'P']\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'C/1B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == '2B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == '3B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SS']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'OF'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'UTIL'])
            elif site == 2:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'P']\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'C'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == '1B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == '2B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == '3B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SS']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'OF'])

            Solution =FixedLineup['ID'].tolist()
            Solution.append(str(sum(RawLineup[stat].tolist())))
            Score = float(Solution[-1])
            if goodLineups == 0:
                Threshold_Score = float(Solution[-1])
            if Score >= .8*Threshold_Score:
                fullSheet['Lineups'] = np.where(fullSheet['Exposure'] == 1,fullSheet['Lineups']+1, fullSheet['Lineups'])
                goodLineups = goodLineups+1
                for entry in Solution:
                    LineupText = LineupText + entry + ","
                LineupText = LineupText + "\n"
    return Threshold_Score, LineupText


def MLBsolveStack(site, sheet, IDList, teamList, Threshold_Score):
    totalSalary  = 0
    if site == 1:
        totalSalary = 35000
    elif site == 2:
        totalSalary = 50000
    LineupText = ""
    activeTeams = []
    for team in teamList:
        if sheet[team].tolist != [0]*len(sheet[team].tolist()):
            activeTeams.append(team)
    for team in activeTeams:
        for stackDepth in range(3, 6):
            selection = cvxpy.Variable(shape=len(sheet['Price']), boolean=True)
            constraint_list = []
            constraint_list.append(sheet[team].tolist()@selection == stackDepth)

            for item in IDList:
                constraint_list.append(sheet[item].tolist()@selection <= 1)

            constraint_list.append(sheet['Price'].tolist() @ selection <= totalSalary)
            if site == 1:
                constraint_list.append(sheet['P'].tolist() @ selection == 1)
                constraint_list.append(sheet['C/1B'].tolist() @ selection == 1)
                constraint_list.append(sheet['UTIL'].tolist() @ selection == 1)
            if site == 2:
                constraint_list.append(sheet['P'].tolist() @ selection == 2)
                constraint_list.append(sheet['C'].tolist() @ selection == 1)
                constraint_list.append(sheet['1B'].tolist() @ selection == 1)

            constraint_list.append(sheet['2B'].tolist() @ selection == 1)
            constraint_list.append(sheet['3B'].tolist() @ selection == 1)
            constraint_list.append(sheet['SS'].tolist() @ selection == 1)
            constraint_list.append(sheet['OF'].tolist() @ selection == 3)

            points = sheet['VarAdj'].tolist() @ selection

            MLB_DFS = cvxpy.Problem(cvxpy.Maximize(points), constraint_list)
            if MLB_DFS.status in ["infeasible", "unbounded"]:
                continue
            MLB_DFS.solve(solver=cvxpy.GLPK_MI)
            sheet['Exposure'] = selection.value
            RawLineup = sheet[sheet['Exposure'] == 1]
            FixedLineup = pd.DataFrame()
            if site == 1:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'P']\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'C/1B']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == '2B']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == '3B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SS']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'OF'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'UTIL'])
            elif site == 2:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'P']\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'C']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == '1B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == '2B']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == '3B'])\
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SS']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'OF'])

            Solution =FixedLineup['ID'].tolist()
            Solution.append(team)
            Solution.append(str(sum(RawLineup['VarAdj'].tolist())))
            Score = float(Solution[-1])
            if Score >= .95*Threshold_Score:
                for entry in Solution:
                    LineupText = LineupText + entry + ","
                LineupText = LineupText + "\n"

    return LineupText

def MLBDubsolveStack(site, sheet, IDList, teamList, Threshold_Score):
    totalSalary  = 0
    if site == 1:
        totalSalary = 35000
    elif site == 2:
        totalSalary = 50000
    LineupText = ""
    activeTeams = []
    for team in teamList:
        if sheet[team].tolist != [0]*len(sheet[team].tolist()):
            activeTeams.append(team)
    for team in activeTeams:
        for team2 in activeTeams:
            if team == team2:
                continue
            for stackDepth in range(3,5):
                selection = cvxpy.Variable(shape=len(sheet['Price']), boolean=True)
                constraint_list = []
                constraint_list.append(sheet[team].tolist()@selection == stackDepth)
                constraint_list.append(sheet[team2].tolist()@selection == stackDepth)

                for item in IDList:
                    constraint_list.append(sheet[item].tolist()@selection <= 1)

                constraint_list.append(sheet['Price'].tolist() @ selection <= totalSalary)
                if site == 1:
                    constraint_list.append(sheet['P'].tolist() @ selection == 1)
                    constraint_list.append(sheet['C/1B'].tolist() @ selection == 1)
                    constraint_list.append(sheet['UTIL'].tolist() @ selection == 1)
                if site == 2:
                    constraint_list.append(sheet['P'].tolist() @ selection == 2)
                    constraint_list.append(sheet['C'].tolist() @ selection == 1)
                    constraint_list.append(sheet['1B'].tolist() @ selection == 1)

                constraint_list.append(sheet['2B'].tolist() @ selection == 1)
                constraint_list.append(sheet['3B'].tolist() @ selection == 1)
                constraint_list.append(sheet['SS'].tolist() @ selection == 1)
                constraint_list.append(sheet['OF'].tolist() @ selection == 3)

                points = sheet['VarAdj'].tolist() @ selection

                MLB_DFS = cvxpy.Problem(cvxpy.Maximize(points), constraint_list)
                if MLB_DFS.status in ["infeasible", "unbounded"]:
                    continue
                MLB_DFS.solve(solver=cvxpy.GLPK_MI)
                sheet['Exposure'] = selection.value
                RawLineup = sheet[sheet['Exposure'] == 1]
                FixedLineup = pd.DataFrame()
                if site == 1:
                    FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'P']\
                        .append(RawLineup[RawLineup['Roster_Position'] == 'C/1B']) \
                        .append(RawLineup[RawLineup['Roster_Position'] == '2B']) \
                        .append(RawLineup[RawLineup['Roster_Position'] == '3B'])\
                        .append(RawLineup[RawLineup['Roster_Position'] == 'SS']) \
                        .append(RawLineup[RawLineup['Roster_Position'] == 'OF'])\
                        .append(RawLineup[RawLineup['Roster_Position'] == 'UTIL'])
                elif site == 2:
                    FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'P']\
                        .append(RawLineup[RawLineup['Roster_Position'] == 'C']) \
                        .append(RawLineup[RawLineup['Roster_Position'] == '1B'])\
                        .append(RawLineup[RawLineup['Roster_Position'] == '2B']) \
                        .append(RawLineup[RawLineup['Roster_Position'] == '3B'])\
                        .append(RawLineup[RawLineup['Roster_Position'] == 'SS']) \
                        .append(RawLineup[RawLineup['Roster_Position'] == 'OF'])

                Solution =FixedLineup['ID'].tolist()
                Solution.append(str(sum(RawLineup['VarAdj'].tolist())))
                Score = float(Solution[-1])
                if Score >= .95*Threshold_Score:
                    for entry in Solution:
                        LineupText = LineupText + entry + ","
                    LineupText = LineupText + "\n"

    return LineupText
