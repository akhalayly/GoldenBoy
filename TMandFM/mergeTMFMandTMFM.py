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


def IDindex(IDlist, playerID):
    try:
        return IDlist.index(playerID)
    except:
        return -1


if __name__ == "__main__":
    files = ["CAMS.csv", "CBs.csv", "CMs.csv", "DMs.csv", "GKs.csv", "LBs.csv", "LWs.csv", "RBs.csv", "RWs.csv",
             "Strikers.csv"]
    for file in files:
        FM12 = pd.read_csv("2011_2012/allData_" + file, encoding="ISO-8859-1", delimiter=",")
        filename = "11_12AllData_" + file
        f = open(filename, "w", encoding="utf-8")
        f.write("GameDate_2012,Name_2012,UID_2012,NationID_2012,Born_2012,Age_2012,IntCaps_2012,IntGoals_2012,"
                "U21Caps_2012,U21Goals_2012,WorldReputation_2012,HomeReputation_2012,CurrentReputation_2012,PA_2012,"
                "CA_2012,Price_2012,Height_2012,Weight_2012,PositionsString_2012,GK.AerialAbility_2012,"
                "GK.CommandOfArea_2012,GK.Communication_2012,GK.Eccentricity_2012,GK.Handling_2012,GK.Kicking_2012,"
                "GK.OneOnOnes_2012,GK.Reflexes_2012,GK.RushingOut_2012,GK.TendencyToPunch_2012,GK.Throwing_2012,"
                "Tech.Corners_2012,Tech.Crossing_2012,Tech.Dribbling_2012,Tech.Finishing_2012,Tech.FirstTouch_2012, "
                "Tech.Freekicks_2012,Tech.Heading_2012,Tech.LongShots_2012,Tech.Longthrows_2012,Tech.Marking_2012,"
                "Tech.Passing_2012,Tech.PenaltyTaking_2012, Tech.Tackling_2012,Tech.Technique_2012,"
                "Mental.Aggression_2012,Mental.Anticipation_2012,Mental.Bravery_2012,Mental.Composure_2012,"
                "Mental.Concentration_2012,Mental.Vision_2012,Mental.Decisions_2012,Mental.Determination_2012,"
                "Mental.Flair_2012,Mental.Leadership_2012, Mental.OffTheBall_2012,Mental.Positioning_2012,"
                "Mental.Teamwork_2012,Mental.Workrate_2012,Phy.Acceleration_2012,Phy.Agility_2012,Phy.Balance_2012,"
                "Phy.Jumping_2012,Phy.LeftFoot_2012,Phy.NaturalFitness_2012,Phy.Pace_2012,Phy.RightFoot_2012,"
                "Phy.Stamina_2012,Phy.Strength_2012, Hidden.Consistency_2012,Hidden.Dirtiness_2012,"
                "Hidden.ImportantMatches_2012,Hidden.InjuryProness_2012,Hidden.Versatility_2012,"
                "Personality.Adaptability_2012,Personality.Ambition_2012,Personality.Loyalty_2012,"
                "Personality.Pressure_2012,Personality.Professional_2012,Personality.Sportsmanship_2012,"
                "Personality.Temperament_2012,Personality.Controversy_2012,Positions.Defender_2012,"
                "Positions.WingBack_2012,Positions.Midfielder_2012,Positions.AttackingMidfielder_2012,"
                "Positions.Right_2012,Positions.Left_2012,Positions.Centre_2012,Positions.PositionsDesc_2012,"
                "Positions.PositionsDescVal_2012,Positions.Goalkeeper_2012,Positions.Sweeper_2012,"
                "Positions.Striker_2012,Positions.AttackingMidCentral_2012,Positions.AttackingMidLeft_2012,"
                "Positions.AttackingMidRight_2012,Positions.DefenderCentral_2012,Positions.DefenderLeft_2012, "
                "Positions.DefenderRight_2012,Positions.DefensiveMidfielder_2012,Positions.MidfielderCentral_2012,"
                "Positions.MidfielderLeft_2012,Positions.MidfielderRight_2012,Positions.WingBackLeft_2012,"
                "Positions.WingBackRight_2012,PPMVal_2012,PPM0_2012,PPM1_2012,PPM2_2012,PPM3_2012,PPM4_2012,"
                "PPM5_2012,PPM6_2012,PPM7_2012,PPM8_2012,PPM9_2012,PPM10_2012,PPM11_2012,PPM12_2012,PPM13_2012,"
                "PPM14_2012,PPM15_2012,PPM16_2012,PPM17_2012,PPM18_2012,PPM19_2012,PPM20_2012,PPM21_2012,PPM22_2012,"
                "PPM23_2012,PPM24_2012,PPM25_2012,PPM26_2012,PPM27_2012,PPM28_2012,PPM29_2012,PPM30_2012,PPM31_2012,"
                "PPM32_2012,PPM33_2012,PPM34_2012,PPM35_2012,PPM36_2012,PPM37_2012,PPM38_2012,PPM39_2012,PPM40_2012,"
                "PPM41_2012,PPM42_2012,PPM43_2012,PPM44_2012,PPM45_2012,PPM46_2012,PPM47_2012,name_2012,"
                "Market Value_2012,age_2012,height_2012,position_2012,foot_2012,current club_2012,10/11 games_2012,"
                "10/11 goals/conceded_2012,10/11 assists/clean_2012,10/11 minutes_2012,11/12 games_2012,"
                "11/12 goals/conceded_2012,11/12 assists/clean_2012,11/12 minutes_2012,12/13 games_2012,"
                "12/13 goals/conceded_2012,12/13 assists/clean_2012,12/13 minutes_2012,13/14 games_2012,"
                "13/14 goals/conceded_2012,13/14 assists/clean_2012,13/14 minutes_2012,14/15 games_2012,"
                "14/15 goals/conceded_2012,14/15 assists/clean_2012,14/15 minutes_2012,15/16 games_2012,"
                "15/16 goals/conceded_2012,15/16 assists/clean_2012,15/16 minutes_2012,16/17 games_2012,"
                "16/17 goals/conceded_2012,16/17 assists/clean_2012,16/17 minutes_2012,17/18 games_2012,"
                "17/18 goals/conceded_2012,17/18 assists/clean_2012,17/18 minutes_2012,18/19 games_2012,"
                "18/19 goals/conceded_2012,18/19 assists/clean_2012,18/19 minutes_2012,current league_2012,"
                "19/20 games_2012,19/20 goals/conceded_2012,19/20 assists/clean_2012,19/20 minutes_2012,"
                "20/21 games_2012,20/21 goals/conceded_2012,20/21 assists/clean_2012,20/21 minutes_2012,"
                "GameDate_2011,Name_2011,UID_2011,NationID_2011,Born_2011,Age_2011,IntCaps_2011,IntGoals_2011,"
                "U21Caps_2011,U21Goals_2011,WorldReputation_2011,HomeReputation_2011,CurrentReputation_2011,PA_2011,"
                "CA_2011,Price_2011,Height_2011,Weight_2011,PositionsString_2011,GK.AerialAbility_2011,"
                "GK.CommandOfArea_2011,GK.Communication_2011,GK.Eccentricity_2011,GK.Handling_2011,GK.Kicking_2011,"
                "GK.OneOnOnes_2011,GK.Reflexes_2011,GK.RushingOut_2011,GK.TendencyToPunch_2011,GK.Throwing_2011,"
                "Tech.Corners_2011,Tech.Crossing_2011,Tech.Dribbling_2011,Tech.Finishing_2011,Tech.FirstTouch_2011,"
                "Tech.Freekicks_2011,Tech.Heading_2011,Tech.LongShots_2011,Tech.Longthrows_2011,Tech.Marking_2011,"
                "Tech.Passing_2011,Tech.PenaltyTaking_2011,Tech.Tackling_2011,Tech.Technique_2011,"
                "Mental.Aggression_2011,Mental.Anticipation_2011,Mental.Bravery_2011,Mental.Composure_2011,"
                "Mental.Concentration_2011,Mental.Vision_2011,Mental.Decisions_2011,Mental.Determination_2011,"
                "Mental.Flair_2011,Mental.Leadership_2011,Mental.OffTheBall_2011,Mental.Positioning_2011,"
                "Mental.Teamwork_2011,Mental.Workrate_2011,Phy.Acceleration_2011,Phy.Agility_2011,Phy.Balance_2011,"
                "Phy.Jumping_2011,Phy.LeftFoot_2011,Phy.NaturalFitness_2011,Phy.Pace_2011,Phy.RightFoot_2011,"
                "Phy.Stamina_2011,Phy.Strength_2011,Hidden.Consistency_2011,Hidden.Dirtiness_2011,"
                "Hidden.ImportantMatches_2011,Hidden.InjuryProness_2011,Hidden.Versatility_2011,"
                "Personality.Adaptability_2011,Personality.Ambition_2011,Personality.Loyalty_2011,"
                "Personality.Pressure_2011,Personality.Professional_2011,Personality.Sportsmanship_2011,"
                "Personality.Temperament_2011,Personality.Controversy_2011,name_2011,Market Value_2011,"
                "current league_2011")
        f.write("\n")
        for playerRow in FM12.values:
            player_2011_index = -1
            resList = []
            for item in playerRow:
                resList.append(item)
            for file2 in files:
                FM11 = pd.read_csv("2010_2011/allData_" + file2, encoding="ISO-8859-1", delimiter=",")
                IDList11 = [name[2] for name in FM11.values]
                player_2011_index = IDindex(IDList11, playerRow[2])
                if player_2011_index != -1:
                    player2011 = FM11.values[player_2011_index]
                    for item in player2011[:81]:
                        resList.append(item)
                    for item in player2011[154:]:
                        resList.append(item)
                    for cell in resList:
                        f.write(str(cell))
                        if cell != resList[resList.__len__()-1]:
                            f.write(",")
                    break
            if player_2011_index == -1:
                for cell in resList:
                    f.write(str(cell))
                    if cell != resList[resList.__len__() - 1]:
                        f.write(",")
            f.write("\n")
        f.close()
