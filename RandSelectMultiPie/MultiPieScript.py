import os
import sys
import shutil
import datetime
from numpy import random

# get random directory on given path
def getDir(pathtodirs):
    dirs = os.listdir(pathtodirs)
    idx = random.randint(0, len(dirs))
    res = '/'+dirs[idx]
    return res

# get the name of random picture on given path
def getPictName(pathtopicts):
    pictlist = [pict for pict in os.listdir(pathtopicts)] # form list of pictures on given path
    idx = random.randint(0, len(pictlist))
    res = pictlist[idx]
    return res

def getFileSelectionName(emotiontype, emotionscatter, curcount):
    if (emotiontype == 'N' or emotiontype == 'NS' or emotiontype == 'NOTSMILE'):
        nsemotions = ['AMAZED', 'LOOKING', 'DISGUIST', 'YAWNING', 'CALM']
        idx = random.randint(0, len(nsemotions))
        et = nsemotions[idx]
    else:
        et = getFullEmotionName(emotiontype)
    filename = str(et) + '-' + str(emotionscatter[et]+1) + '.png'
    return filename, et

# get random folder of session on the type of emotion
def getSessionDir(emotiontype):
    if (emotiontype == 'S' or emotiontype == 'SMILE'):
        sessionlist = ['/session01', '/session03'] # Smile photos are contained only in session 1 and 3
    elif (emotiontype == 'A' or emotiontype == 'AMAZED' or emotiontype == 'L' or emotiontype == 'LOOKING'):
        sessionlist = ['/session02'] # Amazedand looking photos are contained only in session 1 and 3
    elif (emotiontype == 'D' or emotiontype == 'DISGUIST'):
        sessionlist = ['/session03'] # Disguist photos are contained only in session 1 and 3
    elif (emotiontype == 'Y' or emotiontype == 'YAWNING'):
        sessionlist = ['/session04'] # Yawning photos are contained only in session 1 and 3
    else:
    # emotiontype == 'N' or emotiontype == 'NS' or emotiontype == 'NOTSMILE'
    # or emotiontype == 'C' or emotiontype == 'CALM'
        sessionlist = ['/session01', '/session02', '/session03', '/session04']
    idx = random.randint(0, len(sessionlist))
    return sessionlist[idx]

# get random folder of recording on given path and the type of emotion
def getRecordingDir(pathtosubject, emotiontype):
    if (emotiontype == 'S' or emotiontype == 'SMILE' or emotiontype == 'A' or emotiontype == 'AMAZED'):
        return '/02' # Smile and amazed photos are shooted only in recording 2
    elif (emotiontype == 'L' or emotiontype == 'LOOKING' or emotiontype == 'D' or emotiontype == 'DISGUIST' or
                  emotiontype == 'Y' or emotiontype == 'YAWNING'):
        return '/03' # Looking, disguist and yawning photos are shooted only in recording 3
    else:
    # if emotiontype != 'C' or emotiontype != 'CALM'
        recordingdirs = os.listdir(pathtosubject) # form list of recording folders on given path
        if (str(pathtosubject).find('session01') != -1 or str(pathtosubject).find('session03') != -1):
            recordingdirs.remove('02') # except folders with smile photos
        if (emotiontype == 'C' or emotiontype == 'CALM'):
            if str(pathtosubject).find('session02') != -1:
                recordingdirs.remove('02')  # except folders with amazed photos
                recordingdirs.remove('03')  # except folders with looking photos
            if str(pathtosubject).find('session03') != -1:
                recordingdirs.remove('03')  # except folders with disguist photos
            if str(pathtosubject).find('session04') != -1:
                recordingdirs.remove('03')  # except folders with yawning photos
        idx = random.randint(0, len(recordingdirs))
        res = '/'+recordingdirs[idx]
        return res

# get random folder of camera on given angle of view
def getCameraDir(angle):
    cameralist = ['/05_1'] # initially only direct view (angle = 0) is correct for selection
    # add auxilary cameras with greater angle of view
    if angle >= 15:
        cameralist.extend(['/14_0', '/05_0']) # -15, 15
    if angle >= 30:
        cameralist.extend(['/13_0', '/04_1']) # -30, 30
    if angle >= 45:
        cameralist.extend(['/08_0', '/19_0']) # -45, 45
    idx = random.randint(0, len(cameralist))
    res = cameralist[idx]
    return res

# get full name of emotion
def getFullEmotionName(emotiontype):
    if (emotiontype == 'S' or emotiontype == 'SMILE'):
        return 'SMILE'
    if (emotiontype == 'A' or emotiontype == 'AMAZED'):
        return 'AMAZED'
    if (emotiontype == 'L' or emotiontype == 'LOOKING'):
        return 'LOOKING'
    if (emotiontype == 'D' or emotiontype == 'DISGUIST'):
        return 'DISGUIST'
    if (emotiontype == 'Y' or emotiontype == 'YAWNING'):
        return 'YAWNING'
    if (emotiontype == 'C' or emotiontype == 'CALM'):
        return 'CALM'
    return emotiontype

# get path to picture of selection and its new name
def getSelectionPict(pathtodb, emotiontype, angle, emotionscatter, curcount):
    # form file name of file from selection
    filenamepict, et = getFileSelectionName(emotiontype, emotionscatter, curcount)
    # form full path to random selected picture on given type of emotion and angle of view from Multi-Pie database
    datadir = '/data'
    sessiondir = getSessionDir(et)
    multiviewdir = '/multiview'
    pathtosubjects = pathtodb + datadir + sessiondir + multiviewdir
    subjectdir = getDir(pathtosubjects)
    pathtosubject = pathtosubjects + subjectdir
    recordingdir = getRecordingDir(pathtosubject, et)
    pathtorecording = pathtosubject + recordingdir
    cameradir = getCameraDir(angle)
    pathtopicts = pathtorecording + cameradir
    pictfilename = getPictName(pathtopicts)
    fullpathtopict = pathtopicts + '/' + pictfilename
    filenamepict = str(pictfilename.replace('.png', '')) + filenamepict
    return fullpathtopict, filenamepict, et

# create the folder with photos of selection. If folder is not empty, it rewrites
def createSelectionFolder(foldername):
    pathtodir = os.getcwd() + '\\' + foldername # form full path to the folder with selection
    if os.path.exists(pathtodir):
        shutil.rmtree(pathtodir) # remove existing folder with the same name
    os.makedirs(pathtodir)
    return pathtodir

# copy pictures from Multi-Pie database to the folder of selection
def copySelection(selectionpath, pictures, names):
    idx = 0
    for pict in pictures :
        shutil.copy(pict, selectionpath+'/'+names[idx])
        idx += 1
    return

# make log-file with full paths to chosen selection photos from Multi-Pie database
def makeLog(foldername, select, names, emotionscatter):
    now = datetime.datetime.now()
    logname = foldername + '__' + now.strftime("%d.%m.%Y__%H-%M-%S") + '.log' # form the name of log-file
    f = open(logname, 'w')
    idx = 0
    f.write('Choosen emotions:\n')
    for key in emotionscatter.keys():
        if (emotionscatter[key] != 0):
            f.write(str(key)+':   '+str(emotionscatter[key])+'\n')
    f.write('\n')
    for pictpath in select:
        f.write(pictpath + '     ' + names[idx] + '\n') # writing to log-file
        idx += 1
    return

pathtodb = input('Please, enter the path to Multi-Pie: ')
if not os.path.isdir(pathtodb): # check the rightness of path to Multi-Pie database
    print('Wrong way to Multi-Pie')
    sys.exit(0)
countphotos = input('Please, enter the count of photos in selection: ')
if not str(countphotos).isnumeric(): # validation for count of photos in selection
    print('Wrong quantity')
    sys.exit(0)
else:
    countphotos = int(countphotos)
emotiontype = input('Please, choose the emotion: ')
emotiontype = str(emotiontype).upper()
# list of valid emotions
emotionlist = ['S', 'SMILE', 'N', 'NS', 'NOTSMILE', 'A', 'AMAZED', 'L', 'LOOKING', 'D', 'DISGUIST' ,'Y', 'YAWNING',
               'C', 'CALM']
if emotiontype not in emotionlist:
    print('Wrong chosen type of emotion')
    sys.exit(0)
anglevalue = input('Please, enter the value of viewing angle [-angle..angle]. angle = ')
if not str(anglevalue).isnumeric(): # validation for value of viewing angle
    print('Wrong quantity')
    sys.exit(0)
else:
    angle = abs(int(anglevalue))
    if angle > 45: # validation for correct (not large) value of viewing angle
        print('Too large angle of view')
        sys.exit(0)
foldername = input('Please, enter the name of new folder with selection: ')
if ('*' in str(foldername) or '|' in str(foldername) or '\\' in str(foldername) or ':' in str(foldername) or
            '"' in str(foldername) or '<' in str(foldername) or '>' in str(foldername) or '?' in str(foldername) or
            '/' in str(foldername)): # validation of foldername with selection
    print('Wrong name of folder with selection!')
    sys.exit(0)
curcount = 0 # current count of photos in selection. At the beginning no photos are selected
listphotos = [] # list of path of chosen photos in selection
listnames = [] # list of new names for photos in selection
emotionscatter = {'AMAZED': 0, 'LOOKING': 0, 'DISGUIST': 0, 'YAWNING': 0, 'CALM': 0, 'SMILE': 0}
# dictionary-scater of different types of not smiling emotions
print('\nMaking selection...')
while (curcount < countphotos):
    pict, filenamepict, et = getSelectionPict(pathtodb, emotiontype, angle, emotionscatter, curcount)
    if pict not in set(listphotos): # new photo is selected for selection
        listphotos.append(pict)
        curcount += 1
        emotionscatter[et] += 1
        listnames.append(filenamepict)
print('Files for selection are choosen!')
selectionpath = createSelectionFolder(foldername)
print('Copying files...')
copySelection(selectionpath, listphotos, listnames)
print('All files of selection are copied!')
makeLog(foldername, listphotos, listnames, emotionscatter)
print('Log-file is created!')
print('Selection is created!')
input("Press any key to continue...")