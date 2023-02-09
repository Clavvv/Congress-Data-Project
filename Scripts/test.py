import json



dictionary= {'Things I love': ['Ice cream', 'donuts', 'climbing']}


with open('output.txt', 'w') as f:
    f.write(json.dumps(dictionary))