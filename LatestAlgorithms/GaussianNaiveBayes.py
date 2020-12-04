from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, chi2
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
        # X = SelectKBest(chi2, k=20).fit_transform(X, y)
        for train, test in kf.split(X):
            splits.append((train, test))
        results = [0] * 6
        index = 0
        for varPortion in [0.000000001, 0.0000001, 0.00001, 0.001, 0.1, 1]:
            for train_index, test_index in splits:
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                gnb = GaussianNB(var_smoothing=varPortion)  # decide if there is a need for a graph or not
                gnb.fit(X_train, y_train)
                pred_i = gnb.predict(X_test)
                results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
            index += 1
        # print(file + " Accuracy is: " + str(results))
        plt.figure(figsize=(12, 6))
        plt.plot([0.000000001, 0.0000001, 0.00001, 0.001, 0.1, 1], results, color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.title('Accuracy Rate GuassianNaiveBayes ' + file)
        plt.xlabel('Variance portion Value')
        plt.ylabel('Mean Accuracy')
        plt.show()
