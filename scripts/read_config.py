import json

with open("configs/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

print(config["agent_name"])
print(config["model"])
print(config["tools"])
print(config["memory"]["path"])