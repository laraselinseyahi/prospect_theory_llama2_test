import pandas as pd
import numpy as np
import os
from pathlib import Path
import secrets
import hashlib
import glob
import matplotlib.pyplot as plt


def plot_respmat(respmat, targetdir, i, type):

    output_path = os.path.join(current_path, "plots") 
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    plt.imshow(respmat, cmap='jet')
    plt.xlabel('Loss')
    plt.ylabel('Gain')
    plt.colorbar(label='Response')
    respmat.to_csv(os.path.join(output_path, type + f'_respmat_test{i}.csv'), index=False) #added
    plt.savefig(os.path.join(output_path, type + f'_respmat_test{i}.png'))
    plt.close() 

def mean_SD(current_path):
    print(current_path)


    for i in range(1,6):
        test_dir = Path(f'outputs/test{i}/')
        folder_path = os.path.join(current_path, test_dir) 
        print(folder_path)
        # file_path = os.path.join(folder_path, 'respmat.csv')

        # Get all directories within the directory
        subdirectories = glob.glob(os.path.join(folder_path, '*/'))

        dfs_list = []
        # Loop over each subdirectory
        for subdir in subdirectories:
            # Get all CSV files within the subdirectory
            csv_file = glob.glob(os.path.join(subdir, 'respmat.csv'))
            dfs_list.append(csv_file)
        print(len(dfs_list))
        stacked_arrays = np.stack([pd.read_csv(df[0]).values for df in dfs_list], axis=2)

        # Calculate the mean along the third axis
        mean_data = np.mean(stacked_arrays, axis=2)

        # Calculate the standard deviation along the third axis
        std_data = np.std(stacked_arrays, axis=2)

        mean_df = pd.DataFrame(mean_data)
        sd_df = pd.DataFrame(std_data)
        # mean_df.to_csv(os.path.join(current_path, f'mean_test{i}.csv'), index=False)
        # sd_df.to_csv(os.path.join(current_path, f'SD_test{i}.csv'), index=False) 
        plot_respmat(mean_df, current_path, i, 'mean')
        plot_respmat(sd_df, current_path, i, 'sd')

        






if __name__ == "__main__":
        
    current_path = os.getcwd()
    mean_SD(current_path)
