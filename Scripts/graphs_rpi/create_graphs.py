#!/usr/bin/env python3

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_ab_graph_from_csv(path_to_ab_csv_file, appName):
    df = pd.read_csv(path_to_ab_csv_file)
    print(df)
    df = df.groupby(axis = 0, by = ['Concurrency'], as_index = False).mean()
    
    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add traces
    fig.add_trace(
        go.Scatter(x = df['Concurrency'], y = df['Total_Time(seconds)'], name="Total_Time(seconds) vs Concurrency"),
        secondary_y=False,
    )
    
    fig.add_trace(
        go.Scatter(x = df['Concurrency'], y = df['Time_for_Each_Group(seconds)'], name="Time_for_Each_Group(seconds) vs Concurrency"),
        secondary_y=True,
    )
    
    # Add figure title
    fig.update_layout(
        height=600, width=600,
        title_text="Jetson nano concurrency graph using apache benchmark for {0}".format(appName)
    )
    
    # Set x-axis title
    fig.update_xaxes(title_text="<b>Concurrency</b>")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>Total Time(Seconds)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Group Time(Seconds)</b>", secondary_y=True)

    # Saving the graph as the pdf file at the below path
    fig.write_image("../concurrency/NANO/{0}/{0}_ap_op_nano.pdf".format(appName))

def create_cpu_mem_graphs_from_csv(path_to_cpu_mem_csv_file, appName):
    col_names = ['Concurrency','Container_ID','Appname','CPU','Mem_used','Total_mem']
    df = pd.read_csv(path_to_cpu_mem_csv_file, names=col_names)

    df = df.groupby(axis = 0, by = ['Concurrency'], as_index = False).mean()
    
    fig = make_subplots(rows=2,cols=1,subplot_titles=("Concurrency vs CPU(%)","Concurrency vs Mem(MiB)"))
    
    fig.add_trace(go.Scatter(x = df['Concurrency'], y = df['CPU'], name="Concurrency vs CPU(%)"),row=1, col=1)

    fig.add_trace(go.Scatter(x = df['Concurrency'], y = df['Mem_used'], name="Concurrency vs Mem(MiB)"),row=2, col=1)

    fig.update_layout(height=600, width=600,
                  title_text="Jetson nano CPU MEM usage graph for {0}".format(appName))

    # Set x-axis title
    fig.update_xaxes(title_text="<b>Concurrency</b>")
    
    # Set y-axes titles
    fig.update_yaxes(title_text="<b>CPU(%)</b>", secondary_y=False)
    fig.update_yaxes(title_text="<b>Memory(MiB)</b>", secondary_y=True)

    fig.write_image("../concurrency/NANO/{0}/{0}_cpu_mem_op_nano.pdf".format(appName))

def main():
    # appanme = "image-classification-alexnet-cpu" #has issues
    # appanme = "image-classification-with-cpu"
    # appanme = "sentiment-analysis"
    appanme = "matrix-multiplication-high"
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
#    appanme = "floating-point-operation-sqrt"

    path1 = "../concurrency/NANO/{0}/ab_output/{0}_ab_readings.csv".format(appanme)
    path2 = "../concurrency/NANO/{0}/cpu_mem_output/{0}_cpu_mem_readings.csv".format(appanme)
    create_ab_graph_from_csv(path1, appanme)
    create_cpu_mem_graphs_from_csv(path2, appanme)
    
if __name__=='__main__':
    main()
