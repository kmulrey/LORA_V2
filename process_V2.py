import numpy as np
import ROOT, glob, os, sys
import read_root_files as read
import matplotlib.pyplot as plt
import datetime
from datetime import datetime, timedelta
from datetime import date

sys.path.insert(1, '../LORA_software_V2/')
import LORAparameters as LORA
import process_functions
import read_functions
import detector
import event
import imp

#outputdir='/Users/kmulrey/LOFAR/LORA/LORAprocessing/LORA_V2/LORAoutput/'
outputdir='/vol/astro3/lofar/lora/testOutput/'

path='/vol/astro3/lofar/vhecr/lora_triggered/LORAraw/'
path2='new_files/'




parser = OptionParser()
parser.add_option('-f', '--file',type='str',help='filename',default=0)

(options, args) = parser.parse_args()
file_name=str(options.file)


  


#file_name='20200105_2207'
file=path2+file_name+'.npz'

d=np.load(file,allow_pickle=True)
print d.files
log_data= d['data_log']
config_data= d['data_config']
header_data= d['data_header']
osm_data= d['data_osm']
event_data= d['data_event']


big_events=[119]

event_size=header_data.item()['Event_Size']
event_id_all=header_data.item()['Event_Id']


big_events=event_id_all[event_size>10]
print big_events


for e in np.arange(len(big_events)):
#for e in np.arange(0):

    event_id=big_events[e]
    print '\n\n\n________________________________________\n'

    time_event=header_data.item()['GPS_Time_Stamp_FirstHit'][event_id_all==event_id]
    ns_event=header_data.item()['nsec_Online_FirstHit'][event_id_all==event_id]

    detectors=[]
    lasas=[]
    LOFAR_id=str(int(time_event-LORA.event_id_offset))

    print 'running LOFAR event: {0}'.format(LOFAR_id)

    ev=event.Event(LOFAR_id,'V2')


    detectors=[]
    lasas=[]

    for i in np.arange(LORA.nDetA):
        detectors.append(detector.Detector('Det'+(str(i+1))))
    
    for i in np.arange(LORA.nLasaA):
        lasas.append(detector.Lasa('Lasa'+(str(i+1))))
                                  
    detector.load_positions(detectors)
    detector.load_signal(detectors)
    detector.load_gain(detectors)

    info,log_info=read_functions.return_event_V2(event_id,time_event,ns_event,event_data)
    sec_info0,sec_info1,sec_info2=read_functions.return_second_data_V2(event_id,time_event,ns_event,osm_data)




    for i in np.arange(LORA.nLASA):
        diff0=int(sec_info0[i]['GPS_time_stamp_M'])-int(time_event)
        diff1=int(sec_info1[i]['GPS_time_stamp_M'])-int(time_event)
        diff2=int(sec_info2[i]['GPS_time_stamp_M'])-int(time_event)
        if diff0!=0 or diff1!=1 or diff2!=2:
            print 'difference not correct'
            lasas[i].sec_flag=1
        if sec_info0[i]['CTP_M']>1e10 or sec_info0[i]['CTP_S']>1e10:
            print 'data type problem'
            lasas[i].sec_flag=1


    detector.load_event_information(info,detectors)
    detector.load_sec_information(sec_info0,sec_info1,sec_info2,lasas,'V2')
    detector.load_log_information(log_info,detectors)


    lasa1_status=config_data.item()['lasa1_is_active']
    lasa2_status=config_data.item()['lasa2_is_active']
    lasa3_status=config_data.item()['lasa3_is_active']
    lasa4_status=config_data.item()['lasa4_is_active']
    lasa5_status=config_data.item()['lasa5_is_active']


    for d in np.arange(LORA.nDetA):
        event.find_counts(detectors[d])
        event.get_arrival_time(detectors[d])
        #print 'getting timestamp for----> {0}  {1}'.format(d, int((detectors[d].number-1)/4))
        event.get_event_timestamp_V2(detectors[d],lasas[int((detectors[d].number-1)/4)])

    for l in np.arange(LORA.nLasaA):
        event.cal_event_timestamp(detectors,lasas[l])


    event.do_arrival_time_diff(detectors)
    event.do_arrival_direction(detectors,ev)
    event.do_COM_core(detectors,ev)
    event.find_density(detectors,ev)

    event.fit_arrival_direction(detectors,ev)
    event.fit_NKG(detectors,ev)





    dt_object = datetime.utcfromtimestamp(time_event)

    year=dt_object.year
    month=dt_object.month
    day=dt_object.day
    hour=dt_object.hour
    minute=dt_object.minute
    sec=dt_object.second




    output_file=open(outputdir+'LORAdata-'+str(dt_object.year)+str(dt_object.month).zfill(2)+str(dt_object.day).zfill(2)+'T'+str(dt_object.hour).zfill(2)+str(dt_object.minute).zfill(2)+str(dt_object.second).zfill(2)+'.dat','w')




    output_file.write('//UTC_Time(secs)\tnsecs\t\tCore(X)\t\tCore(Y)\t\tElevation\tAzimuth\t\tEnergy(eV)\tCoreE(X)\tCoreE(Y)\tMoliere_rad(m)\t\tElevaErr\tAziErr\tEnergyErr(eV)\tNe\t\tNeErr\t\tCorCoef_XY\t\tNe_RefA\t\tNeErr_RefA\t\tEnergy_RefA\t\tEnergyErr_RefAtrig\n')
    output_file.write('{0}\t{1}\t{2:.2f}\t{3:.2f}\t{4:.2f}\t{5:.2f}\t{6}\t{7:.2f}\t{8:.2f}\t{9:.2f}\t{10:.2f}\t{11:.2f}\t{12}\t{13}\t{14}\t{15}\t{16}\t{17}\t{18}\t{19}\n'.format(int(ev.UTC_min), int(ev.nsec_min/10), ev.x_core, ev.y_core, ev.fit_elevation, ev.fit_phi, ev.energy*np.power(10,15), ev.x_core_err, ev.y_core_err, ev.Rm, ev.fit_elevation_err, ev.fit_phi_err, ev.energy_err*np.power(10,15), ev.Ne, ev.Ne_err, ev.CorCoef_xy, ev.Ne_RefA, ev.NeErr_RefA, ev.Energy_RefA*np.power(10,15), ev.EnergyErr_RefA*np.power(10,15)))

    output_file.write('//Detector coordinates w.r.t CS002 LBA center\n')
    output_file.write('//Det_no.    X_Cord(m)    Y_Cord(m)    Z_Cord(m)    UTC_time    (10*nsecs)  Particle_Density(/m2)\n')
    
    for i in np.arange(len(detectors)):
        output_file.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6:.4f}\n'.format(i+1,detectors[i].x_cord,detectors[i].y_cord,detectors[i].z_cord,int(detectors[i].gps),int(detectors[i].cal_time),detectors[i].density))

    output_file.close()
