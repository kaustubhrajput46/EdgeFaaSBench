#!/bin/sh

# Fetch all the arguments in appropriate variable names
EDGE_LOGIN_PASSWORD="$1"
EDGE_LOGIN_NAME="$2"
EDGE_HOST_IP="$3"
SCRIPT="$4"
APPLICATION_NAME="$5"
DOCKER_HUB_USERNAME="$6"
SET_NUMBER="$7"
APACHE_BENCH="$8"
SCRIPT_PATH="$9"

# setup data file to reduce logs on the console.
touch data.txt

# Set -m sto enable job bg fg commands in the script
set -m 

# Kill previous job if present.
kill %1 >> data.txt

# Command to be executed on edge device
SCRIPT_EXECUTION_ON_DEVICE="cd $SCRIPT_PATH && sh $SCRIPT $APPLICATION_NAME $DOCKER_HUB_USERNAME $SET_NUMBER $SCRIPT_PATH"

# setting up ssh command to execute edge device script
EDGE_COMMAND="echo $EDGE_LOGIN_PASSWORD | sshpass -p $EDGE_LOGIN_PASSWORD ssh -tt ${EDGE_LOGIN_NAME}@${EDGE_HOST_IP} '$SCRIPT_EXECUTION_ON_DEVICE'"
#echo $EDGE_COMMAND

# Running the command in detached mode so that we can execute apache bench command next.
EDGE_COMMAND_DETACHED="$EDGE_COMMAND &"
echo $EDGE_COMMAND_DETACHED >> data.txt
eval $EDGE_COMMAND_DETACHED >> data.txt

# Print any job running in background.
jobs >> data.txt
sleep 1

# Run the apache bench command.
date >> cold_warm_start_AB/${APPLICATION_NAME}/NANO/ab_cws_${APPLICATION_NAME}_nano_logs_${SET_NUMBER}.txt
echo '***********************' >> cold_warm_start_AB/${APPLICATION_NAME}/NANO/ab_cws_${APPLICATION_NAME}_nano_logs_${SET_NUMBER}.txt
$APACHE_BENCH >> cold_warm_start_AB/${APPLICATION_NAME}/NANO/ab_cws_${APPLICATION_NAME}_nano_logs_${SET_NUMBER}.txt
echo '***********************' >> cold_warm_start_AB/${APPLICATION_NAME}/NANO/ab_cws_${APPLICATION_NAME}_nano_logs_${SET_NUMBER}.txt

# Sleep for one second before killing the docker stats command on Jetson nano.
sleep 1
# Kill jobs running in background if any
kill %1 >> data.txt

#sleep 1 sec before transferring .csv file to laptop
sleep 1
echo "Refer cold_warm_start_AB/${APPLICATION_NAME}/NANO/ab_cws_${APPLICATION_NAME}_nano_logs_${SET_NUMBER}.txt output."

# Transferring log files from edge device to laptop
DIR_COLD_WARM_STATS="/home/${EDGE_LOGIN_NAME}/faas/functions/cold_warm_start/${APPLICATION_NAME}/NANO/${APPLICATION_NAME}_nano_logs_${SET_NUMBER}.csv"
PATH_FOR_SAVING_CSV="cold_warm_start_AB/${APPLICATION_NAME}/NANO"
TRANSFER="echo $EDGE_LOGIN_PASSWORD | sshpass -p $EDGE_LOGIN_PASSWORD scp ${EDGE_LOGIN_NAME}@${EDGE_HOST_IP}:${DIR_COLD_WARM_STATS} ${PATH_FOR_SAVING_CSV}"
eval $TRANSFER
echo $TRANSFER >> data.txt


