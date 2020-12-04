from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import KFold
from sklearn.feature_selection import SelectKBest, chi2, f_classif
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
        # X = SelectKBest(f_classif, k=20).fit_transform(X, y)
        for train, test in kf.split(X):
            splits.append((train, test))
        last_results = {
            None: [],
            'l2': [],
            'l1': [],
            'elasticnet': []
        }
        for penalty in [None, 'l2', 'l1', 'elasticnet']:
            results = [0] * 7
            index = 0
            for eta0 in [0.0001, 0.001, 0.01, 0.1, 0.3, 0.6, 1]:
                for train_index, test_index in splits:
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    clf = SGDClassifier(loss="squared_hinge", penalty=penalty, eta0=eta0,
                                        alpha=0.1)  # two runs, change loss(squared_hinge and perceprton) and compare
                    clf.fit(X_train, y_train)
                    pred_i = clf.predict(X_test)
                    results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
                # print(str(eta0) + " Accuracy is: " + str(results[index]))
                index += 1
            last_results[penalty] = results
        plt.figure(figsize=(12, 6))
        plt.plot([0.0001, 0.001, 0.01, 0.1, 0.3, 0.6, 1], last_results[None], color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.plot([0.0001, 0.001, 0.01, 0.1, 0.3, 0.6, 1], last_results['l2'], color='blue', marker='o',
                 markerfacecolor='blue', markersize=10)
        plt.plot([0.0001, 0.001, 0.01, 0.1, 0.3, 0.6, 1], last_results['l1'], color='black', marker='o',
                 markerfacecolor='black', markersize=10)
        plt.plot([0.0001, 0.001, 0.01, 0.1, 0.3, 0.6, 1], last_results['elasticnet'], color='brown', marker='o',
                 markerfacecolor='brown', markersize=10)
        plt.title('Accuracy Rate StochasticGradientDescent ' + file)
        plt.xlabel('Eta0')
        plt.ylabel('Mean Accuracy')
        plt.legend([str(i) for i in last_results.keys()])
        plt.show()
