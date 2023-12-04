import json
import time


# New function to set robot focus
def set_robot_focus(path_info, focus_contexts, degree_reduction=1, weight_multiplier=1.5):
    path, average_weight, degree_of_separation = path_info
    for edge in path:
        if edge[0] in focus_contexts:
            # print(f"Adjusting for focus context: {edge[0]}") 

            # degree_of_separation = max(1, degree_of_separation - degree_reduction)  # Ensure it doesn't go below 1

            degree_of_separation -= degree_reduction
            average_weight *= weight_multiplier
            break
    return (path, average_weight, degree_of_separation)



def get_object_context(data, object_name, desired_contexts=None, focus_contexts=[]):

    # Start timing for the first implementation
    start_time_1 = time.time()
    """
    Given the data, an object name, and an optional list of desired contexts,
    return its most relevant context along with the path, weight, and degree of separation.
    """
    # If no specific contexts are provided, consider all available contexts
    if not desired_contexts:
        desired_contexts = ["kitchen", "office", "playroom", "living_room", "bedroom", 
                        "dining_room", "pantry", "garden", "laundry_room","bathroom"]
        

    print("Desired Contexts:", desired_contexts)


    
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

    # Exclude paths that have any edge labeled 'Synonym'
    relevant_paths = [path for path in relevant_paths if not any(edge[1] == 'Synonym' for edge in path[0])]

    # # Exclude paths that have any edge labeled 'RelatedTo' with a weight less than 2
    # relevant_paths = [path for path in relevant_paths if not any(edge[1] == 'RelatedTo' and edge[2] < 2 for edge in path[0])]


    # Calculate the average weight for each path based on the robot's focus
    for i, (path, _) in enumerate(relevant_paths):
        # Calculate the average weight for the path
        total_weight = sum(edge[2] for edge in path)
        average_weight = total_weight / len(path)
        degree_of_separation = len(path)

        # Adjust the average weight and degree of separation based on the robot's focus
        if focus_contexts:
            path_info = set_robot_focus((path, average_weight, degree_of_separation), focus_contexts)
        else:
            path_info = (path, average_weight, degree_of_separation)
        
        relevant_paths[i] = path_info


    # Sort the paths by degree of separation and then by weight
    sorted_paths = sorted(relevant_paths, key=lambda x: (x[2], -x[1]))


    # The most relevant location and details will be from the first path in the sorted list
    if sorted_paths:
        most_relevant_path, weight, degree_of_separation = sorted_paths[0]
        context = most_relevant_path[0][0]
        
        # Create a readable path for display
        path_elements = []
        for edge in most_relevant_path:
            if edge[1] in ['IsA', 'AtLocation']:
                arrow = " <- "
            else:
                arrow = " -> "
            path_elements.append(f"{edge[0]} ({edge[1]}){arrow}")
        readable_path = ''.join(path_elements) + object_name

           
        # End timing for the first implementation
        end_time_1 = time.time()

        execution_time_1 = end_time_1 - start_time_1
        print(f"Execution time for the robo-csk implementation: {execution_time_1:.4f} seconds")

        
        return context, readable_path, weight, degree_of_separation
    else:

           
        # End timing for the first implementation
        end_time_1 = time.time()

        execution_time_1 = end_time_1 - start_time_1
        print(f"Execution time for the first implementation: {execution_time_1:.4f} seconds")

        return f"No paths found for {object_name}", None, None, None
 


def get_conceptnet_context(object_name, desired_contexts=None, focus_contexts=None):
    # Load the data
    with open('paths_modified_6.json', 'r') as file:
        data = json.load(file)

    # If desired_contexts or focus_contexts are not provided, set default values
    if desired_contexts is None:
        desired_contexts = ["kitchen", "office", "playroom", "living_room", "bedroom", 
                            "dining_room", "pantry", "garden", "laundry_room", "bathroom"]

    if focus_contexts is None:
        focus_contexts = []

    context, path, weight, degree_of_separation = get_object_context(data, object_name, desired_contexts, focus_contexts)
    print(f"The most relevant context for {object_name} is {context}.")
    if context and not context.startswith("No paths found"):
        print(f"Path: {path}")
        print(f"Average_Weight: {weight:.2f}")
        print(f"Degree of Separation: {degree_of_separation}")
    else:
        print("No relevant paths found.")


    # Return both context and path
    if context and not context.startswith("No paths found"):
        return context, path
    else:
        return "NoPaths", None


# get_conceptnet_context("apple")