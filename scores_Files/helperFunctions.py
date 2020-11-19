import Positions_Traits as posT
from operator import itemgetter
import math

year_2012 = "_2012"
year_2011 = "_2011"
year_2017 = "_2017"
year_2018 = "_2018"


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


def successMeter(playerRow, columns, marketValueRange1, marketValueRange2, marketValueRange3, goalsScoredParm,
                 assistsParam, weightsDict, roles, rolesNames):
    playerMarketValue = playerRow[roleTraitIndexesFinder(["Market Value"], columns, year_2018)[0]]
    playerGoalsScored = playerRow[roleTraitIndexesFinder(["Goals_Scored"], columns, "")[0]]
    playerAssists = playerRow[roleTraitIndexesFinder(["Assists"], columns, "")[0]]
    playerGamesPlayed = playerRow[roleTraitIndexesFinder(["Games_Played"], columns, "")[0]]
    currentAbility = playerRow[roleTraitIndexesFinder(["CA"], columns, year_2018)[0]]
    attribsScore = findBestRole(playerRow, year_2018, columns, roles, rolesNames)[1]
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
        sumOfComponents += min((10 + (playerGoalsScored / playerGamesPlayed) * goalsScoredParm) * weightsDict['goals'],
                               20 * weightsDict['goals'])
        weightsConsidered += weightsDict['goals']
    if playerGamesPlayed >= 10 and assistsParam > 0:
        sumOfComponents += min((10 + (playerAssists / playerGamesPlayed) * assistsParam) * weightsDict['assists'],
                               20 * weightsDict['assists'])
        weightsConsidered += weightsDict['assists']
    if currentAbility > 0:
        sumOfComponents += (currentAbility / 10) * weightsDict['CA']
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
    if pos == "GKs":
        return successMeterGK(playerRow, cols, 1.5, 15, 100,
                              {'market': 0.2, 'conceded': 0.2, 'CA': 0.2, 'clean': 0.2, 'attribs': 0.2})
    elif pos == 'CBs':
        return successMeter(playerRow, cols, 4, 20, 100, 50, 0,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.CBs_Traits,
                            posT.CBs)
    elif pos == 'RBs':
        return successMeter(playerRow, cols, 1.5, 15, 100, 23, 23,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.FBs_Traits,
                            posT.FBs)
    elif pos == "LBs":
        return successMeter(playerRow, cols, 1.5, 15, 100, 23, 23,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.FBs_Traits,
                            posT.FBs)
    elif pos == "CDMs":
        return successMeter(playerRow, cols, 3, 15, 100, 23, 30,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.CDMs_Traits,
                            posT.CDMs)
    elif pos == "CMs":
        return successMeter(playerRow, cols, 3, 12, 100, 20, 20,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.CMs_Traits,
                            posT.CMs)
    elif pos == "CAMS":
        return successMeter(playerRow, cols, 4, 20, 130, 15, 17,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.CAMs_Traits,
                            posT.CAMs)
    elif pos == "Strikers":
        return successMeter(playerRow, cols, 4, 18, 120, 15, 20,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.Strikers_Traits, posT.Strikers)
    elif pos == "LMs":
        return successMeter(playerRow, cols, 4, 20, 130, 15, 17,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.Wingers_Traits, posT.Wingers)
    elif pos == "RMs":
        return successMeter(playerRow, cols, 4, 20, 130, 15, 17,
                            {'market': 0.2, 'goals': 0.2, 'CA': 0.2, 'assists': 0.2, 'attribs': 0.2},
                            posT.Wingers_Traits, posT.Wingers)
    else:
        return -1
