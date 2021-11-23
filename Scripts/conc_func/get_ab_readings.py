#!/usr/bin/env python3

import re
import os

# *******************************************************************************************************************************************************************************
# Author: Chinmay Kulkarni                                                                                                                                                      *
# University: The University of Georgia                                                                                                                                         *
# Code Description: This file contains the functions which will be used for getting all the required numbers from the apache benchmark output.                                  *
# *******************************************************************************************************************************************************************************

def get_required_values_from_all_ab_output(path_where_the_ab_output_files_present, appName):
    # writing column names to the file appName_ab_readings.csv
    with open("../concurrency/{0}/ab_output/{0}_ab_readings.csv".format(appName), "a") as f:
            f.write("Concurrency,Total_Time(seconds),Time_for_Each_Group(seconds)\n")
    # read all the file names in the
    all_files=os.listdir(path_where_the_ab_output_files_present)
    only_txt_file_names = filter(lambda x: x[-4:] == '.txt', all_files)

    for each_text_file_name in only_txt_file_names:
        path_to_open_each_text_file="{0}/{1}".format(path_where_the_ab_output_files_present, each_text_file_name)
        with open(path_to_open_each_text_file, "r") as f:
            output_data=f.readlines()
        # Putting all the output data in a single string
        entire_data="".join(output_data)

        # Now from entire data we will find 
        concurrecny_level = re.findall(r'^(Concurrency Level:)([ ]*)([0-9]{3}|[0-9]{2}?|[0-9]{1})*', entire_data, flags=re.MULTILINE)
        time_taken_for_tests = re.findall(r'^(Time taken for tests:)([ ]*)([\d]*[.]?[\d]+)', entire_data, flags=re.MULTILINE)
        complete_requests = re.findall(r'^(Complete requests:)([ ]*)([0-9]{3}|[0-9]{2}?|[0-9]{1})+', entire_data, flags=re.MULTILINE)
        # print("concurrency level:{0}, time_for_tests:{1}, complete_req:{2}".format(concurrecny_level, time_taken_for_tests, complete_requests))
        time_taken_for_each_group = float((float(time_taken_for_tests[0][2]) * float(concurrecny_level[0][2]))/float(complete_requests[0][2]))
        # Arranging the data in csv pattern and store them in a file in same path as output files
        data_to_store = "{0}, {1}, {2:.3f}\n".format(concurrecny_level[0][2], time_taken_for_tests[0][2], time_taken_for_each_group)
        # appneding this data to file sorter_ab_readings.txt
        with open("../concurrency/{0}/ab_output/{0}_ab_readings.csv".format(appName), "a") as f:
            f.write(data_to_store)

def main():
    # appanme = "image-classification-alexnet-cpu"
    appanme = "image-classification-alexnet-cpu"
    # appanme = "image-classification-with-cpu"
    # appanme = "sentiment-analysis"
    # appanme = "matrix-multiplication-high"
    # appanme = "iperf3"
    # appanme = "image-classification-with-cuda"
    # appanme = "object-classification-yolo-no-gpu"
    # appanme = "image-processing-pillow"
    # appanme = "floating-point-operation-cosine"
    # appanme = "fast-fourier-transform"
    # appanme = "matrix-multiplication-medium"
    # appanme = "dd-cmd"
    # appanme = "object-classification-yolo-gpu"
    # appanme = "floating-point-operation-sine"
    # appanme = "speech-to-text"
    # appanme = "sorter"
    # appanme = "image-classification-alexnet-gpu"
    # appanme = "matrix-multiplication-low"
    # appanme = "floating-point-operation-sqrt"
    print("WOrking") #remove
    path = "../concurrency/{0}/ab_output/".format(appanme)
    get_required_values_from_all_ab_output(path, appanme)
    # get_required_values_from_all_ab_output("./concurrency/sorter/ab_output/", "sorter")

if __name__=='__main__':
    main()
