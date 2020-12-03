import pandas as pd
import cvxpy



def NFLSolve(site, sheet, IDList, lineups):
    totalSalary  = 0
    LineupText = ""
    if site == 1:
        totalSalary = 60000
        LineupText = "QB,RB,RB,WR,WR,WR,TE,FLEX,D\n"
    elif site == 2:
        totalSalary = 50000
        LineupText = "QB,RB,RB,WR,WR,WR,TE,FLEX,DST\n"

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
            constraint_list.append(sheet['QB'].tolist() @ selection == 1)
            constraint_list.append(sheet['RB'].tolist() @ selection == 2)
            constraint_list.append(sheet['WR'].tolist() @ selection == 3)
            constraint_list.append(sheet['TE'].tolist() @ selection == 1)
            constraint_list.append(sheet['FLEX'].tolist() @ selection == 1)
            constraint_list.append(sheet['D'].tolist() @ selection == 1)

        elif site == 2:
            constraint_list.append(sheet['QB'].tolist() @ selection == 1)
            constraint_list.append(sheet['RB'].tolist() @ selection == 2)
            constraint_list.append(sheet['WR'].tolist() @ selection == 3)
            constraint_list.append(sheet['TE'].tolist() @ selection == 1)
            constraint_list.append(sheet['FLEX'].tolist() @ selection == 1)
            constraint_list.append(sheet['DST'].tolist() @ selection == 1)

        points = sheet['FP'].tolist() @ selection

        NFL_DFS = cvxpy.Problem(cvxpy.Maximize(points), constraint_list)
        NFL_DFS.solve(solver=cvxpy.GLPK_MI)
        sheet['Exposure'] = selection.value
        RawLineup = sheet[sheet['Exposure'] == 1]
        Solution = ""
        if site == 1:
            FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'QB']\
                .append(RawLineup[RawLineup['Roster_Position'] == 'RB'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'WR'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'TE'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'FLEX'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'D'])
            Solution =FixedLineup['Name + ID'].tolist()

        elif site == 2:
            FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'QB']\
                .append(RawLineup[RawLineup['Roster_Position'] == 'RB'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'WR'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'TE'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'FLEX'])\
                .append(RawLineup[RawLineup['Roster_Position'] == 'DST'])
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


def NFLsolveStack(site, sheet, IDList, teamList, Threshold_Score):
    totalSalary  = 0
    if site == 1:
        totalSalary = 60000
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
                constraint_list.append(sheet['QB'].tolist() @ selection == 1)
                constraint_list.append(sheet['RB'].tolist() @ selection == 2)
                constraint_list.append(sheet['WR'].tolist() @ selection == 3)
                constraint_list.append(sheet['TE'].tolist() @ selection == 1)
                constraint_list.append(sheet['FLEX'].tolist() @ selection == 1)
                constraint_list.append(sheet['D'].tolist() @ selection == 1)

            elif site == 2:
                constraint_list.append(sheet['QB'].tolist() @ selection == 1)
                constraint_list.append(sheet['RB'].tolist() @ selection == 2)
                constraint_list.append(sheet['WR'].tolist() @ selection == 3)
                constraint_list.append(sheet['TE'].tolist() @ selection == 1)
                constraint_list.append(sheet['FLEX'].tolist() @ selection == 1)
                constraint_list.append(sheet['DST'].tolist() @ selection == 1)
            points = sheet['FP'].tolist() @ selection

            NFL_DFS = cvxpy.Problem(cvxpy.Maximize(points), constraint_list)
            NFL_DFS.solve(solver=cvxpy.GLPK_MI)
            sheet['Exposure'] = selection.value
            RawLineup = sheet[sheet['Exposure'] == 1]
            Solution = ""
            if site == 1:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'QB'] \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'RB']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'WR']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'TE']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'FLEX']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'DST'])
                Solution =FixedLineup['Name + ID'].tolist()

            elif site == 2:
                FixedLineup = RawLineup[RawLineup['Roster_Position'] == 'QB'] \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'RB']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'WR']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'TE']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'FLEX']) \
                    .append(RawLineup[RawLineup['Roster_Position'] == 'DST'])
                Solution =FixedLineup['ID'].tolist()
            Solution.append(str(sum(RawLineup['FP'].tolist())))
            Score = float(Solution[-1])
            if Score >= .95*Threshold_Score:
                for entry in Solution:
                    LineupText = LineupText + entry + ","
                LineupText = LineupText + "\n"

    return LineupText