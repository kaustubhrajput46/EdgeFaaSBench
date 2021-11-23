#!/usr/bin/env python3
import re
import os


def get_function_execution_times_from_ab_rpi(path_to_output, appname):
    ex_times = "{0}_rpi".format(appname)
    all_ab_outputs = os.listdir(path_to_output)
    only_text_files = filter(lambda x: x[-4:] == '.txt', all_ab_outputs)

    for each_text_file in only_text_files:
        path_to_each_text_file = "{0}/{1}".format(
            path_to_output, each_text_file)
        with open(path_to_each_text_file, "r") as f:
            output = f.readlines()
        op_in_single_line = "".join(output)

        function_execution_times = re.findall(
            r'(The function has executed successfully in )([0-9]+[.][0-9]+)( seconds)', op_in_single_line, flags=re.MULTILINE)
        if len(function_execution_times) != 0:
            for each_function_execution_time_tuple in function_execution_times:
                ex_times += ",{0}".format(
                    each_function_execution_time_tuple[1])
        else:
            function_execution_times = re.findall(
                r'(The function has executed succesfully in )([0-9]+[.][0-9]+)( seconds)', op_in_single_line, flags=re.MULTILINE)
            if len(function_execution_times) != 0:
                for each_function_execution_time_tuple in function_execution_times:
                    ex_times += ",{0}".format(
                        each_function_execution_time_tuple[1])
    ex_times += "\n"
    with open("./execcution_times.csv", "a") as f:
        f.write(ex_times)


def get_function_execution_times_from_ab_nano(path_to_output, appname):
    ex_times = "{0}_nano".format(appname)
    all_ab_outputs = os.listdir(path_to_output)
    only_text_files = filter(lambda x: x[-4:] == '.txt', all_ab_outputs)

    for each_text_file in only_text_files:
        path_to_each_text_file = "{0}/{1}".format(
            path_to_output, each_text_file)
        with open(path_to_each_text_file, "r") as f:
            output = f.readlines()
        op_in_single_line = "".join(output)

        function_execution_times = re.findall(
            r'(Function executed in )([0-9]+[.][0-9]+)( seconds)', op_in_single_line, flags=re.MULTILINE)
        if len(function_execution_times) != 0:
            for each_function_execution_time_tuple in function_execution_times:
                ex_times += ",{0}".format(
                    each_function_execution_time_tuple[1])
    ex_times += "\n"
    with open("./execcution_times.csv", "a") as f:
        f.write(ex_times)


def main():
    appnames = [
    "dd-cmd", 
    "fast-fourier-transform", 
    "floating-point-operation-cosine", 
    "floating-point-operation-sine",
    "floating-point-operation-sqrt", 
    "image-classification-alexnet-cpu", 
    "image-classification-with-cpu", 
    "image-processing-pillow", 
    "iperf3",
    "matrix-multiplication-high", 
    "matrix-multiplication-medium", 
    "matrix-multiplication-low", 
    "object-classification-yolo-no-gpu",
    "sentiment-analysis", 
    "sorter", 
    "speech-to-text",

    "image-classification-with-cuda",
    "object-classification-yolo-gpu",
    "image-classification-alexnet-gpu"
    ]
    for appname in appnames:
        get_function_execution_times_from_ab_rpi(
            "./cold_warm_start_AB/{0}/RPI/".format(appname), appname)
        get_function_execution_times_from_ab_nano(
            "./cold_warm_start_AB/{0}/NANO/".format(appname), appname)


if __name__ == '__main__':
    main()
