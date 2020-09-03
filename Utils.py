import re
import pandas as pd
import numpy as np
from scipy import stats


def parseDigit(string):
    numbers = []
    endnum = ""
    string = re.findall(".",string)
    for word in string:
        if digOrDecimal(word):
            numbers.append(word)
    for item in numbers:
        endnum = endnum+item
    return endnum


def digOrDecimal(string):
    if string.isdigit():
        return True
    elif string == '.':
        return True
    else:
        return False


def parseName(string):
    return re.sub('\s+',' ',string)


def alphOrDec(string):
    if string.isalpha():
        return True
    elif string == '.':
        return True
    else:
        return False


def nameChange(series):
    for item in series:
        if item == 'Ronald Acuna':
            series = series.str.replace('Ronald Acuna', 'Ronald Acuna Jr.', regex=False)
        series = series.str.replace('Michael Brosseau', 'Mike Brosseau', regex=False)
        if item == 'Steven Souza':
            series = series.str.replace('Steven Souza', 'Steven Souza Jr.', regex=False)
        series = series.str.replace('D.J. Stewart', 'DJ Stewart', regex=False)
        series = series.str.replace('Jake Junis', 'Jakob Junis', regex=False)
        series = series.str.replace('Enrique Hernandez', 'Kike Hernandez', regex=False)
        series = series.str.replace('Giovanny Urshela', 'Gio Urshela', regex=False)
        series = series.str.replace('Yulieski Gurriel', 'Yuli Gurriel', regex=False)
        series = series.str.replace('Hyun-jin Ryu', 'Hyun Jin Ryu', regex=False)
        if item == 'Lourdes Gurriel':
            series = series.str.replace('Lourdes Gurriel', 'Lourdes Gurriel Jr.', regex=False)
        series = series.str.replace('Dan Vogelbach', 'Daniel Vogelbach', regex=False)
        series = series.str.replace('Robert Refsnyder', 'Rob Refsnyder', regex=False)
        series = series.str.replace('Philip Gosselin', 'Phil Gosselin', regex=False)
        if item == 'Jackie Bradley':
            series = series.str.replace('Jackie Bradley', 'Jackie Bradley Jr.', regex=False)
        if item == 'Shed Long':
            series = series.str.replace('Shed Long', 'Shed Long Jr.', regex=False)
        series = series.str.replace('Matthew Joyce', 'Matt Joyce', regex=False)
        series = series.str.replace('Matt Boyd', 'Matthew Boyd', regex=False)
        series = series.str.replace('Vincent Velasquez', 'Vince Velasquez', regex=False)
        series = series.str.replace('A.J. Pollock', 'AJ Pollock', regex=False)
        series = series.str.replace('Delino DeShields Jr.', 'Delino DeShields', regex=False)
        series = series.str.replace('J.R. Murphy', 'John Ryan Murphy', regex=False)
        series = series.str.replace('Nicholas Castellanos', 'Nick Castellanos', regex=False)
        if item == 'LaMonte Wade Jr':
            series = series.str.replace('LaMonte Wade Jr', 'LaMonte Wade Jr.', regex=False)
        if item == 'Fernando Tatis':
            series = series.str.replace('Fernando Tatis', 'Fernando Tatis JR.', regex=False)


    return series

def nameChangeNBA(series):
    series = series.str.replace('Jose Juan Barea', 'J.J. Barea')
    series = series.str.replace('Terence Davis II', 'Terence Davis')
    series = series.str.replace('P.J. Dozier', 'PJ Dozier')
    series = series.str.replace('T.J. Leaf', 'TJ Leaf')
    series = series.str.replace('JaKarr Sampson', 'Jakarr Sampson')
    series = series.str.replace('Frank Mason', 'Frank Mason III')
    series = series.str.replace('Patrick Mills', 'Patty Mills')
    series = series.str.replace('Mohamed Bamba', 'Mo Bamba')
    series = series.str.replace('Luc Mbah a Moute', 'Luc Richard Mbah a Moute')
    series = series.str.replace('Luc Mbah a Moute', 'Luc Richard Mbah a Moute')
    series = series.str.replace('Wesley Iwundu', 'Wes Iwundu')
    series = series.str.replace('James Ennis', 'James Ennis III')
    series = series.str.replace('Lonnie Walker', 'Lonnie Walker IV')
    series = series.str.replace('Harry Giles', 'Harry Giles III')
    series = series.str.replace('J.J. Redick', 'JJ Redick')
    series = series.str.replace('Ishmael Smith', 'Ish Smith')
    series = series.str.replace('C.J. McCollum', 'CJ McCollum')
    series = series.str.replace('Troy Brown', 'Troy Brown Jr.')
    series = series.str.replace('Louis Williams', 'Lou Williams')
    series = series.str.replace('Marcus Morris', 'Marcus Morris Sr.')
    return series


def processMults(multiPos,site):
    sepPosFrame = pd.DataFrame(columns=['Name', 'FP', 'Price', 'ID', 'Roster_Position','TeamAbbrev'])
    if site == 1:
        for i in range(0, len(multiPos)):
            tempEntry = pd.DataFrame(multiPos.iloc[i, :])
            tempEntry = tempEntry.transpose()
            for item in multiPos.iloc[i, :]['Roster_Position'].split(','):
                newEntry = tempEntry
                newEntry['Roster_Position'] =item
                sepPosFrame = pd.concat([sepPosFrame, newEntry], ignore_index=True,sort=False)
    elif site == 2:
        for i in range(0, len(multiPos)):
            tempEntry = pd.DataFrame(multiPos.iloc[i, :])
            tempEntry = tempEntry.transpose()
            for item in multiPos.iloc[i, :]['Roster_Position'].split('/'):
                newEntry = tempEntry
                newEntry['Roster_Position'] =item
                sepPosFrame = pd.concat([sepPosFrame, newEntry], ignore_index=True,sort=False)
    return sepPosFrame


def removeDupes(List):
    return list(dict.fromkeys(List))


def PosIdentifiers(df,positionList):
    for item in positionList:
        df[item] = 0
        df[item] = np.where((df.Roster_Position == item), 1, 0)
    return df



def idIdentifiers(df,IDList):
    for item in IDList:
        df[item] = 0
        df[item] = np.where((df.ID == item), 1, 0)
    return df


def idTeam(df,TeamList):
    for item in TeamList:
        df[item] = 0
        df[item] = np.where((df.TeamAbbrev == item), 1, 0)
    return df

def fixPositions(df):
    df['Roster_Position'] = np.where((df.Roster_Position == 'C'), 'C/1B', df.Roster_Position)
    df['Roster_Position'] = np.where((df.Roster_Position == '1B'), 'C/1B', df.Roster_Position)
    df['Roster_Position'] = np.where((df.Roster_Position != 'P'), df.Roster_Position+",UTIL", df.Roster_Position)
    return df

def MLBvarAdjBats(df,site):
    valList = []
    if site == 1:
        valList = [3, 2, 6, 9, 12, 3.2, 3.5, 6]
    elif site == 2:
        valList = [2, 3, 5, 8, 10, 2, 2, 5]
    varAdjListTemp = []
    for index, player in df.iterrows():
        tempPartials = []
        PA = player['PA']
        for i in range(len(valList)):
            OneAB = player[4+i]/PA
            var = PA*(OneAB*(valList[i]-OneAB)**2)
            tempPartials.append(var)
        varAdjListTemp.append(sum(tempPartials))
    average = sum(varAdjListTemp)/len(varAdjListTemp)
    varAdjList = [x/average for x in varAdjListTemp]
    varAdjFinal = np.multiply(df['FP'].tolist(), varAdjList)
    varAdjFinal = pd.Series(varAdjFinal)
    Variance = pd.Series(varAdjListTemp)
    df['Variance'] = Variance
    df['VarAdj'] = varAdjFinal.values
    return df

def MLBvarAdjPits(df,site):
    valList = []
    df = df[df['TBF'] > 5].copy()
    df = df[df['W'] > .05].copy()
    df = df.reset_index()

    if site == 1:
        valList = [6, 3, 0, 3, 3, 0]
    elif site == 2:
        valList = [2.25, 4, .6, .6, 2, 2]
    varAdjListTemp = []
    for index, player in df.iterrows():
        tempPartials = []
        TBF = player['TBF']
        for i in range(len(valList)):
            if i == 1:
                xk = [valList[i], 0]
                pk = (player[5+i], 1-player[5+i])
                custm = stats.rv_discrete(name='custm', values=(xk, pk))
                tempPartials.append(custm.var())
            else:
                OneAB = player[5 + i] / TBF
                var = TBF * (OneAB * (valList[i] - OneAB) ** 2)
                tempPartials.append(var)
        varAdjListTemp.append(sum(tempPartials))
    average = sum(varAdjListTemp) / len(varAdjListTemp)
    varAdjList = [x / average for x in varAdjListTemp]
    varAdjFinal = np.multiply(df['FP'].tolist(), varAdjList)
    varAdjFinal = pd.Series(varAdjFinal)
    Variance = pd.Series(varAdjListTemp)
    df['Variance'] = Variance
    df['VarAdj'] = varAdjFinal.values

    return df

def tournPrep(sheet):
    pitchers = sheet[sheet['Roster_Position'] == 'P']
    for index, row in pitchers.iterrows():
        Opp = row['Opponent']
        indices = sheet[sheet['TeamAbbrev'] == Opp]['ID']
        for item in indices:
            sheet.loc[index, item] = 1
    return sheet

def reprocessList(Lineup):
    Lineup = Lineup.replace("'", "")
    Lineup = Lineup.replace("[", "")
    Lineup = Lineup.replace("]", "")
    Lineup = Lineup.split(',')
    Lineup = [entry.strip() for entry in Lineup]
    return Lineup
