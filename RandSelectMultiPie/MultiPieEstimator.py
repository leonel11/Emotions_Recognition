import os
import shutil

listphotos = [] # list of path of chosen photos in selection
print('\nMaking selection...')

sessiondir = 'session03'

partpath = 'I:/Multi-Pie/data/' + sessiondir + '/multiview/'
subjectdirs = os.listdir(partpath)

recorddir = '03'

selectionpath = sessiondir + '_' + recorddir
os.makedirs(selectionpath)
for subdir in subjectdirs:
    pathtopicts = partpath + subdir + '/' + recorddir + '/05_1/'
    pictname = os.listdir(pathtopicts)[6]
    shutil.copy(pathtopicts + pictname, selectionpath + '/' + pictname)
print('Selection is created!')