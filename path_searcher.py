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
    
for key, paths_list in data.items():
    try:
        location, object_ = key.split(':')
    except ValueError:
        print(f"Error: Expected a single colon in the key '{key}' for splitting.")
        location, object_ = None, None  # Or any default values you'd like to assign

    print(f"\nPaths from {location} to {object_}:")
    
    for path, path_weight in paths_list:
        readable_path_elements = []
        for edge in path:
            if edge[1] in ['IsA', 'AtLocation']:
                arrow = " <- "
            else:
                arrow = " -> "
            
            readable_path_elements.append(f"{edge[0]} ({edge[1]} | Weight: {edge[2]:.2f}){arrow}")

        readable_path = ''.join(readable_path_elements) + object_
        print(f"{readable_path} | Total Path Weight: {path_weight:.2f}")