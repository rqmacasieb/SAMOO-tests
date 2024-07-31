import os
import multiprocessing as mp
import numpy as np
import pandas as pd
import pyemu
import flopy
import shutil

ncols = 4000
wl_loc = 2800

def get_arch_data ():
    args = {}
    with open("artrch.dat",'r') as f:
        for line in f:
            raw = line.strip().split()
            args[raw[0]] = float(raw[1])
    
    return args

def process_ucn():
    ucn = pd.read_csv(os.path.join("trans.conc.csv"))
    df = pd.read_csv(os.path.join("flow.wel_stress_period_data_scenario.txt"),
                    delim_whitespace=True, header=None, names=["l", "r", "c", "flux", "concen"])
    df = df.loc[85:92, :]
    
    args = get_arch_data()
   
    ar_total = args['ar_rate_1'] + args['ar_rate_2']

    wel_conc = {}
    flx_dict = {}
    tot_flx = 0
    for l,r,c,flx in zip(df.l,df.r,df.c,df.flux):
        name = "WELL_"+ str(l) +"_" + str(r) + "_" + str(c)
        wel_conc[name] = ucn.loc[:,name].values
        flx_dict[name] = -1. * flx
        tot_flx += flx_dict[name]

    df = pd.DataFrame(wel_conc,index=np.round(ucn.loc[:,'time'].values,5))
    df.loc[:,"time"] = df.index
    cols = df.columns.to_list()
    cols.sort()
    cols.remove("time")
    cols.insert(0,"time")
    df = df.loc[:,cols]
    
    # print all time series data of mean conc [for debugging purposes]
    mn_conc_tstp = []
    lines = ["t_scen,mean_concen\n"]
   
    for t in df.time:
        #if t > predevprd:
            concen = df.loc[df.time == t,:].iloc[0].to_dict()
            tflx,tmas = 0,0
            for n,f in flx_dict.items():
                tflx += f
                try:
                    concen[n] = float(concen[n])
                except:
                    concen[n] = 0
                if concen[n] < 0:
                    concen[n] = 0
                tmas += f * concen[n]
            mn_conc_tstp.append(tmas / tflx)
            lines.append("{0},{1}\n".format(t,tmas / tflx))
    
    if max(mn_conc_tstp) > 1:
        pf_salinity = 0
    else:
        pf_salinity = 1

    
    t_mean_conc_file_name = "mean_conc_at_t.csv" 
    with open(t_mean_conc_file_name,'w') as f:
        for line in lines:
            f.write(line)
            
    with open("mean_concen.dat",'w') as f:
        f.write("mean_concen {0}\n".format(max(mn_conc_tstp)))  
        f.write("salinity {0}\n".format(max(mn_conc_tstp)))
        f.write("total_pump_rate {0}\n".format(tot_flx)) 
        f.write("ar_rate_total {0}\n".format(ar_total))
        f.write("ar_rate_t {0}\n".format(ar_total))
        f.write("pf_salinity {0}\n".format(pf_salinity))
        f.write("mean_conc_sd 0\n")
        f.write("salinity_sd 0\n")
        f.write("ar_rate_total_sd 0\n")
        

def add_artrch():
    args = get_arch_data()
    
    org_wel_list_file = "flow.wel_stress_period_data_scenario_base.txt"
    new_wel_list_file = "flow.wel_stress_period_data_scenario.txt"
    lines = []
    with open(org_wel_list_file,'r') as f:
        for line in f:
            if len(line.strip()) > 0:
                lines.append(line)
    
    lines.append("40 1 2750 {0} 0.0\n".format(args["ar_rate_1"]))
    lines.append("85 1 2000 {0} 0.0\n".format(args["ar_rate_2"]))
    
    with open(new_wel_list_file,'w') as f:
        for line in lines:
            f.write(line)
            
def head_dd():
    hds_0 = flopy.utils.HeadFile("flow_ic.hds").get_data()[:,0,wl_loc-1]
    hds = pd.read_csv(os.path.join("flow.hds.csv")).to_numpy()

    for i in range(len(hds_0)):
        if hds_0[i] != -1e+30:
            hds_strt = hds_0[i]
            break
    
    hds_scen = []
    #hds = pd.read_csv(os.path.join("flow.hds.csv")).to_numpy()[:,1:]
    for i in range(hds.shape[0]):
        for j in range(1,hds.shape[1]):
            if hds[i][j] != -1e+30:
                hds_scen.append(hds[i][j])
                break
    
    dd = hds_strt - hds_scen
    with open("dd_at_t.csv","w") as f:
        for line in dd:
            f.write("{0:5.6f}\n".format(line))

    #ucn = pd.read_csv("trans.wl.conc.csv").to_numpy()[:,1:]
    
    if max(dd) > 5.68:
        pf_wetland_dd = 0
    else:
        pf_wetland_dd = 1
    
    with open("ar_wl_ddown.csv",'w') as f:
        f.write("qname,value\n")
        f.write("scen_max_dd,{0:15.6E}\n".format(max(dd)))
        f.write("wetland_dd_sd,0\n")
        f.write("pf_wetland_dd,{0:15.6E}\n".format(pf_wetland_dd))

        
def main():

    try:
       os.remove(r'pump_well_concen.csv')
    except Exception as e:
       print(r'error removing tmp file:pump_well_concen.csv')
    try:
       os.remove(r'mean_concen.dat')
    except Exception as e:
       print(r'error removing tmp file:mean_concen.dat')
    try:
       os.remove(r'flow.wel_stress_period_data_scenario.txt')
    except Exception as e:
       print(r'error removing tmp file:flow.wel_stress_period_data_scenario.txt')
    try:
      os.remove(r'ar_heads.csv')
    except Exception as e:
      print(r'error removing tmp file:ar_heads.csv')
    
    add_artrch()

    pyemu.os_utils.run('mf6')

    process_ucn()
    head_dd()

if __name__ == '__main__':
    mp.freeze_support()
    main()

