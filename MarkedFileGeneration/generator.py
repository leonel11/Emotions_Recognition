import os.path as pth
import glob
import sys

# Get all file names of pictures from the selection
def GetAllFilesOfDirectory(folder):
    searchmask = folder + '/*'
    listfiles = glob.glob(searchmask)
    files = [pth.basename(file) for file in listfiles]
    return files

# Get class number for picture dependiong on task
def GetLabel(task, imgfile):
    if 'SMILE' in imgfile:
        return 0
    else:
        if task == '1': # task: Emotion Recognition
            if 'AMAZED' in imgfile:
                return 1
            elif 'DISGUIST' in imgfile:
                return 2
            elif 'LOOKING' in imgfile:
                return 3
            elif 'YAWNING' in imgfile:
                return 4
            elif 'CALM' in imgfile:
                return 5
            else:
                return -1
        else: # task: Smile Detection
            return 1

# Make marked file
# Format of file: list of strings 'imagename classnumber'
def MakeMarkedFile(task, pathtoselection, markedfile):
    listimages = GetAllFilesOfDirectory(pathtoselection)
    labels = [GetLabel(task, imgfile) for imgfile in listimages] # generate the list of class numbers
    with open(markedfile, 'w') as f:
        for idx in range(0, len(labels)):
            f.write(str(listimages[idx]) + ' ' + str(labels[idx]) + '\n')

task = input('Choose the task (1 - Emotions Recognition, 2 - Smile Detection): ')
if task != '1' and task != '2': # check the right input for chosen task
    print('Wrong chosen task!')
    sys.exit(0)
pathtoselection = input('Please, enter the path to selection: ')
if not pth.isdir(pathtoselection): # check the rightnes of path to selection
    print('Wrong way to selection!')
    sys.exit(0)
markedfile = input('Please, enter the name of generated marked file : ') # name of marked file, which will be generated
print('Creating LMDB files')
MakeMarkedFile(task, pathtoselection, markedfile)
print('Completed!')