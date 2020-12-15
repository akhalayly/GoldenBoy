from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import KFold
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Positions_Traits as posT
import helperFunctions as hf

if __name__ == '__main__':
    files = ["CAMS", "CBs", "CMs", "CDMs", "GKs", "LBs", "LMs", "RBs", "RMs",
             "Strikers"]
    for file in files:
        dataset = pd.read_csv("Success_" + file + ".csv")
        attrbs = []
        attrbs_names = []
        attrbs = attrbs + hf.roleTraitIndexesFinder(["Age"], dataset.columns, hf.year_2012)
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.General_Info, dataset.columns, "")
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.Positive_Traits, dataset.columns, hf.year_2012)
        for role in posT.positionToTraits[file]:
            attrbs = attrbs + hf.roleTraitIndexesFinder(role, dataset.columns, hf.year_2012)
        attrbs = list(set(attrbs))
        attrbs_names = list(set(attrbs_names))
        X = dataset.iloc[:, attrbs].values.astype(float)
        y = dataset.iloc[:, -1].values
        X = hf.normalizeAge(hf.normalizeMarketValue(hf.normalizeCA(X, 1), -1, file), 0)
        kf = KFold(n_splits=5)
        splits = []
        results = 0
        for train, test in kf.split(X):
            splits.append((train, test))
        results = [0] * 6
        index = 0
        for varPortion in [0.01, 0.1, 0.2, 0.5, 0.8, 1]:
            for train_index, test_index in splits:
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                gnb = GaussianNB(var_smoothing=varPortion)
                gnb.fit(X_train, y_train)
                pred_i = gnb.predict(X_test)
                results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
            index += 1
        plt.figure(figsize=(12, 6))
        plt.plot([0.01, 0.1, 0.2, 0.5, 0.8, 1], results, color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.title('Accuracy Rate GuassianNaiveBayes ' + file)
        plt.xlabel('Variance portion Value')
        plt.ylabel('Mean Accuracy')
        plt.savefig("Results/NaiveBayes/Graph_" + file + ".png")
        plt.show()
