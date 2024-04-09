#!/bin/bash

# Set the number of iterations you want
iterations=2

# Loop for the desired number of iterations
count=0
while [ $count -lt $iterations ] # lt stands for less than
do
    # Run your Python script
    python3 run_test_from_params.py -p configfiles/test5.config

    # Increment the counter
    count=$((count+1))

    # Add a delay if needed
    # sleep <seconds>
    # Example: sleep 1 # for 1 second delay
done