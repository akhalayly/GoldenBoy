import difflib
import pandas as pd


def findIndices(pairsList, wantedName, TMList):
    matchingPlayer = ""
    matchingIdx = 0
    for playersPair in pairsList:
        if playersPair[0] == wantedName:
            matchingPlayer = playersPair[1]
            break
    if matchingPlayer == "":
        return -1
    for index in range(len(TMList)):
        if TMList[index][0] == matchingPlayer:
            matchingIdx = index
            break
    return matchingIdx


if __name__ == "__main__":
    files = ["CAMS.csv", "CBs.csv", "CMs.csv", "DMs.csv", "GKs.csv", "LBs.csv", "LWS.csv", "RBs.csv", "RWS.csv",
             "Strikers.csv"]
    for file in files:
        NamesFM = pd.read_csv("2012_cut/" + file, encoding="cp1250", delimiter=",")
        NamesListFM = [name[1] for name in NamesFM.values]
        NamesTM = pd.read_csv("MarketValuesGoals11-12.csv", encoding="utf-8", delimiter=",")
        NamesListTM = [name[0] for name in NamesTM.values]
        matched_list = []
        for FMname in NamesListFM:
            wantedString = difflib.get_close_matches(FMname, NamesListTM, 1, 0.85)
            if len(wantedString) == 0:
                wantedString = [""]
            matched_list.append((FMname, wantedString[0]))
        filename = "allData_" + file
        f = open(filename, "w", encoding="utf-8")
        f.write("GameDate,Name,UID,NationID,Born,Age,IntCaps,IntGoals,U21Caps,U21Goals,WorldReputation,HomeReputation,"
                "CurrentReputation,PA,CA,Price,Height,Weight,PositionsString,GK.AerialAbility,GK.CommandOfArea,"
                "GK.Communication,GK.Eccentricity,GK.Handling,GK.Kicking,GK.OneOnOnes,GK.Reflexes,GK.RushingOut,"
                "GK.TendencyToPunch,GK.Throwing,Tech.Corners,Tech.Crossing,Tech.Dribbling,Tech.Finishing,"
                "Tech.FirstTouch, "
                "Tech.Freekicks,Tech.Heading,Tech.LongShots,Tech.Longthrows,Tech.Marking,Tech.Passing,"
                "Tech.PenaltyTaking, "
                "Tech.Tackling,Tech.Technique,Mental.Aggression,Mental.Anticipation,Mental.Bravery,Mental.Composure,"
                "Mental.Concentration,Mental.Vision,Mental.Decisions,Mental.Determination,Mental.Flair,"
                "Mental.Leadership, "
                "Mental.OffTheBall,Mental.Positioning,Mental.Teamwork,Mental.Workrate,Phy.Acceleration,Phy.Agility,"
                "Phy.Balance,Phy.Jumping,Phy.LeftFoot,Phy.NaturalFitness,Phy.Pace,Phy.RightFoot,Phy.Stamina,"
                "Phy.Strength, "
                "Hidden.Consistency,Hidden.Dirtiness,Hidden.ImportantMatches,Hidden.InjuryProness,Hidden.Versatility,"
                "Personality.Adaptability,Personality.Ambition,Personality.Loyalty,Personality.Pressure,"
                "Personality.Professional,Personality.Sportsmanship,Personality.Temperament,Personality.Controversy,"
                "Positions.Defender,Positions.WingBack,Positions.Midfielder,Positions.AttackingMidfielder,"
                "Positions.Right,Positions.Left,Positions.Centre,Positions.PositionsDesc,Positions.PositionsDescVal,"
                "Positions.Goalkeeper,Positions.Sweeper,Positions.Striker,Positions.AttackingMidCentral,"
                "Positions.AttackingMidLeft,Positions.AttackingMidRight,Positions.DefenderCentral,"
                "Positions.DefenderLeft, "
                "Positions.DefenderRight,Positions.DefensiveMidfielder,Positions.MidfielderCentral,"
                "Positions.MidfielderLeft,Positions.MidfielderRight,Positions.WingBackLeft,Positions.WingBackRight,"
                "PPMVal,PPM0,PPM1,PPM2,PPM3,PPM4,PPM5,PPM6,PPM7,PPM8,PPM9,PPM10,PPM11,PPM12,PPM13,PPM14,PPM15,PPM16,"
                "PPM17,PPM18,PPM19,PPM20,PPM21,PPM22,PPM23,PPM24,PPM25,PPM26,PPM27,PPM28,PPM29,PPM30,PPM31,PPM32,PPM33,"
                "PPM34,PPM35,PPM36,PPM37,PPM38,PPM39,PPM40,PPM41,PPM42,PPM43,PPM44,PPM45,PPM46,PPM47,name,Market Value,"
                "age,height,position,foot,current club,10/11 games,10/11 goals/conceded,10/11 assists/clean,"
                "10/11 minutes,11/12 games,11/12 goals/conceded,11/12 assists/clean,11/12 minutes,12/13 games,"
                "12/13 goals/conceded,12/13 assists/clean,12/13 minutes,13/14 games,13/14 goals/conceded,"
                "13/14 assists/clean,13/14 minutes,14/15 games,14/15 goals/conceded,14/15 assists/clean,14/15 minutes,"
                "15/16 games,15/16 goals/conceded,15/16 assists/clean,15/16 minutes,16/17 games,16/17 goals/conceded,"
                "16/17 assists/clean,16/17 minutes,17/18 games,17/18 goals/conceded,17/18 assists/clean,17/18 minutes,"
                "18/19 games,18/19 goals/conceded,18/19 assists/clean,18/19 minutes,current league,19/20 games,"
                "19/20 goals/conceded,19/20 assists/clean,19/20 minutes,20/21 games,20/21 goals/conceded,"
                "20/21 assists/clean,20/21 minutes")
        f.write("\n")
        for FMcell in NamesFM.values:
            matchingIndex = findIndices(matched_list, FMcell[1], NamesTM.values)
            if matchingIndex == -1:
                wantedCell = []
            else:
                wantedCell = NamesTM.values[matchingIndex]
            resList = []
            for item in FMcell:
                resList.append(item)
            for item in wantedCell:
                resList.append(item)
            for cell in resList:
                f.write(str(cell))
                f.write(",")
            f.write("\n")
        f.close()
