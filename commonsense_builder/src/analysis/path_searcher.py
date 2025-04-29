import sys
import json 

# Check if the user provided the required argument
if len(sys.argv) < 2:
    print("Usage: python script_name.py <path_to_json_file>")
    sys.exit(1)

# Use the provided JSON file path
json_file_path = sys.argv[1]

# Load the data from the specified JSON file
with open(json_file_path, 'r') as file:
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
        readable_path_elements = []
        for edge in path:
            if edge[1] in ['IsA', 'AtLocation']:
                arrow = " <- "
            else:
                arrow = " -> "
            
            readable_path_elements.append(f"{edge[0]} ({edge[1]} | Weight: {edge[2]:.2f}){arrow}")

        readable_path = ''.join(readable_path_elements) + object_
        print(f"{readable_path} | Total Path Weight: {path_weight:.2f}")

# Outputting the command example
command_example = f"python {sys.argv[0]} paths_modified.json2"  # Using the script's name for demonstration
command_example
