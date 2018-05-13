import sys
import os
import numpy as np
import caffe
import matplotlib.pyplot as plt
from scipy.misc import imsave
from sklearn import metrics

def getCountClases(mode):
    if mode == 1:
        return 6
    if mode == 2:
        return 2
    return 0


def getClassNumber(prototxt_file, caffemodel_file, picture_file, real_class, y_true, y_score):
    image = caffe.io.load_image(picture_file, color=False)
    transformed_image = transformer.preprocess('data', image)
    # copy the image data into the memory allocated for the net
    #mean_image = np.zeros([122, 122])
    mean_image = np.zeros([118, 118])
    mean_image.fill(0.5)
    net.blobs['data'].data[...] = transformed_image - mean_image
    # perform classification
    output = net.forward(end='loss')
    output_prob = output['loss'] # the output probability vector for the first image in the batch
    np.set_printoptions(formatter={'float': '{: .6f}'.format})
    print(output_prob)
    y_true.append(real_class)
    y_score.append(output_prob[0, 1])
    print(output_prob[0, 1])
    predicted_class = output_prob.argmax()
    print(predicted_class, real_class)
    return predicted_class

def getSelectionAllocation(selection_file):
    res = dict()
    with open(selection_file, 'r') as f:
        while 1:
            fileline = f.readline()
            if not fileline: # EOF
                break
            dataline = fileline.split() # picture class_number
            res[dataline[0]] = int(dataline[1])
    return res

def visualizeFilters(picture_file, layer_name):
    print(picture_file)
    image = caffe.io.load_image(picture_file, color=False)
    transformed_image = transformer.preprocess('data', image)
    # copy the image data into the memory allocated for the net
    #mean_image = np.zeros([122, 122])
    mean_image = np.zeros([118, 118])
    mean_image.fill(0.5)
    net.blobs['data'].data[...] = transformed_image - mean_image
    output = net.forward(end=layer_name)
    data = net.blobs[layer_name].data
    K = data.shape[1] / 5
    M = 5 * data.shape[2]
    N = K * data.shape[2]
    map_features = np.zeros((M, N))
    for i in range(data.shape[1]):
    	st_j = (i/5)*data.shape[2]
    	st_i = (i%5)*data.shape[2]
    	print(st_i, st_j)
    	for x in range(data.shape[2]):
    		for y in range(data.shape[2]):
    			map_features[st_i+x, st_j+y] = int(255.0*data[0, i, x, y])
    imsave(layer_name+'.png', map_features)

def buildConfusionMatrix(count_classes, selection_path, selection_file, prototxt_file, caffemodel_file):
    conf_matr = np.zeros((count_classes, count_classes))
    list_pictures = os.listdir(selection_path)
    selection_allocation = getSelectionAllocation(selection_file)
    y_true = []
    y_score = []
    for pict in list_pictures:
    	print(pict)
        real_class = selection_allocation[pict]
        picture_file = selection_path + '/' + pict
        predicted_class = int(getClassNumber(prototxt_file, caffemodel_file, picture_file, real_class, y_true, y_score))
        conf_matr[predicted_class, real_class] += 1
    np.set_printoptions(formatter={'int': '{}'.format})
    print(conf_matr)
    np.savetxt('y_true.txt', y_true, delimiter=' ')
    np.savetxt('y_score.txt', y_score, delimiter=' ')
    #buildROC(y_true, y_score)
    #visualizeFilters(selection_path + '/' + '201_01_02_051_06SMILE-15027__.bmp', 'pool0')
    return conf_matr

def computeErrors(count_classes, conf_matr):
    for class_numb in range(count_classes):
        precision = conf_matr[class_numb, class_numb] / np.sum(conf_matr[class_numb, :])
        recall = conf_matr[class_numb, class_numb] / np.sum(conf_matr[:, class_numb])
        f1 = 2.0*precision*recall / (precision+recall)
        print('Class ' + str(class_numb) + ': precision=' + str(precision) + ', recall=' + str(recall) + ', f1=' + str(f1))
    acc = np.trace(conf_matr)/np.sum(conf_matr)
    print('Total accuracy: ' + str(acc))

'''def buildROC(y_true, y_score):
    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_score)
    auc = metrics.roc_auc_score(y_true, y_score)
    print('AUC-ROC for class 1: '+str(auc))
    #plt.figure()
    import matplotlib
    matplotlib.use('Agg')
    plt.plot(fpr[2], tpr[2], color='darkorange')
    plt.plot([0, 1], [0, 1], color='navy', linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.0])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.savefig('roccurve.png')'''

def getCNNSquad(net):
    # for each layer, show the output shape
    for layer_name, blob in net.blobs.iteritems():
        print(layer_name + '\t' + str(blob.data.shape))

if len(sys.argv) != 6:
    print('Script must be run in the format:\n python ConfusionMatrix.py mode selection_path selection_file prototxt caffemodel\n')
    print('Modes of script:')
    print('     1 - for emotion recognition')
    print('     2 - for smile detection')
else:
    mode = int(sys.argv[1])
    selection_path = str(sys.argv[2])
    selection_file = str(sys.argv[3])
    prototxt_file = str(sys.argv[4])
    caffemodel_file = str(sys.argv[5])
    count_classes = getCountClases(mode)

    caffe.set_device(0)
    caffe.set_mode_gpu()
    net = caffe.Net(prototxt_file,  # deploy prototxt model
                    caffemodel_file,  # trained weights
                    caffe.TEST)  # use test mode (e.g., don't perform dropout)
    #  create transformer for the input called 'data'
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost dimension
    # transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR
    # transformer.set_mean('data', np.array([127]))
    # transformer.set_raw_scale('data', 255.0)
    net.blobs['data'].reshape(1,  # batch size
                              1,  # 3-channel (BGR) images
                              118, 118)
                              #122, 122)  # image size is 122x122
    conf_matr = buildConfusionMatrix(count_classes, selection_path, selection_file, prototxt_file, caffemodel_file)
    computeErrors(count_classes, conf_matr)
    getCNNSquad(net)