import Positions_Traits as posT
from operator import itemgetter
import math

year_2012 = "_2012"
year_2011 = "_2011"
year_2017 = "_2017"
year_2018 = "_2018"


def updateValue(lst, idx, occrs):
    if occrs > 1:
        for row in lst:
            row[idx] = row[idx] * occrs
    return lst


def normalizeMarketValue(arr, index, pos):
    bound1, bound2, bound3 = getMarketValueBounds(pos)
    for row in arr:
        row[index] = marketSuccess(row[index], bound1, bound2, bound3)
    return arr


def normalizeCA(arr, index):
    for row in arr:
        row[index] = row[index] / 10.0
    return arr


def PositionTraitFinder(Position, DatasetColumns):
    DatasetTraits = []
    for role in Position:
        for Attribute in role:
            for DatasetColumn in DatasetColumns:
                if removeSpace(Attribute).lower() in DatasetColumn.lower() and DatasetColumn not in DatasetTraits:
                    DatasetTraits.append(DatasetColumn)
    return DatasetTraits


def roleTraitNamesFinder(Role, DatasetColumns, year):
    DatasetTraits = []
    for Attribute in Role:
        for DatasetColumn in DatasetColumns:
            if removeSpace(Attribute + year).lower() in DatasetColumn.lower() and DatasetColumn not in DatasetTraits:
                DatasetTraits.append(DatasetColumn)
    return DatasetTraits


def roleTraitIndexesFinder(Role, DatasetColumns, year):
    wantedIndexes = []
    for Attribute in Role:
        for DatasetColumnIndex in range(len(DatasetColumns)):
            if removeSpace(Attribute + year).lower() in removeSpace(DatasetColumns[DatasetColumnIndex].lower()) and \
                    DatasetColumnIndex not in wantedIndexes:
                wantedIndexes.append(DatasetColumnIndex)
    return wantedIndexes


def removeSpace(trait):
    newTrait = trait.replace(" ", "")
    return newTrait


def scoreByRole(playerRow, traitsIndexes):
    numTraits = 0
    roleScore = 0
    for traitsIndex in traitsIndexes:
        if playerRow[traitsIndex] == -1:
            return -1
        if playerRow[traitsIndex] != math.nan and playerRow[traitsIndex] != "" and \
                not posT.DatasetColumns[traitsIndex].startswith("Height"):
            roleScore += float(playerRow[traitsIndex])
            numTraits += 1
        if posT.DatasetColumns[traitsIndex].startswith("Height"):
            numTraits += 1
            hScore = (playerRow[traitsIndex] - 170) / 2.0
            if hScore > 10:
                roleScore += 20
            elif hScore < 0:
                roleScore += 10
            else:
                roleScore += (hScore + 10)

    if numTraits != 0:
        roleScore = roleScore / numTraits
    return roleScore


def findBestRole(playerRow, year, cols=posT.DatasetColumns, roles=posT.allRoles_Traits, rolesNames=posT.allRoles):
    allScores = []
    for role, roleName in zip(roles, rolesNames):
        score = scoreByRole(playerRow, roleTraitIndexesFinder(role, cols, year))
        if score == -1:
            return -1, -1
        allScores.append((roleName, score))
    best_role = max(allScores, key=itemgetter(1))
    return best_role


def getRightLeftFoot(playerRow, columns):
    RightFoot2018 = playerRow[roleTraitIndexesFinder(["Phy.RightFoot"], columns, year_2018)[0]]
    LeftFoot2018 = playerRow[roleTraitIndexesFinder(["Phy.LeftFoot"], columns, year_2018)[0]]
    RightFoot2012 = playerRow[roleTraitIndexesFinder(["Phy.RightFoot"], columns, year_2012)[0]]
    LeftFoot2012 = playerRow[roleTraitIndexesFinder(["Phy.LeftFoot"], columns, year_2012)[0]]
    RightFoot = RightFoot2018 if RightFoot2018 > 0 else RightFoot2012
    LeftFoot = LeftFoot2018 if LeftFoot2018 > 0 else LeftFoot2012
    return RightFoot, LeftFoot


def successMeter(playerRow, columns, marketValueRange1, marketValueRange2, marketValueRange3, weightsDict, roles,
                 rolesNames):
    TransferMarketPosition = playerRow[roleTraitIndexesFinder(["position_2012"], columns, "")[0]]
    RightFoot, LeftFoot = getRightLeftFoot(playerRow, columns)
    goalsScoredParm, assistsParam = getGoalAssistParams(TransferMarketPosition)
    playerMarketValue = playerRow[roleTraitIndexesFinder(["Market Value"], columns, year_2018)[0]]
    playerGoalsScored = playerRow[roleTraitIndexesFinder(["Goals_Scored"], columns, "")[0]]
    playerAssists = playerRow[roleTraitIndexesFinder(["Assists"], columns, "")[0]]
    playerGamesPlayed = playerRow[roleTraitIndexesFinder(["Games_Played"], columns, "")[0]]
    currentAbility2012 = playerRow[roleTraitIndexesFinder(["CA"], columns, year_2012)[0]]
    currentAbility2018 = playerRow[roleTraitIndexesFinder(["CA"], columns, year_2018)[0]]
    potentialAbility2012 = playerRow[roleTraitIndexesFinder(["PA"], columns, year_2012)[0]]
    attribsScore = findBestRole(playerRow, year_2018, columns, roles, rolesNames)[1]
    marketSuccessScore = marketSuccess(playerMarketValue, marketValueRange1, marketValueRange2, marketValueRange3)
    weightsConsidered = weightsDict['weakFoot']
    sumOfComponents = weightsDict['weakFoot'] * (RightFoot + LeftFoot) / 2
    if attribsScore > -1:
        sumOfComponents += weightsDict['attribs'] * attribsScore
        weightsConsidered += weightsDict['attribs']
    if marketSuccessScore >= 0 and TransferMarketPosition != 'Goalkeeper':
        sumOfComponents += weightsDict['market'] * marketSuccessScore
        weightsConsidered += weightsDict['market']
    if playerGamesPlayed >= 10 and goalsScoredParm > 0:
        sumOfComponents += min((10 + (playerGoalsScored / playerGamesPlayed) * goalsScoredParm) * weightsDict['goals'],
                               20 * weightsDict['goals'])
        weightsConsidered += weightsDict['goals']
    if playerGamesPlayed >= 10 and assistsParam > 0:
        sumOfComponents += min((10 + (playerAssists / playerGamesPlayed) * assistsParam) * weightsDict['assists'],
                               20 * weightsDict['assists'])
        weightsConsidered += weightsDict['assists']
    if currentAbility2018 > 0:
        sumOfComponents += (currentAbility2018 / 10) * weightsDict['CA']
        weightsConsidered += weightsDict['CA']
    else:
        improvement = potentialAbility2012 - currentAbility2012
        sumOfComponents += (((potentialAbility2012 - (improvement * 0.75)) / 10) * weightsDict['CA'])
        weightsConsidered += weightsDict['CA']
    if weightsConsidered == 0:
        return -1
    return sumOfComponents / weightsConsidered


def successMeterGK(playerRow, columns, marketValueRange1, marketValueRange2, marketValueRange3, weightsDict):
    playerMarketValue = playerRow[roleTraitIndexesFinder(["Market Value"], columns, year_2018)[0]]
    goalsConceded = playerRow[roleTraitIndexesFinder(["Goals_Conceded"], columns, "")[0]]
    cleanSheets = playerRow[roleTraitIndexesFinder(["Clean_sheets"], columns, "")[0]]
    playerGamesPlayed = playerRow[roleTraitIndexesFinder(["Games_Played"], columns, "")[0]]
    currentAbility = playerRow[roleTraitIndexesFinder(["CA"], columns, year_2018)[0]]
    attribsScore = findBestRole(playerRow, year_2018, columns, posT.GKs_Traits, posT.GKs)[1]
    marketSuccessScore = marketSuccess(playerMarketValue, marketValueRange1, marketValueRange2, marketValueRange3)
    weightsConsidered = 0
    sumOfComponents = 0
    if attribsScore > -1:
        sumOfComponents += weightsDict['attribs'] * attribsScore
        weightsConsidered += weightsDict['attribs']
    if marketSuccessScore >= 0:
        sumOfComponents += weightsDict['market'] * marketSuccessScore
        weightsConsidered += weightsDict['market']
    if playerGamesPlayed >= 10:
        sumOfComponents += max((20 - (goalsConceded / playerGamesPlayed) * 5) * weightsDict['conceded'], 0)
        sumOfComponents += min(((cleanSheets / playerGamesPlayed) * 35) * weightsDict['clean'],
                               20 * weightsDict['clean'])
        weightsConsidered += weightsDict['conceded']
        weightsConsidered += weightsDict['clean']
    if currentAbility > 0:
        sumOfComponents += (currentAbility / 10) * weightsDict['CA']
        weightsConsidered += weightsDict['CA']
    if weightsConsidered == 0:
        return -1
    return sumOfComponents / weightsConsidered


def marketSuccess(marketValue, marketValueRange1, marketValueRange2, marketValueRange3):
    marketValue = int(marketValue) / 1000000
    if 0 <= marketValue < marketValueRange1:
        return (marketValue / marketValueRange1) * 3 + 10
    elif marketValueRange1 <= marketValue < marketValueRange2:
        return ((marketValue - marketValueRange1) / (marketValueRange2 - marketValueRange1)) * 3 + 13
    elif marketValueRange2 <= marketValue < marketValueRange3:
        return ((marketValue - marketValueRange2) / (marketValueRange3 - marketValueRange2)) * 4 + 16
    elif marketValue >= marketValueRange3:
        return 20
    return -1


def getScoreByPos(playerRow, cols, pos):
    marketBound1, marketBound2, marketBound3 = getMarketValueBounds(pos)
    if pos == "GKs":
        return successMeterGK(playerRow, cols, marketBound1, marketBound2, marketBound3,
                              {'market': 0.2, 'conceded': 0.2, 'CA': 0.15, 'clean': 0.15, 'attribs': 0.3})
    elif pos == 'CBs':
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.35, 'goals': 0.1, 'CA': 0.15, 'assists': 0.05, 'attribs': 0.35, 'weakFoot': 0},
                            posT.CBs_Traits,
                            posT.CBs)
    elif pos == 'RBs':
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.225, 'goals': 0.05, 'CA': 0.15, 'assists': 0.25, 'attribs': 0.275,
                             'weakFoot': 0.05},
                            posT.FBs_Traits,
                            posT.FBs)
    elif pos == "LBs":
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.225, 'goals': 0.05, 'CA': 0.15, 'assists': 0.25, 'attribs': 0.275,
                             'weakFoot': 0.05},
                            posT.FBs_Traits,
                            posT.FBs)
    elif pos == "CDMs":
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.3, 'goals': 0.05, 'CA': 0.15, 'assists': 0.2, 'attribs': 0.3, 'weakFoot': 0},
                            posT.CDMs_Traits,
                            posT.CDMs)
    elif pos == "CMs":
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.225, 'goals': 0.1, 'CA': 0.15, 'assists': 0.2, 'attribs': 0.275,
                             'weakFoot': 0.05},
                            posT.CMs_Traits,
                            posT.CMs)
    elif pos == "CAMS":
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.2, 'goals': 0.15, 'CA': 0.15, 'assists': 0.225, 'attribs': 0.2,
                             'weakFoot': 0.075},
                            posT.CAMs_Traits,
                            posT.CAMs)
    elif pos == "Strikers":
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.225, 'goals': 0.25, 'CA': 0.15, 'assists': 0.05, 'attribs': 0.225,
                             'weakFoot': 0.1},
                            posT.Strikers_Traits, posT.Strikers)
    elif pos == "LMs":
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.15, 'assists': 0.2, 'attribs': 0.2,
                             'weakFoot': 0.05},
                            posT.Wingers_Traits, posT.Wingers)
    elif pos == "RMs":
        return successMeter(playerRow, cols, marketBound1, marketBound2, marketBound3,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.15, 'assists': 0.2, 'attribs': 0.2,
                             'weakFoot': 0.05},
                            posT.Wingers_Traits, posT.Wingers)
    else:
        return -1


def getGoalAssistParams(posTM):
    return {
        'Midfielder - Attacking Midfield': (15, 17),
        'Forward - Right Winger': (15, 17),
        'Defender - Left-Back': (45, 35),
        'Defender - Centre-Back': (50, 0),
        'Forward - Left Winger': (15, 17),
        'Midfielder - Left Midfield': (15, 17),
        'Midfielder - Central Midfield': (20, 20),
        'Midfielder - Defensive Midfield': (23, 30),
        'Defender - Right-Back': (45, 35),
        'Forward - Second Striker': (15, 20),
        'Forward - Centre-Forward': (15, 20),
        'Forward': (15, 20),
        'Midfielder - Right Midfield': (15, 17),
        'Midfielder': (20, 20),
        'Goalkeeper': (-1, -1),
        '-1': (-1, -1)
    }[posTM]


def getMarketValueBounds(filePos):
    return {
        'GKs': (1.5, 15, 100),
        'CBs': (4, 20, 100),
        'LBs': (1.5, 15, 100),
        'CDMs': (3, 15, 100),
        'LMs': (4, 20, 130),
        'RBs': (1.5, 15, 100),
        'RMs': (4, 20, 130),
        'Strikers': (4, 18, 120),
        'CAMS': (4, 20, 130),
        'CMs': (3, 12, 100)
    }[filePos]
