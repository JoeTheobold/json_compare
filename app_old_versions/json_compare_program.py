import json
from difflib import Differ
from pprint import pprint

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def compare_json(json1, json2, path=""):
    differences = []
    
    # If both are dictionaries, compare keys and values
    if isinstance(json1, dict) and isinstance(json2, dict):
        all_keys = set(json1.keys()).union(set(json2.keys()))
        for key in all_keys:
            new_path = f"{path}/{key}" if path else key
            value1 = json1.get(key)
            value2 = json2.get(key)
            if value1 != value2:
                differences.extend(compare_json(value1, value2, new_path))
    
    # If both are lists, compare items
    elif isinstance(json1, list) and isinstance(json2, list):
        for index, (item1, item2) in enumerate(zip(json1, json2)):
            new_path = f"{path}[{index}]"
            if item1 != item2:
                differences.extend(compare_json(item1, item2, new_path))
        if len(json1) != len(json2):
            differences.append((path, json1, json2))
    
    # Otherwise, directly compare values
    else:
        if json1 != json2:
            differences.append((path, json1, json2))
    
    return differences

def display_differences(differences):
    if differences:
        print(f"{'Path':<40} {'JSON1':<40} {'JSON2'}")
        print("="*120)
        for path, json1, json2 in differences:
            print(f"{path:<40} {str(json1):<40} {str(json2)}")
    else:
        print("The JSON files are identical.")

if __name__ == "__main__":
    # Replace 'file1.json' and 'file2.json' with your JSON file paths
    json1 = load_json('nvidia_srv_102.json')
    json2 = load_json('nvidia.json')
    
    differences = compare_json(json1, json2)
    display_differences(differences)
