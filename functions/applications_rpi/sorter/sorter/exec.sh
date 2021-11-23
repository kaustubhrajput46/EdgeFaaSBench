#!/bin/bash

# This command will get the start time of the script
start=$(date +%s.%N)

# Actual function to be executed
cat data.txt | sort

# Calculate the duration of the command executed above by the below command
duration=$(echo "$(date +%s.%N) - $start" | bc)

# print the execution time
execution_time=`printf "%.4f seconds" $duration`

echo "The function has executed succesfully in $execution_time"