#!/usr/bin/env python3

import re
import os
import subprocess

def get_average_cold_warm_values_in_csv(path_where_the_ab_output_files_present, appName):
    Varlist = [0,0,0,0,0]    
    #datafile = "./ab_cws_{0}_nano_logs_{1}.data".format(appName, sets)
    all_files=os.listdir(path_where_the_ab_output_files_present)
    only_data_file_names = filter(lambda x: x[-5:] == '.data', all_files)
    no_of_files = len(list(filter(lambda x: x[-5:] == '.data', all_files)))
    print(no_of_files)
    for each_data_file_name in only_data_file_names:
        print(each_data_file_name) #remove
        path_to_open_each_data_file="{0}/{1}".format(path_where_the_ab_output_files_present, each_data_file_name)
        first_check= '{ print $6, $9 }'
        second_check= '{ print $2 }'
        output = "sed '1d' {0} | awk  '{1}' | sort | awk '{2}'".format(path_to_open_each_data_file, first_check, second_check)
        os.system(output + "> temp.txt")
        with open("temp.txt", 'r') as file:
            data = file.read()
            linebyline = data.split("\n")
            file.close()
            Varlist[0] += int(linebyline[0])
            Varlist[1] += int(linebyline[1])
            Varlist[2] += int(linebyline[2])
            Varlist[3] += int(linebyline[3])
            Varlist[4] += int(linebyline[4])

    count = 1
    with open("./cold_warm_start_AB/{0}/NANO/{1}_ab_cold_warm_reading.csv".format(appName, appName), "a") as f:
#    with open("./cold_warm_start_AB/{0}/RPI/{1}_ab_cold_warm_reading.csv".format(appName, appName), "a") as f:
        f.write("Execution, Avg_Time(milliseconds)\n")
        for l in Varlist:
            l = l/no_of_files
            print(l)
            f.write("{0}, {1}\n".format(count, l))
            count = count +1

def main():
    #appanme = "image-classification-alexnet-cpu" #has issues
    #appanme = "image-classification-with-cpu"
#    appanme = "sentiment-analysis"
    #appanme = "matrix-multiplication-high"
    # appanme = "iperf3"
    # appanme = "image-classification-with-cuda" #has issues
    # appanme = "object-classification-yolo-no-gpu"
    # appanme = "image-processing-pillow"
    # appanme = "floating-point-operation-cosine"
    # appanme = "fast-fourier-transform"
    # appanme = "matrix-multiplication-medium"
    # appanme = "dd-cmd"
    # appanme = "object-classification-yolo-gpu" #has issues
    # appanme = "floating-point-operation-sine"
    # appanme = "speech-to-text"
    # appanme = "sorter"
    # appanme = "image-classification-alexnet-gpu" #has issues
    # appanme = "matrix-multiplication-low"
#    appanme = "floating-point-operation-sqrt"    # Sample appname to test the file
#    appame = "image-processing-pillow"

    app_name_list = [
#    "image-classification-alexnet-cpu",
#    "image-classification-with-cpu",
#    "sentiment-analysis",
#    "matrix-multiplication-high",
#    "iperf3",
#    "image-classification-with-cuda",
#    "object-classification-yolo-no-gpu",
#    "image-processing-pillow",
#    "floating-point-operation-cosine",
#    "fast-fourier-transform",
#    "matrix-multiplication-medium",
    "dd-cmd",
#    "object-classification-yolo-gpu",
#    "floating-point-operation-sine",
#    "speech-to-text",
#    "sorter",
#    "image-classification-alexnet-gpu",
#    "matrix-multiplication-low",
#    "floating-point-operation-sqrt",
#     "dd-cmd"
    ]

    for appanme in app_name_list:
        path_where_the_ab_output_files_present = "./cold_warm_start_AB/{0}/NANO".format(appanme)
#        path_where_the_ab_output_files_present = "./cold_warm_start_AB/{0}/RPI".format(appanme)

    # sample invoke
        get_average_cold_warm_values_in_csv(path_where_the_ab_output_files_present, appanme)

if __name__=='__main__':
    main()
