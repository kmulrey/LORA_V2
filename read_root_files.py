#import future
import numpy as np
import ROOT, glob, os, sys
from multiprocessing import Pool

branches={}
branches['Tree_Event'] =['Station','Detector','Channel_Passed_Threshold','Trigg_Threshold','Charge_Corrected','Peak_Height_Corrected','Peak_Height_Raw','Waveform_Raw','Event_Id','Run_Id','GPS_Time_Stamp','CTD','nsec_Online','HiSparc_Trigg_Pattern','HiSparc_Trigg_Condition']
branches['Tree_Detector_Config'] =['sigma_ovr_thresh','lasa1_is_active','lasa1_version','lasa2_is_active','lasa2_version','lasa3_is_active','lasa3_version','lasa4_is_active','lasa4_version','lasa5_is_active','lasa5_version','lofar_trig_mode','lofar_trig_cond','lora_trig_cond','lora_trig_mode','calibration_mode','log_interval','check_coinc_interval','reset_thresh_interval','init_reset_thresh_interval','coin_window','wvfm_process_offtwlen','wvfm_process_wpost','wvfm_process_wpre','diagnostics_interval','output_save_hour','tbb_dump_wait_min','osm_store_interval']

branches['Tree_Log']=['Station','Detector','Channel_Thres_Low','Mean_Baseline','Mean_Sigma']


branches['Tree_OSM_HiSparc']=['Station','Master_Or_Slave','GPS_Time_Stamp','Sync_Error','Quant_Error','CTP']
branches['Tree_Event_Header']=['GPS_Time_Stamp_FirstHit','nsec_Online_FirstHit','Event_Id','Run_Id','LOFAR_Trigg','Event_Tree_Index','Event_Size']

def get_entry(br,key,n):
    br.GetEntry(n)
    if key!='Waveform_Raw':
        return br.GetLeaf(key).GetValue()
        
    if key=='Waveform_Raw':
        nTrace=4000
        return np.array([br.GetLeaf(key).GetValue(k) for k in range(nTrace)])

def process_and_save(tfile):
    print (tfile)
    pklfile='new_files/'+ os.path.basename(tfile).split('.root')[0]+'.npz'
    if os.path.exists(pklfile):
        print ("file exits. skip")
        return
    rtfile = ROOT.TFile.Open(tfile)
    
    data_new={}
    data_new_config={}
    data_new_log={}
    data_new_event={}
    data_new_osm={}
    data_new_header={}
    
    for tree_name in ['Tree_Event_Header']:
        tree=rtfile.Get(tree_name)
        for branch in branches[tree_name]:
            print (tree_name,branch)
            br= tree.GetBranch(branch)
            n=br.GetEntries()
            data_new_header[branch]=np.array([get_entry(br,branch,i) for i in range(n)])

    for tree_name in ['Tree_Detector_Config']:
        tree=rtfile.Get(tree_name)
        for branch in branches[tree_name]:
            print (tree_name,branch)
            br= tree.GetBranch(branch)
            n=br.GetEntries()
            data_new_config[branch]=np.array([get_entry(br,branch,i) for i in range(n)])
    
    for tree_name in ['Tree_Log']:
        tree=rtfile.Get(tree_name)
        for branch in branches[tree_name]:
            print (tree_name,branch)
            br= tree.GetBranch(branch)
            n=br.GetEntries()
            data_new_log[branch]=np.array([get_entry(br,branch,i) for i in range(n)])
    
    for tree_name in ['Tree_Event']:
        tree=rtfile.Get(tree_name)
        for branch in branches[tree_name]:
            print (tree_name,branch)
            br= tree.GetBranch(branch)
            n=br.GetEntries()
            data_new_event[branch]=np.array([get_entry(br,branch,i) for i in range(n)])
    
    for tree_name in ['Tree_OSM_HiSparc']:
        tree=rtfile.Get(tree_name)
        for branch in branches[tree_name]:
            print (tree_name,branch)
            br= tree.GetBranch(branch)
            n=br.GetEntries()
            data_new_osm[branch]=np.array([get_entry(br,branch,i) for i in range(n)])


    #print (len(data_new['Waveform_Raw']), len(data_new['Charge_Corrected']))
    
    all_data={'data_config':data_new_config,'data_log':data_new_log,'data_event':data_new_event,'data_osm':data_new_osm,'data_header':data_new_header}
    
    
    np.savez_compressed(pklfile,data_config=data_new_config,data_log=data_new_log,data_header=data_new_header,data_osm=data_new_osm,data_event=data_new_event)
    #return

if __name__ == '__main__':
    branches={}
    branches['Tree_Event'] =['Detector','Channel_Passed_Threshold',
                             'Trigg_Threshold','Charge_Corrected','Peak_Height_Corrected','Peak_Height_Raw',
                             'Waveform_Raw','nsec_Online']
    branches['Tree_Detector_Config'] =['sigma_ovr_thresh']
                             
    muon_calib_files=glob.glob('../muon_calib_data/2020*root')
        
    for temp in muon_calib_files:
        process_and_save(temp)

