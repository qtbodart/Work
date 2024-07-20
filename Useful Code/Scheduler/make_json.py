import json

with open("settings.json", "r") as file:
    data = json.load(file)

output = {}
output["min_work_duration"] = 30
output["max_work_duration"] = 120
output["min_rest_duration"] = 30
output["max_rest_duration"] = 60
output["work_probability"] = 0.2
output["rest_probability"] = 0.3
output["chunk"] = 10
output["begin_with"] = "work"
output["debug"] = True
with open("settings.json", 'w') as file:
    data = json.dumps(output, indent=4)
    print(data)
    file.write(data)