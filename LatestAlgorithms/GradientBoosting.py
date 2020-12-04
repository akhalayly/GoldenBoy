from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import svm
from sklearn import tree
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Positions_Traits as posT
import helperFunctions as hf

if __name__ == '__main__':
    files = ["CAMS", "CBs", "CMs", "CDMs", "GKs", "LBs", "LMs", "RBs", "RMs",
             "Strikers"]
    for file in files[:3]:
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
        # X = SelectKBest(chi2, k=20).fit_transform(X, y)
        for train, test in kf.split(X):
            splits.append((train, test))
        last_results = {
            2: 0,
            3: 0,
            5: 0,
            10: 0,
            20: 0
        }
        for maxDepth in [2, 3, 5, 10, 20]:
            results = [0] * 8
            index = 0
            for numOfEsti in [1, 5, 10, 20, 40, 70, 100, 150]:
                for train_index, test_index in splits:
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    clf = GradientBoostingClassifier(min_samples_split=30,
                                                     max_depth=maxDepth, n_estimators=numOfEsti)  # two runs, one with
                    # min samples 2 and another with 30 and then compare results
                    clf.fit(X_train, y_train)
                    pred_i = clf.predict(X_test)
                    results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
                # print(str(numOfEsti) + " Accuracy is: " + str(results[index]))
                index += 1
            last_results[maxDepth] = results
        plt.figure(figsize=(12, 6))
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[2], color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[3], color='blue', marker='o',
                 markerfacecolor='blue', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[5], color='black', marker='o',
                 markerfacecolor='black', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[10], color='brown', marker='o',
                 markerfacecolor='brown', markersize=10)
        plt.plot([1, 5, 10, 20, 40, 70, 100, 150], last_results[20], color='orange', marker='o',
                 markerfacecolor='orange', markersize=10)
        plt.title('Accuracy Rate GradientBoosting ' + file)
        plt.xlabel('Number of Estimators')
        plt.ylabel('Mean Accuracy')
        plt.legend([str(i) for i in last_results.keys()])
        plt.show()
