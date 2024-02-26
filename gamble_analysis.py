# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: py311
#     language: python
#     name: python3
# ---

import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import sys
import argparse 
import toml
import jinja2
import os
import subprocess
sys.path.append('src')
from prospect_theory import fit_pt_model, get_predicted_output


def get_arguments():
    args = argparse.ArgumentParser()
    args.add_argument('-t', '--targetdir', type=str, required=True)
    return args.parse_args()


def get_gamble_df(targetdir):
    gambles_df = pd.read_csv(f'{targetdir}/{targetdir}.csv')
    del gambles_df['response']
    gambles_df = gambles_df.rename(columns={'response_int': 'response'})
    return gambles_df


def get_respmat(gambles_df):
    respmat = gambles_df.pivot_table(index='gain', columns='loss', values='response')
    return respmat


def plot_respmat(respmat, targetdir):
    plt.imshow(respmat, cmap='jet')
    plt.xlabel('Loss')
    plt.ylabel('Gain')
    plt.colorbar(label='Response')
    plt.savefig(os.path.join(targetdir, 'respmat.png'))
    plt.close()


def plot_mean_gain(gambles_df, targetdir):
    mean_gain = gambles_df.groupby('gain').mean().reset_index()
    mean_gain.plot(x='gain', y='response', kind='line')
    plt.savefig(os.path.join(targetdir, 'mean_gain.png'))
    plt.close()


def plot_mean_loss(gambles_df, targetdir):
    mean_loss = gambles_df.groupby('loss').mean().reset_index()
    mean_loss.plot(x='loss', y='response', kind='line')
    plt.savefig(os.path.join(targetdir, 'mean_loss.png'))
    plt.close()


def get_config(targetdir):
    testname = targetdir.split('_')[0].split('-')[-1]
    assert os.path.exists(os.path.join(targetdir, f'{testname}.config')), f'{testname}.config does not exist'
    with open(os.path.join(targetdir, f'{testname}.config')) as f:
        config = toml.load(f)
    return config


def mk_report(gambles_df, config, targetdir):
    params_est, _ = fit_pt_model(gambles_df, 
                pars0 = (1,1,1),
                bounds=((0, None), (0.1, 2), (0.1, 2)))
    
    pred = get_predicted_output(params_est, gambles_df)
    print(pred)
    environment = jinja2.Environment()
    template = environment.from_string('''
## Estimated prospect theory parameters:

    - loss aversion(lambda): {{  '%.03f' % lam }}
    - curvature (rho): {{  '%.03f' % rho}}
    - inverse temperature (mu): {{ '%.03f' %  mu }}
    - proportion of correctly predicted responses: {{ '%.04f' % pred }}                    
''')
    
    report = template.render(lam=params_est[0], rho=params_est[1], 
                             mu=params_est[2], pred=pred['pred_acc'])


    with open(os.path.join(targetdir, 'report.md'), 'w') as f:
        f.write(f'# Report: {targetdir}\n')
        f.write('## Config\n')
        for k, v in config.items():
            f.write(f'\n### {k}\n\n')
            for k2, v2 in v.items():
                f.write(f'    - {k2}: {v2}\n')

        f.write(report)
        f.write('\n## Response matrix\n')
        f.write('![respmat](respmat.png)\n\n')
        f.write('## Mean gain\n')
        f.write('![mean_gain](mean_gain.png)\n\n')
        f.write('## Mean loss\n')
        f.write('![mean_loss](mean_loss.png)\n\n')
                

# create function to run shell command

def run_command(command, cwd=None):
    process = subprocess.Popen(command, shell=True,
                               cwd=cwd, 
                               stdout=subprocess.PIPE)
    process.wait()
    return process.stdout.read()


if __name__ == "__main__":
        
    args = get_arguments()
    assert os.path.exists(args.targetdir), f'{args.targetdir} does not exist'

    config = get_config(args.targetdir)
    print(config)
    gambles_df = get_gamble_df(args.targetdir)


    respmat = get_respmat(gambles_df)
    plot_respmat(respmat, args.targetdir)
    plot_mean_gain(gambles_df, args.targetdir)
    plot_mean_loss(gambles_df, args.targetdir)
    mk_report(gambles_df, config, args.targetdir)

    run_command('pandoc -s report.md -o report.html', cwd=args.targetdir)