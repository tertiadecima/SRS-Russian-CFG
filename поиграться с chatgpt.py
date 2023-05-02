import json
with open("POS_tagging.json", "r", encoding='utf-8-sig') as read_file:
    data = json.load(read_file)

for sent in data:
    for word in sent:
        print(word[0])
        print(word[1])

