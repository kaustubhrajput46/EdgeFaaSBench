import subprocess
import time as t

def handle(req):
    startTime = t.time()
    # Initialzing Input file, Output file, block-size, count, oflag to test the write performance
    inputFile = '/dev/zero'
    outputFile = 'output.txt'
    blockSize = '1024k'
    count='500'
    oflag = 'dsync'

    ddCommand = 'dd if=' + inputFile + ' of=' + outputFile + ' bs=' + blockSize + ' count=' + count + ' oflag=' + oflag + " 2>write.txt"
    
    try:
        print("Executing this command:%s" % ddCommand)
        subprocess.check_output(ddCommand, shell=True).decode('UTF-8') 
    except Exception as e:
        print("dd command to test the write performance failed! This is the error:",e)
        print("This is the command program has entered:", ddCommand)
        print("Exiting the program.")
        exit(0)
    
    # reading from the write.output file to get the write speed and the time required to write those records.
    try:
        with open("write.txt", "r") as readOutput:
            for _ in range(2):
                next(readOutput)
            for line in readOutput:
                lineList = line.split(",")
                print("Time Taken to write the output:%s" % lineList[2])
                print("Throughput:%s" % lineList[3])
    except Exception as e:
        print("Following exception has occured ",e)
        print("Exiting the program.")
        exit(0)


    # Initializing the variables for testing out the read performance, read from the same file which has been created above,i.e., read.txt
    inFile = 'output.txt'
    opFile = '/dev/null'
    bs = '1024k'
    count = '10'

    ddCommand1 = 'dd if=' + inFile + ' of=' + opFile + ' bs=' + bs + ' count=' + count + " 2>read.txt"

    try:
        print("Executing this command:%s" % ddCommand1)
        subprocess.check_output(ddCommand1, shell=True).decode('UTF-8')
    except Exception as e:
        print("dd command to test read performance failed! This is the error:", e)
        print("This is the command program has entered:", ddCommand1)
        print("Exiting the program.")
        exit(0)
    
    # reading from the read.output file to get the write speed and the time required to write those records.
    try:
        with open("read.txt", "r") as readOutput:
            for _ in range(2):
                next(readOutput)
            for line in readOutput:
                lineList = line.split(",")
                print("Time Taken to read the output:%s" % lineList[2])
                print("Throughput:%s" % lineList[3])
    except Exception as e:
        print("Following exception has occured ",e)
        print("Exiting the program.")
        exit(0)

    endTime = t.time()

    return "The function has executed successfully in {:.2f} seconds.".format(endTime-startTime)