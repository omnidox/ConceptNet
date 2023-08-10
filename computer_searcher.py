import json

# Modifying the provided code to only print paths that contain the node "computer" and its maximum degree of separation

# Load the data from the paths_modified.json file
# (Note: This step is commented out since I can't access the paths_modified.json file in this environment)

with open('paths_modified.json', 'r') as file:
    data = json.load(file)

# Function to determine the maximum degree of separation for paths with "computer"
def find_max_degree_for_computer(data):
    max_degree = 0
    for key, paths_list in data.items():
        for path, _ in paths_list:
            for edge in path:
                if edge[0] == "computer":
                    max_degree = max(max_degree, len(path))
                    break
    return max_degree

# Use the function to get the maximum degree for "computer"
max_degree_computer = find_max_degree_for_computer(data)

# Iterate through the data and print paths that contain "computer" and have its maximum degree of separation
for key, paths_list in data.items():
    parts = key.split('_')
    location, object_ = '_'.join(parts[:-1]), parts[-1]

    
    # Check if any of the paths for this object contains "computer" and has the max degree
    paths_with_computer = [(path, path_weight) for path, path_weight in paths_list if any(edge[0] == "computer" for edge in path) and len(path) == max_degree_computer]
    
    if paths_with_computer:
        print(f"\nPaths from {location} to {object_} containing 'computer' with maximum degree of {max_degree_computer}:")
        for path, path_weight in paths_with_computer:
            readable_path = " -> ".join([edge[0] + " (" + edge[1] + ")" for edge in path])
            readable_path += " -> " + object_  # Append the object to the end
            print(f"{readable_path} | Weight: {path_weight:.2f}")
