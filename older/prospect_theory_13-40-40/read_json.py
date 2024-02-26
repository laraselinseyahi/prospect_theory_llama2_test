import json

# Open the JSON file
with open('prospect_theory_13b_40-40.json', 'r') as f:
    # Load the JSON data
    data = json.load(f)

# Now you can parse through the data
# For example, if the JSON contains a list of dictionaries:
    
res = []
for item in data[1:]:
    parts = item.split()
    cut = parts[:4]
    gain = cut[0]
    num = gain.split(':')
        # print(num)
        # print(num)
    g = num[1]
    print(g)
    print(cut)
    tuple = g, cut[2], cut[3]
    print(tuple)
    res.append(tuple)
    
with open('13b-40-40-prospect_theory.json', 'w') as json_file:
    json.dump(res, json_file, indent=4)


    # print(cut)
print(res)

# Or if it contains key-value pairs:

