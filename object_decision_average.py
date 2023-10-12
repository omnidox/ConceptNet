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

def find_object_locations(data):
    object_locations = {}

    for key, paths_list in data.items():
        location, object_ = key.split(':')

        # Extract the main object name from the object string
        object_ = object_.split('/')[0]
        
        # If the object is in our OBJECTS list, process its paths
        if object_ in OBJECTS:
            if object_ not in object_locations:
                object_locations[object_] = []


            # Exclude paths that have any edge labeled 'Synonym'
            paths_list = [path_info for path_info in paths_list if not any(edge[1] == 'Synonym' for edge in path_info[0])]

            # # Exclude paths that have any edge labeled 'RelatedTo' with a weight less than 2
            # paths_list = [path_info for path_info in paths_list if not any(edge[1] == 'RelatedTo' and edge[2] < 2 for edge in path_info[0])]

            # Calculate the average weight for each path
            for i, (path, _) in enumerate(paths_list):  # Ignore the provided path weight
                total_weight = sum(edge[2] for edge in path)
                average_weight = total_weight / len(path)
                paths_list[i] = (path, average_weight)

            for path_info in paths_list:
                path, average_weight = path_info
                degree_of_separation = len(path)
                object_locations[object_].append((path, average_weight, degree_of_separation))


            # Prioritize the paths for each object by degree of separation and then by weight
            object_locations[object_] = sorted(object_locations[object_], key=lambda x: (x[2], -x[1]))[:20]

    return object_locations

# Load the data
with open('paths_modified_4.json', 'r') as file:
    data = json.load(file)

object_locations = find_object_locations(data)

# Write the selected paths to a file

filename = 'object_locations_avg2.txt'

with open(filename, 'w') as outfile:
    for object_, paths in object_locations.items():
        outfile.write(f"\nLocations for {object_}:\n")
        for path_info in paths:
            path, weight, degree_of_separation = path_info
            readable_path_elements = []
            for edge in path:
                if edge[1] in ['IsA', 'AtLocation']:
                    arrow = " <- "
                else:
                    arrow = " -> "
                readable_path_elements.append(f"{edge[0]} ({edge[1]} | Weight: {edge[2]:.2f}){arrow}")
            readable_path = ''.join(readable_path_elements) + object_
            outfile.write(f"{readable_path} | Total Weight: {weight:.2f} | Degree of Separation: {degree_of_separation}\n")

print(f"Generated file '{filename}'")
