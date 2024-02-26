from openai import OpenAI
import json
from datetime import date

# code for running prospect theory test on Llama 2 models. 

TOGETHER_API_KEY = "a57513d951516c03a3b6638b9f52b805414f05211e40d06115371650aae631e6"

client = OpenAI(api_key=TOGETHER_API_KEY,
  base_url='https://api.together.xyz',
)


responses = []
responses.append("7b Prospect Theory test 40-40 gains and losses " + str(date.today()))


prompt1 = "Q: Would you choose to accept the following gamble: A 50% chance of winning $"
prompt2 = " and a 50% chance of losing $"
# prompt3 = "Please respond with Yes or No."
prompt3 = ". Please indicate 1 if you accept or 0 if you don't accept (please indicate just the number in your reponse, single digit)."
start = "You have $100 in your pocket."

for gain in range(0, 41):
    for loss in range(0, 41):
        full_prompt = start + prompt1 + str(gain) + prompt2 + str(loss) + prompt3

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
        model="togethercomputer/llama-2-7b-chat",
        max_tokens=1024,
        temperature=0
        )
        print(full_prompt)
        print("gain:", gain, " loss:", loss, chat_completion.choices[0].message.content )
        responses.append("gain:" + str(gain) + " loss:" + str(loss) + chat_completion.choices[0].message.content )

#Write responses to a JSON file
        with open('prospect_theory_7b_40-40.json', 'w') as json_file:
            json.dump(responses, json_file, indent=4)

