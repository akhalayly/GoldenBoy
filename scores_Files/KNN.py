import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Positions_Traits as posT
import helperFunctions as hf

if __name__ == '__main__':
    files = ["CAMS", "CBs", "CMs", "CDMs", "GKs", "LBs", "LMs", "RBs", "RMs",
             "Strikers"]
    for file in files:
        dataset = pd.read_csv("Dataset/AllData_" + file + ".csv")
        cols = dataset.columns.values
        filename = "Success_" + file + ".csv"
        f = open(filename, "w", encoding="utf-8")
        for col in cols:
            f.write(col + ",")
        f.write("Success_Meter, Successful(0/1)\n")
        for row in dataset.values:
            for cell in row:
                f.write(str(cell) + ",")
            score = hf.getScoreByPos(row, cols, file)
            successful = 0
            if score > 14:
                successful = 1
            f.write(str(score) + "," + str(successful) + "\n")
        f.close()
