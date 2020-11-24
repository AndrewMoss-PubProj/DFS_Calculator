import dfsSolverMLB
import dfsSolverNBA
import dfsSolverNFL
import nFScrape
import PrepSolve
import os

sport = int(input("Which Sport do you want to play DFS for? \n 1-MLB \n 2-NBA \n 3-NFL"))
lineups = int(input("How many lineups (before best stacks) do you want to make"))
site = int(nFScrape.scrapeDriver(sport))
sheet, IDs, Teams = PrepSolve.PrepDriver(sport, site)
if sport == 1:
    Threshold_Score, LineupText = dfsSolverMLB.MLBSolve(site, sheet, IDs, lineups)
    LineupTextStack = "" #+ dfsSolverMLB.MLBsolveStack(site, sheet, IDs, Teams, Threshold_Score)
    LineupText = LineupText + "Stacks \n" + LineupTextStack + "Double Stacks \n"
                 # dfsSolverMLB.MLBDubsolveStack(site, sheet, IDs, Teams, Threshold_Score)
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\MLBLineups.csv"), "wb")
    file.write(bytes(LineupText, encoding="ascii,", errors="ignore"))
if sport == 2:
    Threshold_Score, LineupText = dfsSolverNBA.NBASolve(site, sheet, IDs, lineups)
    LineupTextStack = dfsSolverNBA.NBAsolveStack(site, sheet, IDs, Teams, Threshold_Score)
    LineupText = LineupText + "Stacks \n" + LineupTextStack
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\NBALineups.csv"), "wb")
    file.write(bytes(LineupText, encoding="ascii,", errors="ignore"))
if sport == 3:
    Threshold_Score, LineupText = dfsSolverNFL.NFLSolve(site, sheet, IDs, lineups)
    LineupTextStack = dfsSolverNFL.NFLsolveStack(site, sheet, IDs, Teams, Threshold_Score)
    LineupText = LineupText + "Stacks \n" + LineupTextStack
    file = open(os.path.expanduser("C:\\Users\\Andrew Moss\\PycharmProjects\\DFS_Calculator\\NFLLineups.csv"), "wb")
    file.write(bytes(LineupText, encoding="ascii,", errors="ignore"))


