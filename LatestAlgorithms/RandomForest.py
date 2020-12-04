from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import tree
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
        # X = SelectKBest(chi2, k=10).fit_transform(X, y)
        for train, test in kf.split(X):
            splits.append((train, test))
        last_results = {
            2: [],
            5: [],
            10: [],
            20: [],
            30: []
        }
        for minSplit in [2, 5, 10, 20, 30]:
            results = [0] * 8
            index = 0
            for numOfEsti in [1, 5, 10, 20, 40, 70, 100, 150]:
                for train_index, test_index in splits:
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    clf = RandomForestClassifier(criterion="gini", min_samples_split=minSplit,
                                                 n_estimators=numOfEsti)
                    clf.fit(X_train, y_train)
                    pred_i = clf.predict(X_test)
                    results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
                    choseOne = 0
                    choseZero = 0
                    # for i in range(len(pred_i)):
                    #     if pred_i[i] != y_test[i] and pred_i[i] == 1:
                    #         choseOne = choseOne + 1
                    #     elif pred_i[i] != y_test[i]:
                    #         choseZero = choseZero + 1
                    # print("choseZero: " + str(len(pred_i) - sum(pred_i)) + " choseZero: " + str(
                    #     choseZero) + " Ratio of wrong Zeros: " + str(choseZero / (len(pred_i) - sum(pred_i))))
                    # print("choseOne: " + str(sum(pred_i)) + " choseOneWrong: " + str(
                    #     choseOne) + " Ratio of wrong Ones: " + str(choseOne / sum(pred_i)))
                index += 1
            last_results[minSplit] = results
        plt.figure(figsize=(12, 6))
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[2], color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[5], color='blue', marker='o',
                 markerfacecolor='blue', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[10], color='black', marker='o',
                 markerfacecolor='black', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[20], color='brown', marker='o',
                 markerfacecolor='brown', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[30], color='orange', marker='o',
                 markerfacecolor='orange', markersize=10)
        plt.title('Accuracy Rate Random Forest ' + file)
        plt.xlabel('Number of Estimators')
        plt.ylabel('Mean Accuracy')
        plt.legend([str(i) for i in last_results.keys()])
        plt.show()
