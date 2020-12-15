from sklearn.model_selection import KFold
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
        dataset = pd.read_csv("Success_" + file + ".csv")
        attrbs = []
        attrbs = attrbs + hf.roleTraitIndexesFinder(["Age"], dataset.columns, hf.year_2012)
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.General_Info, dataset.columns, "")
        attrbs = attrbs + hf.roleTraitIndexesFinder(posT.Positive_Traits, dataset.columns, hf.year_2012)
        for role in posT.positionToTraits[file]:
            attrbs = attrbs + hf.roleTraitIndexesFinder(role, dataset.columns, hf.year_2012)
        attrbs = list(set(attrbs))
        X = dataset.iloc[:, attrbs].values.astype(float)
        y = dataset.iloc[:, -1].values
        X = hf.normalizeAge(hf.normalizeMarketValue(hf.normalizeCA(X, 1), -1, file), 0)
        kf = KFold(n_splits=5)
        splits = []
        kernel_results = {
            'linear': [],
            'poly': [],
            'rbf': [],
            'sigmoid': []
        }
        for train, test in kf.split(X):
            splits.append((train, test))
        for kernel in ['linear', 'poly', 'rbf', 'sigmoid']:
            c_kernel_results = [0] * 6
            index = 0
            for c in [0.01, 0.1, 0.5, 1, 2, 5]:
                for train_index, test_index in splits:
                    X_train, X_test = X[train_index], X[test_index]
                    y_train, y_test = y[train_index], y[test_index]
                    clf = svm.SVC(kernel=kernel, C=c)
                    clf.fit(X_train, y_train)
                    pred_i = clf.predict(X_test)
                    c_kernel_results[index] += ((1 - np.mean(pred_i != y_test)) / splits.__len__())
                index += 1
            kernel_results[kernel] = c_kernel_results
        plt.figure(figsize=(12, 6))
        plt.plot([0.01, 0.1, 0.5, 1, 2, 5], kernel_results['linear'], color='red', marker='o',
                 markerfacecolor='red', markersize=10)
        plt.plot([0.01, 0.1, 0.5, 1, 2, 5], kernel_results['poly'], color='blue', marker='o',
                 markerfacecolor='blue', markersize=10)
        plt.plot([0.01, 0.1, 0.5, 1, 2, 5], kernel_results['rbf'], color='black', marker='o',
                 markerfacecolor='black', markersize=10)
        plt.plot([0.01, 0.1, 0.5, 1, 2, 5], kernel_results['sigmoid'], color='brown', marker='o',
                 markerfacecolor='brown', markersize=10)
        plt.title('Accuracy Rate SVM ' + file)
        plt.xlabel('C Value')
        plt.ylabel('Mean Accuracy')
        plt.legend([str(i) for i in kernel_results.keys()])
        plt.savefig("Results/SVM/Graph_" + file + ".png")
        plt.show()

        fig, ax = plt.subplots()

        # hide axes
        fig.patch.set_visible(False)
        ax.axis('off')
        ax.axis('tight')
        for key in kernel_results.keys():
            for idx in range(len(kernel_results[key])):
                kernel_results[key][idx] = float("{:.4f}".format(kernel_results[key][idx]))
        df = pd.DataFrame(kernel_results, columns=kernel_results.keys())
        header = ax.table(cellText=[['']],
                          colLabels=['kernel'],
                          loc='bottom', bbox=[0, -0.025, 1.0, 0.15]
                          )
        table = ax.table(cellText=df.values, rowLabels=[0.01, 0.1, 0.5, 1, 2, 5], colLabels=df.columns,
                         colWidths=[0.3, 0.3, 0.3, 0.3, 0.3], loc='bottom', cellLoc='center',
                         rowColours=['r', 'r', 'r', 'r', 'r', 'r'],
                         colColours=['r', 'r', 'r', 'r'], bbox=[0, -0.35, 1.0, 0.4])
        table.auto_set_font_size(False)
        table.scale(1, 1.3)
        table.set_fontsize(7)
        table.add_cell(0, -1, width=0.4, height=0.090, text="C")
        plt.figure(figsize=(20, 10))
        fig.tight_layout()
        fig.savefig("Results/SVM/" + file + ".png")
        plt.show()
