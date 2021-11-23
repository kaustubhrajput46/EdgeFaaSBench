#!/bin/sh

#Architecture
#1. provide appname, no of executions, dockerhub username  while executing script
#2. setup data file to reduce logs on console
#3. Set -m sto enable job bg fg commands in the script
#4. Kill previous job if present.
#5. Get container id of provided appname
#6. Create Command to be execute the given app
#7. Create for loop based on no of executions provided
	#8. Create log csv and stat csv based on execution value.
	#9. start the docker stats command for based on the container id and store in stat csv
	#10.Start the execution of application 
	#11. Sleep for 1 minute to cool the device down.
#12.Send the files to laptop	

#Note --- bypass sudo pwd using --- echo @123 | sudo -S <command>

# Sample execution command
# Note - device_name is case sensitive Values = 'NANO' or 'RPI'
# --> sudo sh ml_batch_gpu_cpu_script.sh <appname> <no_of_exec> <device_name> 

#Fetch the application name
APPLICATION_NAME="$1"
EXECUTIONS="$2"
DEVICE_NAME="$3"

DOCKER_HUB_USERNAME=""
echo $DOCKER_HUB_USERNAME
# Get the dockerhub username based on device
if [ "$DEVICE_NAME" = "NANO" ]; then
	DOCKER_HUB_USERNAME="kaustubhrajput"
  else if [ "$DEVICE_NAME" = "RPI" ]; then
          DOCKER_HUB_USERNAME="cd21"
  fi
fi

echo $DOCKER_HUB_USERNAME

# setup data file to reduce logs on the console.
touch data.txt

# Set -m to enable job bg fg commands in the script
set -m

# Kill previous job if present.
kill %1 >> data.txt
kill %2 >> data.txt

# Get container id of provided appname
GET_CONTAINER_ID=$(echo '@123' | sudo -S docker ps -f ancestor=$DOCKER_HUB_USERNAME/$APPLICATION_NAME:latest --format {{.ID}})
echo "container id below"
echo $GET_CONTAINER_ID >> data.txt
echo $GET_CONTAINER_ID #remove

# Execute application based on no of executions provided
a=0
while [ $a -lt $EXECUTIONS ]
do
   # Shell logs to be stored in below path
   SHELL_LOG_FILE="../logs/${APPLICATION_NAME}/${DEVICE_NAME}/console_${APPLICATION_NAME}_logs_${a}.csv"
   echo $SHELL_LOG_FILE #remove
   # Stats logs to be stroed in below path
   STATS_LOG_FILE="../logs/${APPLICATION_NAME}/${DEVICE_NAME}/stats_${APPLICATION_NAME}_logs_${a}.csv"
   echo $STATS_LOG_FILE #remove
   # Docker stats command to be executed to get system logs
   STAT_COMMAND="echo '@123' | sudo -S docker stats $GET_CONTAINER_ID --format 'ok, {{.ID}}, {{.Name}}, {{.CPUPerc}}, {{.MemUsage}}, {{.MemPerc}}, {{.NetIO}}, {{.BlockIO}}, {{.PIDs}}' >> $STATS_LOG_FILE"
   echo $STAT_COMMAND #remove
   # To run Docker stats in the backgrond so that we can execute applications in the foreground
   STAT_COMMAND_DETACHED="$STAT_COMMAND &"
   echo $STAT_COMMAND_DETACHED #remove
   echo $STAT_COMMAND_DETACHED >> data.txt
   eval $STAT_COMMAND_DETACHED >> data.txt
   jobs >> data.txt
   sleep 1

   # Command to invoke and execute applications
   SHELL_COMMAND="echo | faas-cli invoke $APPLICATION_NAME >> $SHELL_LOG_FILE"
   echo $SHELL_COMMAND #remove
   eval $SHELL_COMMAND

   sleep 1

   # Kill the Docker stats command as we finished our application execution
   kill %1 >> data.txt
   kill %2 >> data.txt

   #increment iterator by 1
   a=`expr $a + 1`

   # Sleep for some time to let the device rest 
   sleep 45
done

