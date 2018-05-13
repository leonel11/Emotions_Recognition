import os.path as pth
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn import metrics

# Get true and predicted labels of classes
def GetLabels(y_true_file, y_score_file):
    y_true, y_score = [], []
    if not pth.exists(y_true_file) or not pth.exists(y_score_file): # checking of reading files with labels
        print('Cannot read files with labels!')
    else: # reading true and predicted labels of classes
        y_true = np.loadtxt(y_true_file, delimiter=' ').tolist()
        y_score = np.loadtxt(y_score_file, delimiter=' ').tolist()
    return y_true, y_score

# Calculate AUC-ROC value
def CalculateAucRoc(y_true, y_score):
    fpr, tpr, _ = metrics.roc_curve(y_true, y_score) # get FPR and TPR values for ROC curve
    auc = metrics.roc_auc_score(y_true, y_score)
    return fpr, tpr, auc

# Build ROC curve
def BuildRocCurve(fpr, tpr):
    plt.figure()
    plt.plot(fpr, tpr, color='red', lw=3, label='ROC curve')
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc="lower right")
    plt.show()

if (len(sys.argv) != 3): # checking of right call
    print('The call of this script looks like this:\n' +
          '     python aucroc.py y_true_file y_score_file')
else:
    y_true, y_score = GetLabels(sys.argv[1], sys.argv[2])
    if y_true and y_score: # main part of script
        fpr, tpr, auc = CalculateAucRoc(y_true, y_score)
        print('AUC-ROC for class 1: ' + str(auc))
        BuildRocCurve(fpr, tpr)