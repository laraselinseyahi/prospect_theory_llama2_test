# run a test using params from a file
from openai import OpenAI
import json
from datetime import date
import sys
import numpy as np
import pandas as pd
sys.path.append('src')
from pt_utils import read_api_key
import argparse
import toml
import os
import shutil
import random
import string


def generate_random_ascii_hash(length=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def get_args():
    parser = argparse.ArgumentParser(description='Run a test using params from a file')
    parser
    parser.add_argument('-p', '--param_file',  type=str, help='File containing parameters for the test', required=True)
    parser.add_argument('-k', '--keyfile',  type=str, help='api key file', default='TOGETHER_API.key')
    parser.add_argument('-o', '--overwrite', action='store_true', help='overwrite output directory if it exists')
    parser.add_argument('--outdir', default='outputs', help='output directory') 
    parser.add_argument('--hash', action='store_true', help='append a random hash to the name')
    print(parser)
    args = parser.parse_args()
    return args


def get_responses(params):
    responses = []

    for gain in np.arange(params['task']['min_gain'], params['task']['max_gain'] + params['task']['gain_step'], params['task']['gain_step']):
        for loss in np.arange(params['task']['min_loss'], params['task']['max_loss'] + params['task']['loss_step'], params['task']['loss_step']):
            p1 = params['prompts']['prompt1'].replace("GAIN", f"{gain}", 1)  # Updating gain
            p2 = params['prompts']['prompt2'].replace("LOSS", f"{loss}", 1)  # Updating loss
            full_prompt = params['prompts']['start'] + p1 + p2

            chat_completion = client.chat.completions.create(
                messages=[
                    {
                    "role": "system",
                    "content": params['prompts']['system_prompt']
                    },
                    {
                    "role": "user",
                    "content": full_prompt
                    }
                ],
                model=params['model']['model'],
                max_tokens=params['model']['max_tokens'],
                temperature=params['model']['temperature']
            )
            print(full_prompt)
            print("gain:", gain, " loss:", loss, chat_completion.choices[0].message.content )
            responses.append({"prompt": full_prompt, 
                            "gain": str(gain), 
                            "loss": str(loss), 
                            'response': chat_completion.choices[0].message.content})
    return responses


def create_output_dict(params, responses):
    output = {'metadata': {'taskname': params['task']['taskname'], 
                        'taskstring': params['task']['taskstring'],
                        'date': str(date.today())}, 
            'responses': responses}
    output['metadata']['prompts'] = {
        'prompt1': params['prompts']['prompt1'],
        'prompt2': params['prompts']['prompt2'],
        'start': params['prompts']['start'],
        'system': params['prompts']['system_prompt']}
    output['metadata']['model'] = params['model']['model']
    output['metadata']['temperature'] = str(params['model']['temperature'])
    output['metadata']['max_tokens'] = str(params['model']['max_tokens'])
    return output


def save_results_to_json(params, output):
    with open(os.path.join(params['outfile_stem'], f"{params['outfile_stem'].split('/')[-1]}.json"), 'w') as json_file:
        json.dump(output, json_file, indent=4)


def save_results_to_df(params, output):
    # write responses to a data frame
    df = pd.DataFrame(output['responses'])
    df['gain'] = df['gain'].astype(int)
    df['loss'] = df['loss'].astype(int)
    df['response_int'] = [1 if i.strip().lower().find('yes') > -1 else 0 for i in df['response']]
    df.to_csv(os.path.join(params['outfile_stem'], f"{params['outfile_stem'].split('/')[-1]}.csv"), index=False)

    # call the pre-processing function clean response i , is that == yes clean_response

if __name__ == '__main__':
    args = get_args()
    with open(args.param_file, 'r') as f:
        params = toml.load(f)
        configname = args.param_file.split("/")[-1].split(".")[0]

    params['model']['modelstring'] = params['model']['model'].split("/")[-1].split('-')[-2]
    if args.hash is not None:
        hashstring = f'_hash-{generate_random_ascii_hash()}'
    else:
        hashstring = ''

    # Construct outfile_stem with an additional layer of directory
    outfile_dir = os.path.join(args.outdir, configname)

    # Check if outfile_dir exists, if not, create it
    if not os.path.exists(outfile_dir):
        os.makedirs(outfile_dir)

    params['outfile_stem'] = os.path.join(
        #args.outdir, 
        outfile_dir, 
        f"test-{configname}_task-{params['task']['taskname']}_model-{params['model']['modelstring']}_taskstring-{params['task']['taskstring']}{hashstring}")

    # Check if params['outfile_stem'] exists, if overwrite is enabled, remove it, else raise error
    if os.path.exists(params['outfile_stem']):
        if args.overwrite:
            shutil.rmtree(params['outfile_stem'])
        else:
            raise FileExistsError(f'Output directory {params["outfile_stem"]} already exists - use -o to overwrite or move it out of the way first')
    
    # create the output directory 
    os.makedirs(params['outfile_stem'])
    shutil.copy(args.param_file, params['outfile_stem'])

    print(hashstring)

    # set up client, reading API key from file
    if not os.path.exists(args.keyfile):
        raise FileNotFoundError(f'API key file {args.keyfile} does not exist')
    client = OpenAI(api_key=read_api_key(args.keyfile),
        base_url='https://api.together.xyz',
    )

    responses = get_responses(params)

    output = create_output_dict(params, responses)

    save_results_to_json(params, output)

    save_results_to_df(params, output)
    # NOTE: moved this outside the loop so that it writes the file only once


