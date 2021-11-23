#!/usr/bin/env python3

import os
import warnings
import pandas as pd
warnings.filterwarnings('ignore')

# *******************************************************************************************************************************************************************************
# Author: Chinmay Kulkarni                                                                                                                                                      *
# University: The University of Georgia                                                                                                                                         *
# Code Description: This file contains the functions which will be used for getting all the required numbers from the apache benchmark output.                                  *
# *******************************************************************************************************************************************************************************

def get_required_values_from_all_cpu_mem_output(path_where_the_cpu_mem_output_files_present, appName):
    # Reading all the csv file from the concurrency/appname/cpu_mem_output folder
    all_csv_files = os.listdir(path_where_the_cpu_mem_output_files_present)

    # Keeping only csv file names in the list
    only_csv_file_names = filter(lambda x: x[-4:] == '.csv', all_csv_files)
    
    # column names to be given to the data which is going to be stored in the pandas dataframe
    col_names = ['TP','Concurrency','Loop','Container_ID','Appname','CPU','Mem_usage','Mem_perc','NetIO','BlockIO']
    
    for each_csv_file in only_csv_file_names:
        df = pd.read_csv("../concurrency/{0}/cpu_mem_output/{1}".format(appName,each_csv_file), names=col_names)
        
        # Filtering out rows which contains CPU percentage usage as " --"
        df = df[df.CPU != " --"]
        
        # Removing "%" from the columns 5 and 7 which contains CPU and MEM usage in percentage for mathematical operation
        df[col_names[5]] = df[col_names[5]].str.rstrip('%')
        df[col_names[7]] = df[col_names[7]].str.rstrip('%')
        
        # Splitting the Mem_used/Total_mem based on "/" with column names as Mem_used,Total_mem
        df[["Mem_used","Total_mem"]] = df.Mem_usage.str.split("/", expand=True)
        
        # updating the old dataframe df with only needed data   
        df=df[["Concurrency","Loop","Container_ID","Appname","CPU","Mem_used","Total_mem"]]
        
        # Extracting only numbers from Mem_used & Total_mem column
        df["Mem_used"] = df["Mem_used"].str.extract(r'(\d+.+\d)')
        df["Total_mem"] = df["Total_mem"].str.extract(r'(\d+.+\d)')
        
        # Converting CPU and MEM_perc columns from object to float datatype to perform mean operation
        df['CPU'] = df['CPU'].astype(str).astype(float)
        df['Mem_used'] = df['Mem_used'].astype(str).astype(float)
        df['Total_mem'] = df['Total_mem'].astype(str).astype(float)
        
        # Filtering out rows which contains CPU percentage usage below 10.00%
        df = df[df.CPU > 10.00]
        
        # For conversion of GiB values into MiB values
        df["Mem_used"] = df["Mem_used"].apply(lambda x: x * 1000 if x < 4 else x)
        
        # Taking values from the filtered dataframe
        concurrency = df['Concurrency'].iloc[0]
        container_id = df['Container_ID'].iloc[0]
        appname = df['Appname'].iloc[0]
        avg_CPU = df['CPU'].mean()
        avg_mem = df['Mem_used'].mean()
        total_mem = df['Total_mem'].iloc[0]
        
        # Creating a row record to write it to csv file
        row_record = "{0},{1},{2},{3:.2f},{4:.2f},{5:.2f}\n".format(concurrency, container_id, appname, avg_CPU, avg_mem, total_mem)
        
        with open("../concurrency/{0}/cpu_mem_output/{0}_cpu_mem_readings.csv".format(appName), "a") as f:
            f.write(row_record)

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

    path = "../concurrency/{0}/cpu_mem_output/".format(appanme)
    get_required_values_from_all_cpu_mem_output(path, appanme)
    # get_required_values_from_all_ab_output("./concurrency/sorter/ab_output/", "sorter")


    # get_required_values_from_all_cpu_mem_output("../concurrency/matrix-multiplication-low/cpu_mem_output/", "matrix-multiplication-low")

if __name__=='__main__':
    main()