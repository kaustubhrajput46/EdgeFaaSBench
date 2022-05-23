# EdgeFaaSBench: Benchmarking Edge Devices Using Serverless Computing

## What is EdgeFaaSBench?

[EdgeFaaSBench](https://github.com/kaustubhrajput46/EdgeFaaSBench) is a novel benchmark tool for edge devices, specifically adopting the idea of the [Function-as-a-Service](https://en.wikipedia.org/wiki/Function_as_a_service) (a.k.a. [serverless computing](https://en.wikipedia.org/wiki/Serverless_computing)) paradigm. EdgeFaaSBench is developed to measure [heterogeneous](https://developer.nvidia.com/embedded/jetson-tx2) and [resource-constrained](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/) [edge](https://en.wikipedia.org/wiki/Edge_computing) devices (often equipped with GPU accelerators) when hosting serverless applications.

EdgeFaaSBench contains 14 different serverless applications performing micro- and application-level benchmarking on edge devices. Micro-benchmark workloads are to measure the performance of a specific resource type on the devices, e.g., CPU, memory, network bandwidth, and disk I/O. Application-level benchmark workloads are developed based on real-world serverless computing use-cases to capture the performances and characteristics of serverless applications on edge devices. In particular, various machine learning and AI FaaS applications, e.g., [image classification](https://en.wikipedia.org/wiki/Computer_vision#Recognition), and [object detection](https://en.wikipedia.org/wiki/Object_detection), are developed for EdgeFaaSBench.

EdgeFaaSBench is developed on top of a widely used open-source FaaS (Function-as-a-Service) framework and container orchestration tool, [OpenFaaS](https://www.openfaas.com/) and [Docker Swarm](https://docs.docker.com/engine/swarm/).

## Publication
* Kaustubh Rajendra Rajput, Chinmay Dilip Kulkarni, Byungjin Cho, Wei Wang, and In Kee Kim, "*EdgeFaaSBench: Benchmarking Edge Devices Using
Serverless Computing*," In 2022 IEEE Internatinoal Conference on Edge Computing (EDGE), Barcelona Spain, July, 2022

## Requirement
* Edge Devices. 
  * [Raspberry PI 4 B](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/), NVidia's Jetson [Nano](https://developer.nvidia.com/embedded/jetson-nano-developer-kit)/[TX2](https://developer.nvidia.com/embedded/jetson-tx2)/[Xavier](https://developer.nvidia.com/embedded/jetson-xavier-nx-devkit)
* [OpenFaaS](https://www.openfaas.com/): Version >= 0.20.5
  * [faas-cli](https://github.com/openfaas/faas-cli) with version >= 0.13.13
* [Docker](https://docs.docker.com/) and [Docker Swarm](https://docs.docker.com/engine/swarm/)
* Python Libraries
  * Python Pillow: https://pillow.readthedocs.io/en/stable/
  * NLTK: https://www.nltk.org/index.html
  * TextBlob: https://textblob.readthedocs.io/en/dev/
  * pyttsx3 2.90: https://pypi.org/project/pyttsx3/
  * SpeechRecognition 3.8.1: https://pypi.org/project/SpeechRecognition/

## Benchmarking Applications
* Micro-Benchmark

| Benchmark Name                    | CPU | MEM | I/O | NET | GPU | Description                                                                                       |
|----------------------------------|-----|-----|-----|-----|-----|---------------------------------------------------------------------------------------------------|
| Matrix Multiplication            | ★★★ | ★★★ | -   | -   | -   | Performing  matrix multiplication of different matrix sizes multiple times                        |
| Fast Fourier Transform           | ★★★ | ★★★ | -   | -   | -   | Reading a random seed number and performing its Fast Fourier Transform operations multiple times  |
| Floating Point Op. (Sine)        | ★★★ | ★★  | -   | -   | -   | Calculating the sine value of all 360 degrees multiple times                                      |
| Floating Point Op. (Sqaure-Root) | ★★★ | ★★  | -   | -   | -   | Calculating the square root value of random numbers, ranging from 10K to 30K multiple times       |
| Sorter                           | ★★  | ★★★ | ★   | -   | -   | Reading a file containing random text data and sorting the text data using the Linux sort command |
| dd                               | ★   | ★   | ★★★ | -   | -   | Performing random read/write operations on storage (micro-SD) on edge devices using the Linux dd command          |
| iPerf3                           | ★   | ★   | -   | ★★★ | -   | Leveraging the iPerf3 tool to measure the achievable bandwidth of the IP network of edge devices  |

* Application-Level Benchmark

| Benchmark Name              | CPU | MEM    | I/O | NET | GPU | Description                                                                                                                                                  |
|----------------------------|-----|--------|-----|-----|-----|--------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Image Processing           | ★★  | ★★     | ★   | ★   | -   | Resizing random images (from benchmark client) to a size of 400x400 pixels                                                                                   |
| Sentiment Analysis         | ★★★ | ★★     | -   | ★   | -   | Downloading JSON files about different topics and calculating the ratio of positive and negative engagements about the topics                                |
| Speech to Text             | ★★  | ★★     | ★   | ★★  | -   | Downloading a random audio file from external storage, generating translated text                                                                            |
| Image Classification (CPU) | ★★★ | ★★     | ★   | ★   | -   | Receiving random images from the benchmark client, performing image classification tasks using pre-training convolutional neural network (CNN) models on CPU |
| Image Classification (GPU) | ★★  | ★★     | ★   | ★   | ★★★ | Reading a file containing random text data and sorting the text data using the Linux sort command                                                            |
| Object Detection (CPU)     | ★★★ | ★★★    | ★   | ★   | -   | Receiving random images from the benchmark client, and performing object detection tasks with YOLOv3 on CPU                                                  |
| Object Detection (GPU)     | ★★  | ★★★    | ★   | ★   | ★★★ | Performing the similar task with Object Detection with CPU, but enabling GPU for faster inference. This workload can run on GPU-equipped edge devices.       |

