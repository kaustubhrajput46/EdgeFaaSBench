#!/usr/bin/env python3

import os
import json
import argparse
import time as t
import subprocess
from threading import *

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
