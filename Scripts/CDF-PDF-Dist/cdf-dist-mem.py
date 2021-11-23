#!/usr/bin/python3
import numpy as np
import csv
import matplotlib.pyplot as plt
# import pandas as pd
import os
from pathlib import Path
# matplotlib inline

# files = ["matrix-multiplication-low_10_1_nano_logs.csv"]
app_name_list = [
    # "image-classification-alexnet-cpu",
    # "image-classification-with-cpu",
    # "sentiment-analysis",
    # "matrix-multiplication-high",
    # "iperf3",
    # "image-classification-with-cuda",
    "object-classification-yolo-no-gpu",
    "image-processing-pillow",
    # "floating-point-operation-cosine",
    # "fast-fourier-transform",
    # "matrix-multiplication-medium",
    # "dd-cmd",
    # "object-classification-yolo-gpu",
    # "floating-point-operation-sine",
    # "speech-to-text",
    # "sorter",
    # "image-classification-alexne-gpu",
    # "matrix-multiplication-low",
    # "floating-point-operation-sqrt",
]

device_name_list = ["NANO", "RPI"]

for app_name in app_name_list:
    Path("../cdf-graphs/{0}/memory".format(app_name)).mkdir(parents=True, exist_ok=True)
    for device_name in device_name_list:
        print(device_name) #remove
        # Path for concurrency
        conc_logs_path = "../concurrency/{0}/{1}/cpu_mem_output".format(device_name, app_name)
        all_files = os.listdir(conc_logs_path)

        Mem = []

        for each_csv_file_name in all_files:
            # ignore <app_name>_cpu_mem_readings csv file
            if each_csv_file_name == "{0}_cpu_mem_readings.csv".format(app_name):
                continue
            path_to_open_each_csv_file="{0}/{1}".format(conc_logs_path, each_csv_file_name)
            with open(path_to_open_each_csv_file,  "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if len(row) < 9:
                        continue
                    if row[6] == " -- / --" :
                        continue
                    mem_usage = row[6].strip()[:-14]
                    if row[6].strip()[-14:-13] == "G" :
                        mem_usage = float(mem_usage) * 1024
                    if row[6] == " -- / --" :
                        continue
                    Mem.append(mem_usage)

            # No of data points used
            N = len(Mem)

            # normal distribution
            x = np.sort(Mem)

            # get the cdf values of y
            y = np.arange(N) / float(N)

            # plotting
            plt.figure(figsize=(8, 4))

            plt.title('CDF with '+each_csv_file_name, fontsize=20)
            plt.xlabel('Memory MiB', fontsize=18)
            plt.ylabel('Probability', fontsize=18)
            plt.tick_params(axis="x", labelsize=16)
            plt.tick_params(axis="y", labelsize=16)
            # not sure if this line should be here or not. Pasted in from PDF script.
#             plt.xticks([0, 500, 1000, 1500, 2000])
            plt.tight_layout()

            plt.plot(x, y, 'b',  linewidth=3)

            fname = "{0}-cdf-dist".format(each_csv_file_name)

            save_path = "../cdf-graphs/{0}/memory/{1}-mem.pdf".format(app_name, fname)
            print(save_path)
            plt.savefig(save_path)
            # plt.show()
            plt.close()
