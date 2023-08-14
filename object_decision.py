import json

OBJECTS = [
    # ... [as provided above]
]

def find_object_locations(data):
    object_locations = {}

    for key, paths_list in data.items():
        location, object_ = key.split(':')
        
        # If the object is in our OBJECTS list, process its paths
        if object_ in OBJECTS:
            if object_ not in object_locations:
                object_locations[object_] = []

            for path_info in paths_list:
                path, weight = path_info
                degree_of_separation = len(path)
                object_locations[object_].append((path, weight, degree_of_separation))

            # Prioritize the paths for each object by degree of separation and then by weight
            object_locations[object_] = sorted(object_locations[object_], key=lambda x: (x[2], -x[1]))[:5]

    return object_locations

# Load the data
with open('paths_modified_3.json', 'r') as file:
    data = json.load(file)

object_locations = find_object_locations(data)

# Write the selected paths to a file
with open('object_locations.txt', 'w') as outfile:
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

print("Generated file 'object_locations.txt'")
