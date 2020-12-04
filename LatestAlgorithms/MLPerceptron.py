from sklearn.neural_network import MLPClassifier
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
        last_results = {
            'relu': [],
            'logistic': [],
            'tanh': [],
            'identity': []
        }
        for activation in ['relu', 'logistic', 'tanh', 'identity']:
            results = [0] * 3
            index = 0
            for solver in ['lbfgs', 'adam', 'sgd']:
                for train_index, test_index in splits:
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    clf = MLPClassifier(activation=activation, solver=solver, max_iter=10000, alpha=1)
                    clf.fit(X_train, y_train)
                    pred_i = clf.predict(X_test)
                    results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
                # print(str(numOfEsti) + " Accuracy is: " + str(results[index]))
                index += 1
            last_results[activation] = results
        plt.figure(figsize=(12, 6))
        plt.plot(['lbfgs', 'adam', 'sgd'], last_results['relu'], color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.plot(['lbfgs', 'adam', 'sgd'], last_results['logistic'], color='blue', marker='o',
                 markerfacecolor='blue', markersize=10)
        plt.plot(['lbfgs', 'adam', 'sgd'], last_results['tanh'], color='black', marker='o',
                 markerfacecolor='black', markersize=10)
        plt.plot(['lbfgs', 'adam', 'sgd'], last_results['identity'], color='brown', marker='o',
                 markerfacecolor='brown', markersize=10)
        plt.title('Accuracy Rate Multi-Layer Perceptron ' + file)
        plt.xlabel('Solver')
        plt.ylabel('Mean Accuracy')
        plt.legend([str(i) for i in last_results.keys()])
        plt.show()
