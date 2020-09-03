import pandas as pd
import cvxpy



def NBASolve(site, sheet, IDList, lineups):
    totalSalary  = 0
    LineupText = ""
    if site == 1:
        totalSalary = 60000
        LineupText = "PG,PG,SG,SG,SF,SF,PF,PF,C\n"
    elif site == 2:
        totalSalary = 50000
        LineupText = "PG,SG,SF,PF,C,G,F,UTIL\n"

    goodLineups = 0
    Threshold_Score = 0
    fullSheet = sheet


    while goodLineups < lineups:
        if goodLineups > 0:
            sheet = fullSheet.sample(frac=.7)
        selection = cvxpy.Variable(shape=len(sheet['Price']), boolean=True)
        constraint_list = []
        for item in IDList:
            constraint_list.append(sheet[item].tolist()@selection <= 1)

        constraint_list.append(sheet['Price'].tolist() @ selection <= totalSalary)
        if site == 1:
            constraint_list.append(sheet['PG'].tolist() @ selection == 2)
            constraint_list.append(sheet['SG'].tolist() @ selection == 2)
            constraint_list.append(sheet['SF'].tolist() @ selection == 2)
            constraint_list.append(sheet['PF'].tolist() @ selection == 2)
            constraint_list.append(sheet['C'].tolist() @ selection == 1)
        elif site == 2:
            constraint_list.append(sheet['PG'].tolist() @ selection == 1)
            constraint_list.append(sheet['SG'].tolist() @ selection == 1)
            constraint_list.append(sheet['SF'].tolist() @ selection == 1)
            constraint_list.append(sheet['PF'].tolist() @ selection == 1)
            constraint_list.append(sheet['C'].tolist() @ selection == 1)
            constraint_list.append(sheet['G'].tolist() @ selection == 1)
            constraint_list.append(sheet['F'].tolist() @ selection == 1)
            constraint_list.append(sheet['UTIL'].tolist() @ selection == 1)

        points = sheet['FP'].tolist() @ selection

        NBA_DFS = cvxpy.Problem(cvxpy.Maximize(points), constraint_list)
        NBA_DFS.solve(solver=cvxpy.GLPK_MI)
        sheet['Exposure'] = selection.value
        RawLineup = sheet[sheet['Exposure'] == 1]
        FixedLineup = pd.DataFrame()

        if site == 1:
            FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'PG']\
                .append(RawLineup[RawLineup['Roster_Position'] == 'SG'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'SF'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'PF'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'C'])
        elif site == 2:
            FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'PG']\
                .append(RawLineup[RawLineup['Roster_Position'] == 'SG'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'SF'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'PF'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'C'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'G']) \
                .append(RawLineup[RawLineup['Roster_Position'] == 'F'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'UTIL'])

        Solution =FixedLineup['ID'].tolist()
        Solution.append(str(sum(RawLineup['FP'].tolist())))
        Score = float(Solution[-1])
        if goodLineups == 0:
            Threshold_Score = float(Solution[-1])
        if Score >=.95*Threshold_Score:
            goodLineups = goodLineups+1
            for entry in Solution:
                LineupText = LineupText + entry + ","
            LineupText = LineupText + "\n"


    return Threshold_Score, LineupText


def NBAsolveStack(site, sheet, IDList, teamList, Threshold_Score):
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
        for stackDepth in range(3,6):
            selection = cvxpy.Variable(shape=len(sheet['Price']), boolean=True)
            constraint_list = []
            constraint_list.append(sheet[team].tolist()@selection == stackDepth)

            for item in IDList:
                constraint_list.append(sheet[item].tolist()@selection <= 1)

            constraint_list.append(sheet['Price'].tolist() @ selection <= totalSalary)
            if site == 1:
                constraint_list.append(sheet['PG'].tolist() @ selection == 2)
                constraint_list.append(sheet['SG'].tolist() @ selection == 2)
                constraint_list.append(sheet['SF'].tolist() @ selection == 2)
                constraint_list.append(sheet['PF'].tolist() @ selection == 2)
                constraint_list.append(sheet['C'].tolist() @ selection == 1)
            elif site == 2:
                constraint_list.append(sheet['PG'].tolist() @ selection == 1)
                constraint_list.append(sheet['SG'].tolist() @ selection == 1)
                constraint_list.append(sheet['SF'].tolist() @ selection == 1)
                constraint_list.append(sheet['PF'].tolist() @ selection == 1)
                constraint_list.append(sheet['C'].tolist() @ selection == 1)
                constraint_list.append(sheet['G'].tolist() @ selection == 1)
                constraint_list.append(sheet['F'].tolist() @ selection == 1)
                constraint_list.append(sheet['UTIL'].tolist() @ selection == 1)

            points = sheet['FP'].tolist() @ selection

            NBA_DFS = cvxpy.Problem(cvxpy.Maximize(points), constraint_list)
            NBA_DFS.solve(solver=cvxpy.GLPK_MI)
            sheet['Exposure'] = selection.value
            RawLineup = sheet[sheet['Exposure'] == 1]
            FixedLineup = pd.DataFrame()

            if site == 1:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'PG'] \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SG']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SF']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'PF']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'C'])
            elif site == 2:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'PG'] \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SG']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'SF']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'PF']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'C']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'G']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'F']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'UTIL'])
            Solution =FixedLineup['ID'].tolist()
            Solution.append(str(sum(RawLineup['FP'].tolist())))
            Score = float(Solution[-1])
            if Score >= .95*Threshold_Score:
                for entry in Solution:
                    LineupText = LineupText + entry + ","
                LineupText = LineupText + "\n"

    return LineupText