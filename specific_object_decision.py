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

def find_specific_object_locations(data, target_object):
    """
    Returns the locations related to the target object.
    """
    if target_object not in OBJECTS:
        return f"{target_object} is not in the OBJECTS list."

    object_locations = {}

    for key, paths_list in data.items():
        location, object_ = key.split(':')

        if object_ == target_object:
            if object_ not in object_locations:
                object_locations[object_] = []

            for path_info in paths_list:
                path, weight = path_info
                degree_of_separation = len(path)
                object_locations[object_].append((path, weight, degree_of_separation))

            # Prioritize the paths for the object by degree of separation and then by weight
            object_locations[object_] = sorted(object_locations[object_], key=lambda x: (x[2], -x[1]))

    return object_locations

# Load the data
with open('paths_modified_3.json', 'r') as file:
    data = json.load(file)

# Specify the target object here
target_object = "high_heels"
object_locations = find_specific_object_locations(data, target_object)

# Write the selected paths to a file
file_name = f"{target_object}_locations.txt"
with open(file_name, 'w') as outfile:
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

print(f"Generated file '{file_name}'")