import matplotlib.pyplot as plt
import os.path as pth
import sys

# Pull data from log file
def GetData(logfile):
    if not pth.exists(logfile): # checking of the existence of log file
        print('Cannot read log file!')
        return []
    with open(logfile) as f: # reading of data from log file
        data = f.read()
    return data.splitlines()

# Get values of losses and accuracies during the training process
def GetFeatures(data):
    Xloss, Yloss, Xacc, Yacc = [], [], [], []
    # getting X and Y values for dependency of iterations and losses
    str_iters = [st for st in data if ' Iteration ' and ' loss = ' in st]
    for str_iter in str_iters:
        sub_strs = str_iter.split()
        if sub_strs[5].isdigit():
            Xloss.append(int(sub_strs[5]))
        else:
            Xloss.append(int(sub_strs[5][:-1]))
        Yloss.append(float(sub_strs[-1]))
    # getting X and Y values for dependency of iterations and accuracies
    step = int([st for st in data if 'test_interval: ' in st][0].split()[-1])
    Xacc = [x for x in Xloss if x % step == 0]
    str_accs = [st for st in data if ' accuracy@1 = ' in st]
    for str_acc in str_accs:
        Yacc.append(float(str_acc.split()[-1]))
    return Xloss, Yloss, Xacc, Yacc

# Build the dependency of iterations and losses
def BuildLossHistoryImage(Xloss, Yloss):
    plt.plot(Xloss, Yloss)
    plt.xlabel('S')
    plt.ylabel('L')
    #plt.xlabel('Number of iteration')
    #plt.ylabel('Loss')
    #plt.xlabel('Число итераций')
    #plt.ylabel('Потери')
    plt.savefig('loss.png')

# Build the dependency of iterations and accuracies
def BuildAccuracyHistoryImage(Xacc, Yacc):
    plt.plot(Xacc, Yacc)
    plt.xlabel('S')
    plt.ylabel('A')
    #plt.xlabel('Number of iteration')
    #plt.ylabel('Accuracy')
    #plt.xlabel('Число итераций')
    #plt.ylabel('Доля правильных ответов')
    plt.savefig('accuracy.png')

# Build images of dependencies
def BuildDependenciesImages(Xloss, Yloss, Xacc, Yacc):
    BuildLossHistoryImage(Xloss, Yloss)
    plt.clf()
    BuildAccuracyHistoryImage(Xacc, Yacc)

if (len(sys.argv) != 2): # checking of right call
    print('The call of this script looks like this:\n' +
          '     python trainhistory.py log_file')
else:
    logfile = sys.argv[1]
    data = GetData(sys.argv[1])
    if data: # main part of script
        Xloss, Yloss, Xacc, Yacc = GetFeatures(data)
        BuildDependenciesImages(Xloss, Yloss, Xacc, Yacc)