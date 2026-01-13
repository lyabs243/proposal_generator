# generate a metadata key (remove also all special characters)
def generate_key(name: str) -> str:
    import re

    # Convert to lowercase
    key = name.lower()
    # Replace spaces with underscores
    key = key.replace(" ", "_")
    # Remove special characters
    key = re.sub(r'\W+', '', key)
    return key


# get all unique technologies from data.json
def get_all_technologies(data_json_path: str = "data/data.json") -> str:
    import json
    import os

    technologies = set()

    # should get the path from the root
    path = os.path.join(os.path.dirname(__file__), data_json_path)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for item in data:
        if "metadata" in item and "technologies" in item["metadata"]:
            techs = item["metadata"]["technologies"]
            if isinstance(techs, list):
                technologies.update(techs)

    return ", ".join(sorted(list(technologies)))

