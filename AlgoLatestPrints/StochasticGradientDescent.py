from sklearn.linear_model import SGDClassifier
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
            for eta0 in [0.01, 0.1, 0.3, 0.5, 0.6, 0.8, 1]:
                for train_index, test_index in splits:
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    clf = SGDClassifier(loss="squared_hinge", penalty=penalty, eta0=eta0,
                                        alpha=0.1)  # two runs, change loss(squared_hinge and perceprton) and compare
                    clf.fit(X_train, y_train)
                    pred_i = clf.predict(X_test)
                    results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
                index += 1
            last_results[penalty] = results
        plt.figure(figsize=(12, 6))
        plt.plot([0.01, 0.1, 0.3, 0.5, 0.6, 0.8, 1], last_results[None], color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.plot([0.01, 0.1, 0.3, 0.5, 0.6, 0.8, 1], last_results['l2'], color='blue', marker='o',
                 markerfacecolor='blue', markersize=10)
        plt.plot([0.01, 0.1, 0.3, 0.5, 0.6, 0.8, 1], last_results['l1'], color='black', marker='o',
                 markerfacecolor='black', markersize=10)
        plt.plot([0.01, 0.1, 0.3, 0.5, 0.6, 0.8, 1], last_results['elasticnet'], color='brown', marker='o',
                 markerfacecolor='brown', markersize=10)
        plt.title('Accuracy Rate StochasticGradientDescent ' + file)
        plt.xlabel('Eta0')
        plt.ylabel('Mean Accuracy')
        plt.legend([str(i) for i in last_results.keys()])
        plt.savefig("Results/StochasticGradientDescent/Hinge_Graph_" + file + ".png")
        plt.show()

        fig, ax = plt.subplots()

        # hide axes
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        for key in last_results.keys():
            for idx in range(len(last_results[key])):
                last_results[key][idx] = float("{:.4f}".format(last_results[key][idx]))
        df = pd.DataFrame(last_results, columns=last_results.keys())
        header = ax.table(cellText=[['']],
                          colLabels=['penalty'],
                          loc='bottom', bbox=[0, -0.025, 1.0, 0.15]
                          )
        table = ax.table(cellText=df.values, rowLabels=[0.01, 0.1, 0.3, 0.5, 0.6, 0.8, 1], colLabels=df.columns,
                         colWidths=[0.3, 0.3, 0.3, 0.3, 0.3], loc='bottom', cellLoc='center',
                         rowColours=['r', 'r', 'r', 'r', 'r', 'r', 'r'],
                         colColours=['r', 'r', 'r', 'r'], bbox=[0, -0.35, 1.0, 0.4])
        table.auto_set_font_size(False)
        table.scale(1, 1.3)
        table.set_fontsize(7)
        table.add_cell(0, -1, width=0.4, height=0.090, text="eta0")
        plt.figure(figsize=(20, 10))
        table._cells[(0, 0)]._text.set_text("None")
        fig.tight_layout()
        fig.savefig("Results/StochasticGradientDescent/Hinge_" + file + ".png")
        plt.show()
