import json

def get_object_context(data, object_name, desired_contexts=None):
    """
    Given the data, an object name, and an optional list of desired contexts,
    return its most relevant context along with the path, weight, and degree of separation.
    """
    # If no specific contexts are provided, consider all available contexts
    if desired_contexts is None:
        desired_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                            "dining_room", "pantry", "garden", "laundry_room"]
    
    # If the object isn't present in the data, return a message indicating that
    if object_name not in [key.split(':')[1] for key in data]:
        return f"No paths found for {object_name}"
    
    # Gather paths relevant to the object
    relevant_paths = []
    for key, paths_list in data.items():
        loc, obj = key.split(':')

        # Remove the '/c/en/' prefix from the object name
        obj = obj.split('/')[0]

        # Only consider paths that have the desired context
        if obj == object_name and loc in desired_contexts:
            relevant_paths.extend(paths_list)

    # # Exclude paths that have any edge labeled 'RelatedTo'
    # relevant_paths = [path for path in relevant_paths if not any(edge[1] == 'RelatedTo' for edge in path[0])]

    # Calculate the average weight for each path
    for i, (path, _) in enumerate(relevant_paths):  # Ignore the provided path weight
        total_weight = sum(edge[2] for edge in path)
        average_weight = total_weight / len(path)
        relevant_paths[i] = (path, average_weight)


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
object_name = "high_heels"
desired_contexts = ["office", "living_room", "bedroom"]  # Specify desired contexts here
context, path, weight, degree_of_separation = get_object_context(data, object_name)
print(f"The most relevant context for {object_name} is {context}.")
if context and not context.startswith("No paths found"):
    print(f"Path: {path}")
    print(f"Average_Weight: {weight:.2f}")
    print(f"Degree of Separation: {degree_of_separation}")
else:
    print("No relevant paths found.")