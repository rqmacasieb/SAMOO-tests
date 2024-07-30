# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 21:15:54 2023

@author: mac732
"""

import pandas as pd
import os
import shutil
import glob
import pyemu
from distutils.dir_util import copy_tree
import datetime

#update outer repository
outer_dirlist = [os.path.basename(x) for x in glob.glob("./outer_[0-999]*", recursive=True)]
outer_dirlist = sorted(outer_dirlist, key = lambda x: int(x.split("_")[1]))

path_in = os.path.join("template", "model", "input")

max_infill = 100
swarm_size = 100

def mogp():
    inner_iter_dirs = [os.path.basename(x) for x in glob.glob("./mogp_[0-999]*", recursive=True)]
    inner_iter_dirs = sorted(inner_iter_dirs, key = lambda x: int(x.split("_")[1]))

    if len(inner_iter_dirs) ==0:
        next_inner_index = 1
    else:
        next_inner_index = int(inner_iter_dirs[-1].split("_",1)[1])+1

    pyemu.os_utils.start_workers("template","./pest/pestpp-mou","./pest/bm2_gp.pst",num_workers=64,worker_root=".",master_dir="./mogp_"+str(next_inner_index))  


def restart_prep():
    
    inner_dirlist = [os.path.basename(x) for x in glob.glob("./mogp_[0-999]*", recursive=True)]
    inner_dirlist = sorted(inner_dirlist, key = lambda x: int(x.split("_")[1]))
    
    #update outer repo
    if (len(outer_dirlist)<=2):
        prev_dv_file = glob.glob(os.path.join(".", outer_dirlist[-2], "*.archive.dv_pop.csv"), recursive= True)
        prev_dv = pd.read_csv(prev_dv_file[0])
        prev_obs_file = glob.glob(os.path.join(".", outer_dirlist[-2], "*.archive.obs_pop.csv"), recursive= True)
        prev_obs = pd.read_csv(prev_obs_file[0])
    else:
        prev_dv_file = glob.glob(os.path.join(".", outer_dirlist[-2], "outer_repo", "*.archive.dv_pop.csv"), recursive= True)
        prev_dv = pd.read_csv(prev_dv_file[0])
        prev_obs_file = glob.glob(os.path.join(".", outer_dirlist[-2], "outer_repo", "*.archive.obs_pop.csv"), recursive= True)
        prev_obs = pd.read_csv(prev_obs_file[0])
    
    curr_dv_file = glob.glob(os.path.join(".", outer_dirlist[-1], "*0.dv_pop.csv"), recursive= True)
    curr_dv = pd.read_csv(curr_dv_file[0])
    
    curr_obs_file = glob.glob(os.path.join(".", outer_dirlist[-1], "*0.obs_pop.csv"), recursive= True)
    curr_obs = pd.read_csv(curr_obs_file[0])
    
    merged_dv_file = pd.concat([prev_dv, curr_dv], ignore_index= True)
    merged_dv_file.drop_duplicates(subset = 'real_name', inplace = True)
    merged_dv_file.to_csv(os.path.join(".", "template", "update_repo", "merged.dv_pop.csv"), index = False)
    
    merged_obs_file = pd.concat([prev_obs, curr_obs], ignore_index= True)
    merged_obs_file.drop_duplicates(subset = 'real_name', inplace = True)
    merged_obs_file.to_csv(os.path.join(".", "template", "update_repo", "merged.obs_pop.csv"), index = False)
    
    shutil.copytree(os.path.join("outer_rundir", "template"), "temp")
    copy_tree(os.path.join("template", "update_repo"), "temp")
    
    #update training dataset
    
    infill_data = pd.concat([curr_dv, curr_obs], axis=1)
    
    training_data = pd.read_csv(os.path.join(path_in, "trainingdata.csv"))
    training_data.columns = infill_data.columns.values
    training_data = pd.concat([training_data, infill_data], ignore_index= True)
    training_data.to_csv(os.path.join(path_in, "trainingdata.csv"), index=False)
    
    #run pestpp mou in pareto sorting mode
    os.chdir("./temp")
    os.system("./pestpp-mou outer_repo.pst")
    os.chdir((".."))
    
    #copy outer repo update files to outer dir
    subdir = os.path.join(outer_dirlist[-1], "outer_repo")
    if os.path.exists(subdir):
        os.remove(subdir)
    os.mkdir(subdir)
    
    outer_repo_sumlist = glob.glob(os.path.join("temp", "outer_repo.pareto*"), recursive=True)
    for name in outer_repo_sumlist:
        shutil.copy(name, subdir)
        
    outer_repo_sumlist = glob.glob(os.path.join("temp", "outer_repo.archive*"), recursive=True)
    for name in outer_repo_sumlist:
        shutil.copy(name, subdir)
    
    shutil.rmtree("temp")
 
    #generate restart files for next set of inner iters    
    dv_restart = pd.read_csv(os.path.join(subdir, "outer_repo.archive.dv_pop.csv"))
    obs_restart = pd.read_csv(os.path.join(subdir, "outer_repo.archive.obs_pop.csv"))  
    
    curr_dv = curr_dv[~curr_dv['real_name'].isin(dv_restart['real_name'].values)]
    if dv_restart.shape[0] < swarm_size:
        if swarm_size-dv_restart.shape[0] <= curr_dv.shape[0]:
            curr_dv_subsample = curr_dv.sample(n=swarm_size-dv_restart.shape[0])
        else:   
            curr_dv_subsample = curr_dv
    
        curr_obs_subsample = curr_obs[curr_obs['real_name'].isin(curr_dv_subsample['real_name'])]
        dv_restart = pd.concat([dv_restart, curr_dv_subsample], ignore_index= True)
        obs_restart = pd.concat([obs_restart, curr_obs_subsample], ignore_index= True)
        
    else:
        dv_restart = dv_restart.sample(n=swarm_size)
        obs_restart = obs_restart[obs_restart['real_name'].isin(dv_restart['real_name'])]
    
    dv_restart = dv_restart.sort_values('real_name')
    obs_restart = obs_restart.sort_values('real_name')
    
    # sd_init = pd.read_csv(os.path.join("template", "model", "preproc", "sd_aug.csv")).loc[0:obs_restart.shape[0]-1,:]
    # for col in list(sd_init.columns):
        # obs_restart[col] = 0.001
    obs_restart.to_csv(os.path.join(path_in,"mogp_bm2.obs_pop.csv"), index=False)
    dv_restart.to_csv(os.path.join(path_in,"mogp_bm2.dv_pop.csv"), index=False)
    
    shutil.copy(os.path.join(subdir, "outer_repo.archive.obs_pop.csv"), path_in)

def start_prep():
    curr_dv_file = glob.glob(os.path.join(".", outer_dirlist[-1], "*0.dv_pop.csv"), recursive= True)
    curr_dv = pd.read_csv(curr_dv_file[0])
    curr_obs_file = glob.glob(os.path.join(".", outer_dirlist[-1], "*0.obs_pop.csv"), recursive= True)
    curr_obs = pd.read_csv(curr_obs_file[0])
    
    if os.path.exists(os.path.join(path_in, "trainingdata.csv")):
        os.remove( os.path.join(path_in, "trainingdata.csv"))
         
    infill_data = pd.concat([curr_dv,curr_obs],axis=1)
    infill_data.to_csv(os.path.join(path_in, "trainingdata.csv"), index = False)
    
    # sd_init = pd.read_csv(os.path.join("template", "model", "preproc", "sd_aug.csv")).loc[0:curr_obs.shape[0]-1,:]
    # obs_pop = pd.concat([curr_obs,sd_init], axis=1)
    curr_obs.to_csv(os.path.join(path_in,"mogp_bm2.obs_pop.csv"), index=False)
    
    curr_obs_repo = pd.read_csv(glob.glob(os.path.join(".", outer_dirlist[-1], "*0.archive.obs_pop.csv"), recursive= True)[0])
    curr_obs_repo.to_csv(os.path.join(path_in,"outer_repo.archive.obs_pop.csv"), index=False)
    
    curr_dv.to_csv(os.path.join(path_in,"mogp_bm2.dv_pop.csv"), index=False)

def resample():      
    outer_pareto_file = glob.glob(os.path.join(outer_dirlist[-1],"*.pareto.archive.summary.csv"), recursive=True)
    outer_pareto = pd.read_csv(outer_pareto_file[0])
    
    inner_dirlist = [os.path.basename(x) for x in glob.glob("./mogp_[0-999]*", recursive=True)]
    inner_dirlist = sorted(inner_dirlist, key = lambda x: int(x.split("_")[1]))

    #get all dv data
    all_dv = pd.DataFrame()
    csvfiles = glob.glob(os.path.join(inner_dirlist[-1], "pest",'*[0-999].dv_pop.csv'), recursive=True)
    csvfiles = sorted(csvfiles, key = lambda x: int(x.split(".dv")[0].split(".")[1]))
    for name in csvfiles:
        inner_dv = pd.read_csv(name)
        all_dv = pd.concat([all_dv, inner_dv], ignore_index= True)

    #get inner iter data
    inner_pareto_file = glob.glob(os.path.join(inner_dirlist[-1], "pest", "*.pareto.trimmed.archive.summary.csv"), recursive=True)
    inner_pareto_summary = pd.read_csv(inner_pareto_file[0])
    
    inner_pareto = inner_pareto_summary[~inner_pareto_summary['member'].isin(outer_pareto['member'].values)]
    
    #perform infill selection
    n_infill = 0
    iter_n = max(inner_pareto['generation'])
    infill_pop = pd.DataFrame(columns = inner_pareto_summary.columns.values)
      
    while ((n_infill < max_infill) & (iter_n > 0)):     
        infill_sort = inner_pareto[inner_pareto["generation"] == iter_n]
        infill_sort = infill_sort[~infill_sort['member'].isin(infill_pop['member'])]
        infill_sort.drop_duplicates(subset = 'member', inplace = True)
        
        if infill_sort.shape[0]>0:
            infill_sort = infill_sort.sort_values(by='nsga2_crowding_distance', ascending = False)
            infill_add = infill_sort.head(max_infill-n_infill)
            infill_pop = pd.concat([infill_pop, infill_add], ignore_index=True)
            n_infill = infill_pop.shape[0]
        else:
            iter_n -= 1
    
    infill_dv_pop = all_dv[all_dv['real_name'].isin(infill_pop['member'].values)]

    #save to outer iter dir
    infill_dv_pop.to_csv(os.path.join(os.path.join("outer_rundir","template"),"infill.dv_pop.csv"), index=False)
    infill_dv_pop.to_csv(os.path.join(os.path.join("outer_rundir","master"),"infill.dv_pop.csv"), index=False)
    
    infill_pop.to_csv(os.path.join(os.path.join("outer_rundir","template"),"infill.gpr.csv"), index=False)
    infill_pop.to_csv(os.path.join(os.path.join("outer_rundir","master"),"infill.gpr.csv"), index=False)

    print("\nInfill ensemble saved. Finished: " + str(datetime.datetime.now()) + "\n")

if __name__ == "__main__":
    if outer_dirlist[-1].endswith("_0"):
        start_prep()
    else:
        restart_prep()
    
    mogp()
    resample()
        
