#import future
import numpy as np
import ROOT, glob, os, sys
import read_root_files as read
import matplotlib.pyplot as plt
plt.ion()

#path='/Users/kmulrey/LOFAR/LORA/DAQ_test/DAQ_test/lora_daq-master/normal_daq_output/'
path='/Users/kmulrey/LOFAR/LORA/LORAraw/'
path2='new_files/'

file_name='20200105_2207'
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

