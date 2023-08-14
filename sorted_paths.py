import json

def prioritize_and_select_paths(data):
    prioritized_relations = ['UsedFor', 'AtLocation']
    
    selected_paths = {}
    
    for key, paths_list in data.items():
        # Filtering paths based on the presence of prioritized relations
        filtered_paths = [path for path in paths_list if any(edge[1] in prioritized_relations for edge in path[0])]
        
        # Sorting the paths first by their length and then by their cumulative weight
        sorted_paths = sorted(filtered_paths, key=lambda x: (len(x[0]), -x[1]))
        
        # Picking the top path
        if sorted_paths:
            selected_paths[key] = sorted_paths[0]
    
    return selected_paths

# Load the data from the provided JSON file
with open('paths_modified_3.json', 'r') as file:
    data = json.load(file)

selected_paths = prioritize_and_select_paths(data)

# Print the selected paths
for key, path in selected_paths.items():
    location, object_ = key.split(':')
    readable_path_elements = []
    for edge in path[0]:
        if edge[1] in ['IsA', 'AtLocation']:
            arrow = " <- "
        else:
            arrow = " -> "
        readable_path_elements.append(f"{edge[0]} ({edge[1]} | Weight: {edge[2]:.2f}){arrow}")
    readable_path = ''.join(readable_path_elements) + object_
    print(f"\nPaths from {location} to {object_}:")
    print(f"{readable_path} | Total Path Weight: {path[1]:.2f}")
