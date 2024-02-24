from openai import OpenAI
import json
from datetime import date
import sys
import numpy as np
import pandas as pd
sys.path.append('../')
from pt_utils import read_api_key

# code for running mixed gambles task on Llama 2 models. 

# task parameters
min_gain = 0
max_gain = 40
gain_step = 1
min_loss = 0
max_loss = 40
loss_step = 1


# settings
taskname = "mixedgamble"
# taskstring defines the specific version of the task
# this should not include any dashes or underscores
taskstring = '40gain40loss'  


# model parameters
model = "togethercomputer/llama-2-70b-chat"
max_tokens = 1024
temperature = 0

system_prompt = "You are a human subject in a psychology experiment. " 
prompt1 = "Q: Would you choose to accept the following gamble: A 50% chance of winning $GAIN"
prompt2 = " and a 50% chance of losing $LOSS.  Please respond with only the word Yes or No. "
start = "You have $100 in your pocket. "

modelstring = model.split("/")[-1].split('-')[-2]
outfile_stem = f"task-{taskname}_model-{modelstring}_taskstring-{taskstring}"

# set up client, reading API key from file
client = OpenAI(api_key=read_api_key('../TOGETHER_API.key'),
  base_url='https://api.together.xyz',
)

responses = []

for gain in np.arange(min_gain, max_gain + gain_step, gain_step):
    for loss in np.arange(min_loss, max_loss + loss_step, loss_step):
        p1 = prompt1.replace("GAIN", f"${gain}", 1)  # Updating gain
        p2 = prompt2.replace("LOSS", f"${loss}", 1)  # Updating loss
        full_prompt = start + p1 + p2

        chat_completion = client.chat.completions.create(
            messages=[
                {
                "role": "system",
                "content": system_prompt
                },
                {
                "role": "user",
                "content": full_prompt
                }
            ],
            model=model,
            max_tokens=max_tokens,
            temperature=temperature
        )
        print(full_prompt)
        print("gain:", gain, " loss:", loss, chat_completion.choices[0].message.content )
        responses.append({"gain": str(gain), "loss": str(loss), 'response': chat_completion.choices[0].message.content})

# Write responses to a JSON file
# Use a separate key for metadata and responses
output = {'metadata': {'taskname': taskname, 
                       'taskstring': taskstring,
                       'date': str(date.today())}, 
          'responses': responses}
output['metadata']['prompts'] = {
    'prompt1': prompt1,
    'prompt2': prompt2,
    'start': start,
    'system': system_prompt}
output['metadata']['model'] = model
output['metadata']['temperature'] = str(temperature)
output['metadata']['max_tokens'] = str(max_tokens)

# NOTE: moved this outside the loop so that it writes the file only once
with open(f'{outfile_stem}.json', 'w') as json_file:
    json.dump(output, json_file, indent=4)

# write responses to a data frame
df = pd.DataFrame(data['responses'])
df['gain'] = df['gain'].astype(int)
df['loss'] = df['loss'].astype(int)
df['response_int'] = [1 if i.strip().lower().find('yes') == 0 else 0 for i in df['response']]
df.to_csv(f'{outfile_stem}.csv', index=False)