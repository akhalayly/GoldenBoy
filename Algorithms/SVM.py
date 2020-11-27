from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, chi2
from sklearn import svm
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import Positions_Traits as posT
import helperFunctions as hf

if __name__ == '__main__':
    files = ["CAMS", "CBs", "CMs", "CDMs", "GKs", "LBs", "LMs", "RBs", "RMs",
             "Strikers"]
    for file in files:
        dataset = pd.read_csv("Success_" + file + "2.csv")
        attrbs = []
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.General_Info, dataset.columns, "")
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.Positive_Traits, dataset.columns, hf.year_2012)
        for role in posT.positionToTraits[file]:
            attrbs = attrbs + hf.roleTraitIndexesFinder(role, dataset.columns, hf.year_2012)
        attrbs = list(set(attrbs))
        X = dataset.iloc[:, attrbs].values.astype(float)
        y = dataset.iloc[:, -1].values
        X = hf.normalizeMarketValue(hf.normalizeCA(X, 0), -1, file)
        # X = SelectKBest(chi2, k=10).fit_transform(X, y)
        kf = KFold(n_splits=5)
        splits = []
        kernel_results = {
            'linear': 0,
            'poly': 0,
            'rbf': 0,
            'sigmoid': 0,
            'precomputed': 0
        }
        for train, test in kf.split(X):
            splits.append((train, test))
        for kernel in ['linear', 'poly', 'rbf', 'sigmoid']:
            for train_index, test_index in splits:
                X_train, X_test = X[train_index], X[test_index]
                y_train, y_test = y[train_index], y[test_index]
                clf = svm.SVC(kernel=kernel, C=1)
                clf.fit(X_train, y_train)
                pred_i = clf.predict(X_test)
                choseOne = 0
                choseZero = 0
                kernel_results[kernel] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
                for i in range(len(pred_i)):
                    if pred_i[i] != y_test[i] and pred_i[i] == 1:
                        choseOne = choseOne + 1
                    elif pred_i[i] != y_test[i]:
                        choseZero = choseZero + 1
                # print("choseZero: " + str(len(pred_i) - sum(pred_i)) + " choseZero: " + str(
                #     choseZero) + " Ratio of wrong Zeros: " + str(choseZero / (len(pred_i) - sum(pred_i))))
                # print("choseOne: " + str(sum(pred_i)) + " choseOneWrong: " + str(
                #     choseOne) + " Ratio of wrong Ones: " + str(choseOne / sum(pred_i)))
            print(kernel + " Last Accuracy is: " + str(kernel_results[kernel]))
        # plt.figure(figsize=(12, 6))
        # plt.plot(range(1, 30), kernel_results['linear'], color='red', marker='o',
        #          markerfacecolor='red', markersize=10)
        # plt.plot(range(1, 30), kernel_results['poly'], color='blue', marker='o',
        #          markerfacecolor='blue', markersize=10)
        # plt.plot(range(1, 30), kernel_results['rbf'], color='black', marker='o',
        #          markerfacecolor='black', markersize=10)
        # plt.plot(range(1, 30), kernel_results['sigmoid'], color='brown', marker='o',
        #          markerfacecolor='brown', markersize=10)
        # plt.plot(range(1, 30), kernel_results['precomputed'], color='orange', marker='o',
        #          markerfacecolor='orange', markersize=10)
        # plt.title('Accuracy Rate K Value ' + file)
        # plt.xlabel('K Value')
        # plt.ylabel('Mean Accuracy')
        # plt.legend([str(i) for i in kernel_results.keys()])
        # plt.show()
