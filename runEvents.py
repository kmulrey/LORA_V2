import numpy as np
import ROOT, glob, os, sys
import read_root_files as read
import matplotlib.pyplot as plt
import datetime
from datetime import datetime, timedelta
from datetime import date
from optparse import OptionParser
from sklearn.externals import joblib
#sys.path.insert(1, '../LORA_software_V2/')
import LORAparameters
import process_functions
import read_functions
import detector
import event
import imp
import process_V2




outputdir='/vol/astro3/lofar/lora/testOutput/'
path='/vol/astro3/lofar/vhecr/lora_triggered/LORAraw/'
path2='new_files/'

file_name='20200302_0051'
file=path2+file_name+'.npz'
print(file)
