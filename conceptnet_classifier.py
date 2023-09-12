import json

def get_object_context(data, object_name):
    """
    Given the data and an object name, return its most relevant context along with the path, weight, and degree of separation.
    """
    # If the object isn't present in the data, return a message indicating that
    if object_name not in [key.split(':')[1] for key in data]:
        return f"No paths found for {object_name}"
    
    # Gather paths relevant to the object
    relevant_paths = []
    for key, paths_list in data.items():
        _, obj = key.split(':')
        if obj == object_name:
            relevant_paths.extend(paths_list)

    # Sort the paths by degree of separation and then by weight
    sorted_paths = sorted(relevant_paths, key=lambda x: (len(x[0]), -x[1]))

    # The most relevant location and details will be from the first path in the sorted list
    if sorted_paths:
        most_relevant_path, weight = sorted_paths[0]
        context = most_relevant_path[0][0]
        degree_of_separation = len(most_relevant_path)
        
        # Create a readable path for display
        path_elements = []
        for edge in most_relevant_path:
            if edge[1] in ['IsA', 'AtLocation']:
                arrow = " <- "
            else:
                arrow = " -> "
            path_elements.append(f"{edge[0]} ({edge[1]}){arrow}")
        readable_path = ''.join(path_elements) + object_name
        
        return context, readable_path, weight, degree_of_separation
    else:
        return f"No paths found for {object_name}", None, None, None

# Load the data
with open('paths_modified_4.json', 'r') as file:
    data = json.load(file)

# Test
object_name = "stapler"
context, path, weight, degree_of_separation = get_object_context(data, object_name)
print(f"The most relevant context for {object_name} is {context}.")
print(f"Path: {path}")
print(f"Weight: {weight:.2f}")
print(f"Degree of Separation: {degree_of_separation}")
