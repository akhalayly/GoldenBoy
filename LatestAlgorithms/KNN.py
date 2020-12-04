from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, chi2, f_classif
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
        attrbs = attrbs + hf.roleTraitIndexesFinder(["Age"], dataset.columns, hf.year_2012)
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.General_Info, dataset.columns, "")
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.Positive_Traits, dataset.columns, hf.year_2012)
        for role in posT.positionToTraits[file]:
            attrbs = attrbs + hf.roleTraitIndexesFinder(role, dataset.columns, hf.year_2012)
        attrbs = list(set(attrbs))
        k_results_dict = {
            10: [],
            15: [],
            20: [],
            25: [],
            attrbs.__len__(): []
        }
        X = dataset.iloc[:, attrbs].values.astype(float)
        y = dataset.iloc[:, -1].values
        X = hf.normalizeAge(hf.normalizeMarketValue(hf.normalizeCA(X, 1), -1, file), 0)
        for j in [10, 15, 20, 25, attrbs.__len__()]:
            X_new = SelectKBest(chi2, k=j).fit_transform(X, y)
            # X_new = X
            kf = KFold(n_splits=5)
            splits = []
            for train, test in kf.split(X_new):
                splits.append((train, test))
            k_results = [0] * 29
            k_resultsU = [0] * 29
            for i in range(1, 30):
                for train_index, test_index in splits:
                    X_train, X_test = X_new[train_index], X_new[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    knn = KNeighborsClassifier(n_neighbors=i, weights='distance')
                    knn.fit(X_train, y_train)
                    pred_i = knn.predict(X_test)
                    k_results[i - 1] += ((1 - np.mean(pred_i != y_test)) / 5.0)
                    knnU = KNeighborsClassifier(n_neighbors=i, weights='uniform')
                    knnU.fit(X_train, y_train)
                    pred_iU = knnU.predict(X_test)
                    k_resultsU[i - 1] += ((1 - np.mean(pred_iU != y_test)) / 5.0)
            k_results_dict[j] = k_results
        plt.figure(figsize=(12, 6))
        plt.plot(range(1, 30), k_results_dict[10], color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.plot(range(1, 30), k_results_dict[15], color='blue', marker='o',
                 markerfacecolor='blue', markersize=10)
        plt.plot(range(1, 30), k_results_dict[20], color='black', marker='o',
                 markerfacecolor='black', markersize=10)
        plt.plot(range(1, 30), k_results_dict[25], color='brown', marker='o',
                 markerfacecolor='brown', markersize=10)
        plt.plot(range(1, 30), k_results_dict[attrbs.__len__()], color='orange', marker='o',
                 markerfacecolor='orange', markersize=10)
        plt.title('Accuracy Rate K Value ' + file)
        plt.xlabel('K Value')
        plt.ylabel('Mean Accuracy')
        plt.legend([str(i) for i in k_results_dict.keys()])
        plt.show()
