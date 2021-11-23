#!/usr/bin/env python3

import json
import time as t
import subprocess

def get_config_values_of_edge_device(pathToConfigFile):
    try:
        with open(pathToConfigFile) as configFile:
            data = json.load(configFile)
            edgeLoginName = data['edgeLoginName']
            edgeLoginPassword = data['edgeLoginPassword']
            edgeHostIp = data['edgeHostIp']
            edgeOpenFaaSPort = data['edgeOpenFaaSPort']
            dockerHubUsername = data['dockerHubUsername']
        print("\nSuccessfully read the configuration values from the {0} config file...\n".format(pathToConfigFile))
        return (edgeLoginName, edgeLoginPassword, edgeHostIp, edgeOpenFaaSPort, dockerHubUsername)
    
    except IOError as e:
        first_reason = "Path where edge_configuration.json file is incorrect."
        second_reason = "configuration file name is incorrect. File name should be \"edge_config.json\""
        third_reason = "Both path to configuration file and configuration file name is correct but the file is present at the mentioned path.\n  Then create a configuration file with name as \"edge_configuration.json\" in the path which you have mentioned and run the program again.\n  Please visit to \"https://github.com/kaustubhrajput46/Thesis/blob/master/faas_ck/scripts_to_run_on_laptop/edge_config.json\" for reference configuration file."
        print("\nCould not read from the configuration file due to error {0}".format(e))
        print("\nThere can be following reasons->\n")
        print("1.{0}\n\n2.{1}\n\n3.{2}\n".format(first_reason, second_reason, third_reason))
        print("*************************************************************************************************************************************************************")
        exit(1)
    
    except Exception as e:
        print("\nCould not read from the configuration file due to error {0}\n".format(e))
        print("*************************************************************************************************************************************************************")
        exit(1)

# ********************************************************************************************************************************************************************************
# Thread 1 --> Run sshpass command to invoke the required script on edge device based on application name entered by user.                                                       *
# Command 1 --> sshpass -p 'Reset@123' ssh ubuntu@192.168.1.6 'cd /home/ubuntu/faas/functions/scripts/ && /home/ubuntu/faas/functions/scripts/Image-Classification-With-CPU.py'  *
# Command 2 --> sshpass -p 'Reset@123' ssh ubuntu@192.168.1.6 'pwd'                                                                                                              *
# ********************************************************************************************************************************************************************************
def get_script_path_on_the_edge_device(edgeLoginPassword, edgeLoginName, edgeHostIp):
    # For Raspberry pi 4
    current_work_directory_command = "sshpass -p '{0}' ssh {1}@{2} 'pwd'".format(edgeLoginPassword, edgeLoginName, edgeHostIp)
    try:
        work_dir_edge_device = subprocess.check_output(current_work_directory_command, shell=True, text=True)
        # dir_of_scripts = "{0}/faas/functions/scripts/".format(work_dir_edge_device.split('\n')[1].strip())
        dir_of_scripts = "{0}/faas/functions/scripts/".format(work_dir_edge_device.strip())
        return dir_of_scripts
    except Exception as e:
        print("\nCode failed with: {0}\n".format(e))
        print("*************************************************************************************************************************************************************")
        exit(1)

def invoke_application_on_edge_device(numRuns, numRequests, timeOut, appName, edgeHostIp, edgeOpenFaaSPort, loop_number, edgeLoginPassword, edgeLoginName, dockerHubUsername):
    default_num_requests=20
    numRequests = 1
    print("Edge login name : " , edgeLoginName)
    if numRuns < default_num_requests:
        default_num_requests = numRuns
    try:
        while numRequests <= default_num_requests:
            apache_benchmark_command_to_execute = "ab -n {0} -c {1} -s {2} -l http://{3}:{4}/function/{5}".format(numRuns, numRequests, timeOut, edgeHostIp, edgeOpenFaaSPort, appName)
            # Get the script path from the edge device
            script_path = get_script_path_on_the_edge_device(edgeLoginPassword, edgeLoginName, edgeHostIp)
            script_name_to_execute = "{0}create_logs_concurrency.sh".format(script_path)
            # Executing the script on the laptop
            local_script = "sh concurrency_shell.sh {0} {1} {2} {3} {4} {5} {6} '{7}' {8} {9}".format(edgeLoginPassword, edgeLoginName, edgeHostIp, script_name_to_execute, appName, dockerHubUsername, numRequests, apache_benchmark_command_to_execute, script_path, loop_number)
            # Blocking call
            subprocess.run(local_script, shell=True, text=True)
            numRequests = numRequests + 1
            t.sleep(15)

    except Exception as e:
        print("\nCannot run apache benchmark due to error:{0}\n".format(e))
        print("*************************************************************************************************************************************************************")
        exit(1)
