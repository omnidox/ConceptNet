import json


OBJECTS = ['apple', 'orange', 'peach', 'strawberry', 'grape', 'pear', 'lemon', 'banana',
'bottle', 'beer', 'juice', 'wine',
'carrot', 'bell_pepper', 'cucumber', 'broccoli', 'asparagus', 'zucchini', 'radish', 'artichoke', 'mushroom', 'potato',
'pretzel', 'popcorn', 'muffin', 'cheese', 'cake', 'cookie', 'pastry', 'doughnut',
'pen', 'adhesive_tape', 'pencil_case', 'stapler', 'scissors', 'ruler',
'ball', 'balloon', 'dice', 'flying_disc', 'teddy_bear',
'platter', 'bowl', 'knife', 'spoon', 'saucer', 'chopsticks', 'drinking_straw', 'mug',
'glove', 'belt', 'sock', 'tie', 'watch', 'computer_mouse', 'coin', 'calculator', 'box', 'boot', 'towel', 'shorts', 'swimwear',
'shirt', 'clock', 'hat', 'scarf', 'roller_skates', 'skirt', 'mobile_phone',
'plastic_bag', 'high_heels', 'handbag', 'clothing', 'oyster', 'tablet_computer', 'book', 'flower', 'candle', 'camera', 'remote_control',
'mask', 'toy', 'face_mask', 'sunglasses', 'sun_glasses', 'spectacles', 'candy', 'pumpkin', 'spider', 'cat', 'bell', 'toothbrush',
'tooth_brush', 'toothpaste', 'tooth_paste', 'top', 'receipt', 'dreidel', 'medicine', 'bow_tie', 'neck_tie', 'bowtie', 'necktie', 
'eyeglasses_case', 'eyeglasses', 'aerosol', 'aerosol_can','dental_floss','cigar', 'stuffed_animal', 'stuffed_toy', 'stuffed_toy_animal',
'chocolate', 'wand', 'block', 'chocolate_bar']


# New function to set robot focus
def set_robot_focus(path_info, focus_contexts, degree_reduction=1, weight_multiplier=1.5):
    path, average_weight, degree_of_separation = path_info
    for edge in path:
        if edge[0] in focus_contexts:
            degree_of_separation -= degree_reduction
            average_weight *= weight_multiplier
            break
    return (path, average_weight, degree_of_separation)


def find_object_locations(data, focus_contexts=[]):
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
                
                # Adjust the path info based on the robot's focus
                adjusted_path_info = set_robot_focus((path, average_weight, degree_of_separation), focus_contexts)
                object_locations[object_].append(adjusted_path_info)


            # Prioritize the paths for each object by degree of separation and then by weight
            object_locations[object_] = sorted(object_locations[object_], key=lambda x: (x[2], -x[1]))[:20]

    return object_locations

# Load the data
with open('paths_modified_6.json', 'r') as file:
    data = json.load(file)

# Set the robot's focus
robot_focus = []
object_locations = find_object_locations(data, focus_contexts=robot_focus)

# Write the selected paths to a file

filename = 'object_locations_tasked2.txt'

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
