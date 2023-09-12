import json

OBJECTS = [
    'apple', 'orange', 'peach', 'strawberry', 'grape', 'pear', 'lemon', 'banana',
    'bottle', 'beer', 'juice', 'wine', 'carrot', 'bell_pepper', 'cucumber', 'broccoli', 
    'asparagus', 'zucchini', 'radish', 'artichoke', 'mushroom', 'potato', 'pretzel', 
    'popcorn', 'muffin', 'cheese', 'cake', 'cookie', 'pastry', 'doughnut', 'pen', 
    'adhesive_tape', 'pencil_case', 'stapler', 'scissors', 'ruler', 'ball', 'balloon', 
    'dice', 'flying_disc', 'teddy_bear', 'platter', 'bowl', 'knife', 'spoon', 'saucer', 
    'chopsticks', 'drinking_straw', 'mug', 'glove', 'belt', 'sock', 'tie', 'watch', 
    'computer_mouse', 'coin', 'calculator', 'box', 'boot', 'towel', 'shorts', 'swimwear',
    'shirt', 'clock', 'hat', 'scarf', 'roller_skates', 'skirt', 'mobile_phone',
    'plastic_bag', 'high_heels', 'handbag', 'clothing', 'oyster', 'tablet_computer', 
    'book', 'flower', 'candle', 'camera', 'remote_control'
]


def prioritize_and_select_paths(data, prioritize_relations=False):
    # If prioritize_relations is True, use the defined relations. Otherwise, use all possible relations.
    prioritized_relations = ['UsedFor', 'AtLocation'] if prioritize_relations else []
    
    selected_paths = {}
    
    for key, paths_list in data.items():
        # Filtering paths based on the presence of prioritized relations, if specified
        if prioritize_relations:
            filtered_paths = [path for path in paths_list if any(edge[1] in prioritized_relations for edge in path[0])]
        else:
            filtered_paths = paths_list
        
        # Sorting the paths first by their length and then by their cumulative weight
        sorted_paths = sorted(filtered_paths, key=lambda x: (len(x[0]), -x[1]))
        
        # Picking the top paths (up to 5 paths)
        if sorted_paths:
            selected_paths[key] = sorted_paths[:5]
    
    return selected_paths

# Load the data
with open('paths_modified_4.json', 'r') as file:
    data = json.load(file)

# Set prioritize_relations to False if you don't want to prioritize. Set to True to prioritize.
selected_paths = prioritize_and_select_paths(data, prioritize_relations=False)

# Write the selected paths to a file
with open('selected_paths.txt', 'w') as outfile:
    for key, paths in selected_paths.items():
        location, object_ = key.split(':')
        outfile.write(f"\nPaths from {location} to {object_}:\n")
        for path in paths:
            readable_path_elements = []
            for edge in path[0]:
                if edge[1] in ['IsA', 'AtLocation']:
                    arrow = " <- "
                else:
                    arrow = " -> "
                readable_path_elements.append(f"{edge[0]} ({edge[1]} | Weight: {edge[2]:.2f}){arrow}")
            readable_path = ''.join(readable_path_elements) + object_
            outfile.write(f"{readable_path} | Total Path Weight: {path[1]:.2f}\n")

# Find objects that were not included
included_objects = set([key.split(':')[1] for key in selected_paths])
not_included = [obj for obj in OBJECTS if obj not in included_objects]
print("Objects not included in the generated file:")
for obj in not_included:
    print(obj)
