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


d = joblib.load(file)

log_data= d['data_log']
config_data= d['data_config']
header_data= d['data_header']
osm_data_hisparc= d['data_osm_hisparc']
osm_data_aera= d['data_osm_aera']

event_data= d['data_event']


event_list=header_data['Event_Id'][header_data['Event_Size']>0]
nEvents=len(event_list)


process_list=[]

print(nEvents)
for i in np.arange(nEvents):
    #print(np.unique(event_data['Station'][event_data['Event_Id']==event_list[i]]))
    stns=np.unique(event_data['Station'][event_data['Event_Id']==event_list[i]])
    if(stns[0]>5 or len(stns)>1) and stns[0]!=0:
        process_list.append(event_list[i])
        print('processing: ',event_list[i],stns)
        
print(len(process_list))

for i in np.arange(len(process_list)):
    eventID=process_list[i]
    try:
        process_V2.runEvent(eventID,log_data,config_data,header_data,osm_data_hisparc,osm_data_aera,event_data,file_name)
    except:
        print('{0} failed'.format(eventID))
