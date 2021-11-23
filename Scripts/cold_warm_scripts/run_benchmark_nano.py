#!/usr/bin/env python3

import argparse
import time as t
from threading import *
from edge_device_config_val import *
from cold_warm_start_nano import *
from ab_txt_readings import *

def main():
    parser = argparse.ArgumentParser(description='RUN BENCHMARK TO GET STATISTICS FROM EDGE DEVICE WHO IS RUNNING OPENFAAS FRAMEWORK.')
    parser.add_argument('-n', metavar='NUM_RUNS',
                    help='Number of requests to perform for the benchmarking session. Default is to perform a single request at a time. This parameter is used for serial execution.',
                    type=int, default=50)
    parser.add_argument('-c', metavar= 'NUM_REQUESTS',
                    help='Number of multiple requests to perform at a time for the benchmarking session. Default is one request at a time. This parameter is used for parallel execution.',
                    type=int, default = 1)
    parser.add_argument('-s', metavar= 'TIMEOUT',
                    help='Maximum number of seconds to wait before the socket times out. Default is 30 seconds.',
                    type=int, default = 30)
    parser.add_argument('-appname', metavar='APPLICATION_NAME',
                    help='Name of the application which you want to test it out. appName should match with names mentioned in the https://github.com/kaustubhrajput46/Thesis/blob/master/faas_ck/app_names.txt file.',
                    type= str, required=True)
    parser.add_argument('-filepath', metavar='Path To Configuration JSON File.',
                    help='This file contains information about edge device such as username, password, IP address, port number where OpenFaaS framework is running.',
                    type=str, required=True)
    args = parser.parse_args()

    # This function will read json configuration file and get the required values and send them to invoke_script_based_on_application_name and invoke_application_on_edge_device.
    output = get_config_values_of_edge_device(args.filepath)
    edgeLoginName = output[0]
    edgeLoginPassword = output[1]
    edgeHostIp = output[2]
    edgeOpenFaaSPort = output[3]
    dockerHubUsername = output[4]

    # This function will run apache benchmark with required paramters mentioned by user or use the default ones to serially or parallely invoke the application on the edge device.
    thread = Thread(target=invoke_application_on_edge_device, args=(args.n, args.c, args.s, args.appname, edgeHostIp, edgeOpenFaaSPort, edgeLoginPassword, edgeLoginName, dockerHubUsername))
    try:
        thread.start()
        thread.join()
    except Exception as e:
        print("Could not start the thread due to:{0}".format(e))
        exit(1)

        # Sample appname to test the file
#    appName = "matrix-multiplication-low"
    path_where_the_ab_output_files_present = "./cold_warm_start_AB/{0}/NANO".format(args.appname)

    get_average_cold_warm_values_in_csv(path_where_the_ab_output_files_present, args.appname)

# calling the main function
if __name__=='__main__':
    main()
