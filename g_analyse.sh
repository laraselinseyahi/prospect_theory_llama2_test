#!/bin/bash

# Set the folder path
# folder_path=$(pwd)

# Loop over test directories
for i in {1..5}; do
    directory="outputs/test$i"
    # Use glob to find subdirectories within each test directory
    # folders=$(find "$folder_path/$directory" -mindepth 1 -maxdepth 1 -type d)
    folders=$(find "$directory" -mindepth 1 -maxdepth 1 -type d)
    # Loop over subdirectories
    for folder in $folders; do
        echo folder
        echo "Executing gamble_analysis.py in directory: $folder"
        # Run gamble_analysis.py script in each subdirectory
        python3 gamble_analysis.py -t "$folder"
    done
done
