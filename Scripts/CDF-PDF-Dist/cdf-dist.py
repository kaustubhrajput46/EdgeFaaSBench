#! /usr/bin/python3
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
    # "object-classification-yolo-no-gpu",
    # "image-processing-pillow",
    # "floating-point-operation-cosine",
    # "fast-fourier-transform",
    # "matrix-multiplication-medium",
    # "dd-cmd",
    # "object-classification-yolo-gpu",
    # "floating-point-operation-sine",
    # "speech-to-text",
    # "sorter",
    # "image-classification-alexne-gpu",
    "matrix-multiplication-low",
    "floating-point-operation-sqrt",
]

# device_name = "RPI"
device_name_list = ["NANO", "RPI"]
# app_name = "fast-fourier-transform"

for app_name in app_name_list:
    Path("./cdf-graphs/{0}".format(app_name)).mkdir(parents=True, exist_ok=True)
    for device_name in device_name_list:

        # Path for concurrency
        conc_logs_path = "concurrency\{0}\{1}\cpu_mem_output".format(device_name, app_name)
        all_files = os.listdir(conc_logs_path)

        CPUs = []
        # Mem = []

        for each_csv_file_name in all_files:
            CPUs = []
            print(each_csv_file_name) # remove
            # ignore <app_name>_cpu_mem_readings csv file
            if each_csv_file_name == "{0}_cpu_mem_readings.csv".format(app_name):
                continue
            path_to_open_each_csv_file="{0}/{1}".format(conc_logs_path, each_csv_file_name)
            with open(path_to_open_each_csv_file,  "r") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    if len(row) < 9:
                        continue
                    strip_percentage = row[5].strip()[:-1]
                    # remove records less than 10%
                    if strip_percentage:
                        if row[5] == " --" or float(strip_percentage) <= 10.00:
                            continue
                        # remove percent sign
                        CPUs.append(float(strip_percentage))

                    # TODO : Add memory content here

            # No of data points used
            N = len(CPUs)

            # normal distribution
            x = np.sort(CPUs)

            # get the cdf values of y
            y = np.arange(N) / float(N)

            # plotting

            plt.figure(figsize=(8, 4))

            plt.title('CDF with '+each_csv_file_name, fontsize=20)
            plt.xlabel('CPU %', fontsize=18)
            plt.ylabel('Probability', fontsize=18)
            plt.tick_params(axis="x", labelsize=16)
            plt.tick_params(axis="y", labelsize=16)
            plt.tight_layout()

            plt.plot(x, y, 'b',  linewidth=3)

            fname = "{0}-cdf-dist".format(each_csv_file_name)

            save_path = "./cdf-graphs/{0}/{1}.pdf".format(app_name, fname)
            plt.savefig(save_path)
            # plt.show()
            plt.close()
