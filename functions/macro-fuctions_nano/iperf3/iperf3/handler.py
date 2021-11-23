import subprocess
import time as t
import os, signal

def handle(req):
    functionStartTime = t.time()
    
    try:
    # Initialzing server
        command = 'iperf3 -s -D'
        subprocess.check_output(command, shell=True).decode('UTF-8')
        print("---------------------------------------------------------------------------------------------------------------------------\n")
        print("Server started in the background. Awaiting for packeges...\n")

        iCommand = 'iperf3 -c 127.0.0.1 > msg.txt'
        startTime = t.time()
        output = subprocess.check_output(iCommand, shell=True).decode('UTF-8')
        endTime = t.time()
        print("Packeges from the client has been sent to the server.\n")

        with open("msg.txt", "r") as readOutput:
            lines = readOutput.readlines()[-4:]
            # To get the client's statistics
            statSender = lines[0].strip().split()
            # To get the server's statistics
            statReceiver = lines[1].strip().split()
            # Printing the statistics of the Client, who sent the packets
            print("Here are the statistics of %s:" % statSender[9])
            print("1. Data Transferred:", (str(statSender[4]) + " " + str(statSender[5])))
            print("2. Bitrate:", (str(statSender[6]) + " " +str(statSender[7])))
            print("---------------------------------------------------------------------------------------------------------------------------\n")
            # Printing the statistics of the Server, who sent the received the packets
            print("Here are the statistics of %s:" % statReceiver[8])
            print("1. Data Received:", (str(statReceiver[4]) + " " + str(statReceiver[5])))
            print("2. Bitrate:", (str(statReceiver[6]) + " " + str(statReceiver[7])))
            print("---------------------------------------------------------------------------------------------------------------------------\n")

            # This code will end the process of server which is running in the background
            print("Obtaining information to kill the server running in the background...\n")
            # To get the PId of the server running in the background
            processInfo = os.popen('ps ax | grep \'iperf3 -s -D\' | grep -v grep')
            for line in processInfo:
                fields = line.split()
                # Confirming whether the output of this is referring to correct process or not
                verifyName = fields[-3:]
                processName = verifyName[0] + " " + verifyName[1] + " " + verifyName[2]
                if processName == "iperf3 -s -D":
                    print("Information collection for \'iperf3 -s -D\' complete. PId for this process is %s" % fields[0])
                    pid = fields[0]
                    # terminate the process
                    os.kill(int(pid), signal.SIGKILL)
                    print("\nProess \"iperf3 -s -D\" has been successfully terminated.\n")
                    print("---------------------------------------------------------------------------------------------------------------------------\n")
                else:
                    print("Obatained process name %s does not match with the required process name \'iperf3 -s -D\'.\n" % processName)
                    print("Maybe This process has been already terminated.\n")
                    print("---------------------------------------------------------------------------------------------------------------------------\n")

            functionEndTime = t.time()
            print("iperf3 command executed in %s seconds.\n"% str(endTime-startTime))
            print("Entire function executed in %s seconds.\n"% str(functionEndTime-functionStartTime))
            print("---------------------------------------------------------------------------------------------------------------------------\n")
    except Exception as e:
        print("Following exception has occured:",e)
        print("\nExiting the program.\n")
        exit(0)
    return "Function to measure network performance has been executed successfully.\n"
