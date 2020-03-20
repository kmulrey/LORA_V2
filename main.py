#import future
import numpy as np
import ROOT, glob, os, sys
import read_root_files as read
#import matplotlib.pyplot as plt
from optparse import OptionParser
from sklearn.externals import joblib
#plt.ion()

#path='/Users/kmulrey/LOFAR/LORA/DAQ_test/DAQ_test/lora_daq-master/normal_daq_output/'





#path='/Users/kmulrey/LOFAR/LORA/LORAraw/'
##path='/vol/astro3/lofar/lora/LORA_software_V2/LORA_V2/'
path='/vol/astro3/lofar/vhecr/lora_triggered/LORAraw/'
path2='new_files/'






parser = OptionParser()
#parser.add_option('-f', '--file',type='str',help='filename',default=0)
parser.add_option('-i', '--index',type='int',help='filename',default=0)

(options, args) = parser.parse_args()
#file_name=str(options.file)
ind=int(options.index)

#event_file=open('event_list.txt','r')
#events=np.genfromtxt(event_file)
#file_name=events[ind]

fp = open('event_list.txt','r')
for i, line in enumerate(fp):
    if i == ind:
        file_name=line.strip()
        break
fp.close()

print file_name

#file_name='20200122_005'
#file_name='20200101_1847'
#20200130_1110.root
#20200130_1110_array.log
#20200130_1110_detectors.log
#print 'hi'


tfile=path+file_name+'.root'
read.process_and_save(tfile)


file=path2+file_name+'.npz'

#d=np.load(file)
#print d.files

'''
waveforms= d['Waveform_Raw']#[0]
det=d['Detector']
id=d['Event_Id']
gps=d['GPS_Time_Stamp']

print waveforms.shape
ne=len(waveforms)
print ne

for i in np.arange(ne):
    if len(id[id==i])>8:
        det_all=det[id==i]
        print('_____________{0}:{1}_____________'.format(int(id[i]),len(id[id==i])))
        print(det_all)
        print(gps)
'''
'''
for i in np.arange(100,200):
    print det[i], id[i]
    fig = plt.figure(figsize=(5,5))
    ax1 = fig.add_subplot(1,1,1)#,aspect=1)
    ax1.plot(waveforms[i])
    plt.show()
    raw_input()
    plt.close()


#ax1.set_xlabel('std($f_r$)',fontsize=12)
#ax1.legend(numpoints=1,loc='upper right')
#ax1.set_xlim([0.0,0.2])

'''

