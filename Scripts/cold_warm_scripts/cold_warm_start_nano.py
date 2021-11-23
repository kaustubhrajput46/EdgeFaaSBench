#!/usr/bin/env python3

import os
import json
import argparse
import time as t
import subprocess
from threading import *

# Fetch the path of script to be executed on the edge device.
def get_script_path_at_edge_device(edgeLoginPassword, edgeLoginName, edgeHostIp):
    current_work_directory_command = "sshpass -p '{0}' ssh {1}@{2} 'pwd'".format(edgeLoginPassword, edgeLoginName, edgeHostIp)
#    current_work_directory_command = "echo '{0}' | sshpass -p '{0}' ssh -tt {1}@{2} 'pwd'".format(edgeLoginPassword, edgeLoginName, edgeHostIp)
    try:
        work_dir_edge_device = subprocess.check_output(current_work_directory_command, shell=True, text=True)
        dir_of_scripts = "{0}/faas/functions/scripts/".format(work_dir_edge_device.strip())
#        dir_of_scripts = "{0}/faas/functions/scripts/".format(work_dir_edge_device.split('\n')[1].strip())
        return dir_of_scripts
    except Exception as e:
        print("\nCode failed with: {0}\n".format(e))
        print("*************************************************************************************************************************************************************")
        exit(1)

def invoke_application_on_edge_device(numRuns, numRequests, timeOut, appName, edgeHostIp, edgeOpenFaaSPort, edgeLoginPassword, edgeLoginName, dockerHubUsername):
    sets = 1
    loop = numRuns // 5
    try:
        while sets <= loop:
            # Deploy command to set replica as 0 on edge device of a given appName.
            cold_start_deployment_command_to_execute = "faas-cli deploy -f https://raw.githubusercontent.com/kaustubhrajput46/datasets/main/jetson_nano_ymls/{0}.yml".format(appName)
            subprocess.run(cold_start_deployment_command_to_execute, shell=True, text=True)

            # time for previous container to be removed so that we can have a cold start scenario.
            t.sleep(30)

# Issue - Out.data is not being saved in the right way
# Problem faced - Cannot log data properly for all the applications at the same time.
# Proposed Sol - 
#       - We can maintain a directory structure for saving .data of ap.
#           - directory structure
#           - cold_warm_start_AB/<APPLICATION_NAME>/NANO/ab_cws_<APPLICATION_NAME>_nano_logs_<sets>.data
#       - We can customize the file name.
#            - name
#            - ab_cws_<APPLICATION_NAME>_nano_logs_<sets>.data

# Issue - Should v -2 flag be hardcoded here ?
            # .data file name with path generated from -g flag of apache bench command.
            datafile = "./cold_warm_start_AB/{0}/NANO/ab_cws_{1}_nano_logs_{2}.data".format(appName, appName, sets)
            print("Datafile name is - ")
            print(datafile) #reomve
            ab_logs="cold_warm_start_AB/{0}/NANO/ab_cws_{1}_nano_logs_{2}.txt".format(appName, appName, sets)
            print("ab file name is - ")
            print(ab_logs) #reomve
            # creating apache benchamrk command to be executed in shell script
            apache_benchmark_command_to_execute = "ab -n 5 -c 1 -s {0} -l -g {5} -v 2 http://{2}:{3}/function/{4}".format(timeOut, sets, edgeHostIp, edgeOpenFaaSPort, appName, datafile)
            print(apache_benchmark_command_to_execute);
            # get the remote script's path on edge device.
            scriptPath = get_script_path_at_edge_device(edgeLoginPassword, edgeLoginName, edgeHostIp)

            # name of script to be executed
            script = "{0}create_logs_cold_warm_nano.sh".format(scriptPath)

            # execute the script on local machine.
            edge_device_script_to_execute = "sh cold_warm_device_script.sh {0} {1} {2} {3} {4} {5} {6} '{7}' {8} {9} {10}".format(edgeLoginPassword, edgeLoginName, edgeHostIp, script, appName, dockerHubUsername, sets, apache_benchmark_command_to_execute, scriptPath, datafile, ab_logs)
            subprocess.run(edge_device_script_to_execute, shell=True, text=True)

            # increment the value of set
            sets = sets + 1

            # Introducing sleep time to give some rest to edge device.
            t.sleep(15)

    except Exception as e:
        print("\nCannot run apache benchmark due to error:{0}\n".format(e))
        print("*************************************************************************************************************************************************************")
        exit(1)
