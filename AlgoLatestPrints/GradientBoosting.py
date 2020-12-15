from sklearn.ensemble import GradientBoostingClassifier
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
                    clf.fit(X_train, y_train)
                    pred_i = clf.predict(X_test)
                    results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
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
        plt.savefig("Results/GradientBoosting/" + file + ".png")
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
                          colLabels=['max_depth'],
                          loc='bottom', bbox=[0, -0.025, 1.0, 0.15]
                          )
        table = ax.table(cellText=df.values, rowLabels=[1, 5, 10, 20, 40, 70, 100, 150], colLabels=df.columns,
                         colWidths=[0.3, 0.3, 0.3, 0.3, 0.3], loc='bottom', cellLoc='center',
                         rowColours=['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'],
                         colColours=['r', 'r', 'r', 'r', 'r'], bbox=[0, -0.35, 1.0, 0.4])
        table.auto_set_font_size(False)
        table.scale(1, 1.3)
        table.set_fontsize(7)
        table.add_cell(0, -1, width=0.4, height=0.090, text="numEstimators")
        plt.figure(figsize=(20, 10))
        fig.tight_layout()
        fig.savefig("Results/GradientBoosting/" + file + ".png")
        plt.show()