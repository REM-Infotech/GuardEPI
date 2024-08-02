import json


with open("criargrupo.json", "r") as f:
    file = json.load(f)
    
print(list(file['grupos']))
pass
    