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

#outputdir='/Users/kmulrey/LOFAR/LORA/LORAprocessing/LORA_V2/LORAoutput/'
outputdir='/vol/astro3/lofar/lora/testOutputV2/'
path='/vol/astro3/lofar/vhecr/lora_triggered/LORAraw/'
path2='new_files/'
  
def runEvent(eventID,log_data,config_data,header_data,osm_data_hisparc,osm_data_aera,event_data,file_name):
    
    

    time_event=header_data['GPS_Time_Stamp_FirstHit'][header_data['Event_Id']==eventID]
    ns_event=header_data['nsec_Online_FirstHit'][header_data['Event_Id']==eventID]

    LOFAR_id=str(int(time_event-LORAparameters.event_id_offset))
    ev=event.Event(LOFAR_id,'V2')
  
  
  
    index=np.where(header_data['Event_Id']==eventID)
    
    
    detectors=[]
    lasas=[]
    LOFAR_id=str(int(time_event-LORAparameters.event_id_offset))
    print('running LOFAR event: {0}'.format(LOFAR_id))

    stations=np.unique(event_data['Station'][event_data['Event_Id']==eventID])
  
    print('running LOFAR event: {0}'.format(LOFAR_id))
    print('including stations: {0}'.format(stations))
    for i in np.arange(LORAparameters.nDetB):
        detectors.append(detector.Detector('Det'+(str(i+1))))
      
    for i in np.arange(LORAparameters.nLasaB):
        lasas.append(detector.Lasa('Lasa'+(str(i+1))))
                                    
    detector.load_positions(detectors)
    detector.load_signal(detectors)
    detector.load_gain(detectors)



    info,log_info=read_functions.return_event_V2(eventID,time_event,ns_event,event_data)
    sec_info0,sec_info1,sec_info2=read_functions.return_second_data_V2(eventID,time_event,ns_event,osm_data_hisparc, osm_data_aera)
        
    info,log_info=read_functions.return_event_V2(eventID,time_event,ns_event,event_data)
    sec_info0,sec_info1,sec_info2=read_functions.return_second_data_V2(eventID,time_event,ns_event,osm_data_hisparc, osm_data_aera)
        


    for i in np.arange(10):
        if i<5:
            diff0=int(sec_info0[i]['GPS_time_stamp_M'])-int(time_event)
            diff1=int(sec_info1[i]['GPS_time_stamp_M'])-int(time_event)
            diff2=int(sec_info2[i]['GPS_time_stamp_M'])-int(time_event)
        else:
            diff0=int(sec_info0[i]['GPS_time_stamp'])-int(time_event)
            diff1=int(sec_info1[i]['GPS_time_stamp'])-int(time_event)
            diff2=int(sec_info2[i]['GPS_time_stamp'])-int(time_event)
            
        if diff0!=0 or diff1!=1 or diff2!=2:
            print('LASA{0} difference not correct'.format(i+1))
            diff0=0
            diff1=1
            diff2=2
            lasas[i].sec_flag=1
        if i<5:
            if sec_info0[i]['CTP_M']>1e10 or sec_info0[i]['CTP_S']>1e10:
                print('data type problem')
                lasas[i].sec_flag=1
        else:
            if sec_info0[i]['CTP']>1e10:
                print('data type problem')
                lasas[i].sec_flag=1

    detector.load_event_information(info,detectors)
    detector.load_sec_information(sec_info0,sec_info1,sec_info2,lasas,'V2')
    detector.load_log_information(log_info,detectors)
    
    
    
    
    for d in np.arange(LORAparameters.nDetB):

        event.find_counts(detectors[d])
        #print(d+1,detectors[d].trace_int_counts)
        event.get_arrival_time(detectors[d])
        event.get_event_timestamp_V2(detectors[d],lasas[int((detectors[d].number-1)/4)])
        #print(detectors[d].event_time_stamp)
        #print((detectors[d].number),(detectors[d].threshold_time),(detectors[d].event_time_stamp))
                        
    
    for l in np.arange(LORAparameters.nLasaB):
        event.cal_event_timestamp(detectors,lasas[l])

    
    
    event.do_arrival_time_diff(detectors)
    try:
    #for t in np.arange(1):
        event.do_arrival_direction(detectors,ev)
        event.do_COM_core(detectors,ev)
        event.find_density(detectors,ev)#
        #print('flag?? ',ev.direction_flag)

    except:
        ev.event_flag=1
        print('\n\nissue with event\n\n')
    
    if ev.event_flag==0 and ev.direction_flag==0:
        print('saving to file')
        
    
        outputfile=open(outputdir+file_name+'_event_'+str(int(eventID))+'.txt','w')
        
        outputfile.write('event:  {0}\n'.format(str(eventID)))
        outputfile.write('gps_timestamp:  {0}\n'.format(int(time_event[0])))
        outputfile.write('ns:  {0}\n'.format(int(ns_event[0])))
        outputfile.write('index:  {0}\n'.format(index[0][0]))
        outputfile.write('theta:  {0}\n'.format(ev.theta))
        outputfile.write('phi:  {0}\n'.format(ev.phi))
        outputfile.write('core_x:  {0}\n'.format(ev.x_core))
        outputfile.write('core_y:  {0}\n'.format(ev.y_core))
        outputfile.write('core_z:  {0}\n'.format(ev.z_core))
        for i in np.arange(40):
            print(i+1, detectors[i].density)
            outputfile.write('{0}     {1}     {2}    {3}     {4}\n'.format(i+1,detectors[i].gps,detectors[i].nsec,int(detectors[i].event_time_stamp),detectors[i].density))
        outputfile.close()
