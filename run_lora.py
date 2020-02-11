import numpy as np
import glob, os, sys
from multiprocessing import Pool

filepath='event_list.txt'
file_list=[]

with open(filepath) as fp:
    for cnt, line in enumerate(fp):
        file_list.append(line.strip())
        
print file_list

'''
def run_event(event):

    runCommand =    'python cr_xmaxfit.py --event={0} --lorafile-suffix=_GeVfix --datadir={1} --simulationdir={2} --iteration=0  --outputdir-radio-only={3} --logdir={4} --filtdir={5} --writedir={6} --collectdir={7}'.format(int(event),DATA_DIR,SIMULATION_DIR,OUTPUT_DIR_RADIO_ONLY,LOG_DIR,NEWSIM_PATH,WRITE_FILT,COLLECT_DIR)

    print 'Running command: %s' % runCommand

    
    retcode = os.system(runCommand)


event=int(events[11])

print '--------> event {0}'.format(event)

#use=[int(events[13]),int(events[14]),int(events[15]),int(events[16])]

p = Pool(12)
p.map(run_event,events)
#run_event(event)
'''
