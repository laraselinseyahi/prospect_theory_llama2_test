from openai import OpenAI
import json
from datetime import date

# code for running prospect theory test on Llama 2 models. 

TOGETHER_API_KEY = "a57513d951516c03a3b6638b9f52b805414f05211e40d06115371650aae631e6"

client = OpenAI(api_key=TOGETHER_API_KEY,
  base_url='https://api.together.xyz',
)


responses = []
responses.append("13b Prospect Theory test 40-40 gains and losses " + str(date.today()))


prompt1 = "Q: Would you choose to accept the following gamble: A 50% chance of winning $0"
prompt2 = " and a 50% chance of losing $0.  Please respond with Yes or No."
start = "You have $100 in your pocket."
prev_gain = 0
prev_loss = 0

for gain in range(0, 41):
    for loss in range(0, 41):
        prompt1 = prompt1.replace(f"${prev_gain}", f"${gain}", 1)  # Updating gain
        prompt2 = prompt2.replace(f"${prev_loss}", f"${loss}", 1)  # Updating loss
        full_prompt = start + prompt1 + prompt2

        chat_completion = client.chat.completions.create(
        messages=[
            {
            "role": "system",
            "content": "You are a human subject in a psychology experiment." 
            },
            {
            "role": "user",
            "content": full_prompt
            }
        ],
        model="togethercomputer/llama-2-13b-chat",
        max_tokens=1024,
        temperature=0
        )
        prev_gain = gain
        prev_loss = loss
        print(full_prompt)
        print("gain:", gain, " loss:", loss, chat_completion.choices[0].message.content )
        responses.append("gain:" + str(gain) + " loss: " + str(loss) + chat_completion.choices[0].message.content )

#Write responses to a JSON file
        with open('prospect_theory_13b_40-40.json', 'w') as json_file:
            json.dump(responses, json_file, indent=4)

