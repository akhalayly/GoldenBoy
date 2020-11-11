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
                if UpperNoSpace(Attribute).lower() in DatasetColumn.lower() and DatasetColumn not in DatasetTraits:
                    DatasetTraits.append(DatasetColumn)
    return DatasetTraits


def roleTraitNamesFinder(Role, DatasetColumns, year):
    DatasetTraits = []
    for Attribute in Role:
        for DatasetColumn in DatasetColumns:
            if UpperNoSpace(Attribute+year).lower() in DatasetColumn.lower() and DatasetColumn not in DatasetTraits:
                DatasetTraits.append(DatasetColumn)
    return DatasetTraits


def roleTraitIndexesFinder(Role, DatasetColumns, year):
    wantedIndexes = []
    for Attribute in Role:
        for DatasetColumnIndex in range(len(DatasetColumns)):
            if UpperNoSpace(Attribute+year).lower() in DatasetColumns[DatasetColumnIndex].lower() and \
                    DatasetColumnIndex not in wantedIndexes:
                wantedIndexes.append(DatasetColumnIndex)
    return wantedIndexes


def UpperNoSpace(trait):
    newTrait = trait.replace(" ", "")
    return newTrait


def scoreByRole(playerRow, traitsIndexes):
    numTraits = 0
    roleScore = 0
    for traitsIndex in traitsIndexes:
        if playerRow[traitsIndex] != math.nan and playerRow[traitsIndex] != "" and not posT.DatasetColumns[traitsIndex].startswith("Height"):
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


def findBestPosition(playerRow):
    allScores = []
    for role, roleName in zip(posT.allRoles_Traits, posT.allRoles):
        allScores.append((roleName, scoreByRole(playerRow, roleTraitIndexesFinder(role, posT.DatasetColumns, year_2012))))
    best_pos = max(allScores, key=itemgetter(1))[0]
    return best_pos
