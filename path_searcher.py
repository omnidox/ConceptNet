import json

# Load the data from the paths_modified.json file
with open('paths_modified.json', 'r') as file:
    data = json.load(file)

# Iterate through the data and print paths
for key, paths_list in data.items():
    try:
        location, object_ = key.split(':')
    except ValueError:
        print(f"Error: Expected a single colon in the key '{key}' for splitting.")
        location, object_ = None, None  # Or any default values you'd like to assign

    print(f"\nPaths from {location} to {object_}:")
    
    for path, path_weight in paths_list:
        readable_path = " -> ".join([edge[0] + " (" + edge[1] + ")" for edge in path])
        readable_path += " -> " + object_  # Append the object to the end
        print(f"{readable_path} | Weight: {path_weight:.2f}")
