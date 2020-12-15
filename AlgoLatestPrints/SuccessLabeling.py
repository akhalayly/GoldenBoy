import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Positions_Traits as posT
import helperFunctions as hf


successBound = {
    'GKs': 13.4,
    'CBs': 13.6,
    'LBs': 13.7,
    'RBs': 13.5,
    'CDMs': 13.4,
    'CMs': 13.8,
    'CAMS': 14.4,
    'Strikers': 14.9,
    'LMs': 14.3,
    'RMs': 14
}
if __name__ == '__main__':
    files = ["CAMS", "CBs", "CMs", "CDMs", "GKs", "LBs", "LMs", "RBs", "RMs",
             "Strikers"]
    for file in files:
        numOfSuccess = 0
        numOfPlayers = 0
        dataset = pd.read_csv("data/AllData_" + file + ".csv")
        cols = dataset.columns.values
        filename = "Success_" + file + ".csv"
        f = open(filename, "w", encoding="utf-8")
        for col in cols:
            f.write(col + ",")
        f.write("Success_Meter, Successful(0/1)\n")
        for row in dataset.values:
            numOfPlayers = numOfPlayers + 1
            for cell in row:
                f.write(str(cell) + ",")
            score = hf.getScoreByPos(row, cols, file)
            successful = 0
            if score > successBound[file]:
                numOfSuccess = numOfSuccess + 1
                successful = 1
            f.write(str(score) + "," + str(successful) + "\n")
        print("Position: " + file + " Number of successful players: " + str(numOfSuccess) + " Number of players: " + str(numOfPlayers)
              + " ratio: " + str(numOfSuccess/numOfPlayers))
        f.close()
