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
    if desired_contexts is None:
        desired_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                            "dining_room", "pantry", "garden", "laundry_room","bathroom"]
    # print("Keys in data:", data.keys())
    # Specify desired contexts here


        # Print the desired_contexts list
        print("Desired Contexts1:", desired_contexts)
    print("Desired Contexts2:", desired_contexts)


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
        # if loc == "child's_bedroom":
            # print("Object:", obj)
            # print("Location:", loc)

        if obj == object_name and loc in desired_contexts:
            # print("Object:", obj)
            # print("Location:", loc)

            relevant_paths.extend(paths_list)

    # Exclude paths that have any edge labeled 'Synonym'
    relevant_paths = [path for path in relevant_paths if not any(edge[1] == 'Synonym' for edge in path[0])]

    # print("Relevant Paths before sorting:", relevant_paths)

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

    return sorted_paths


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
 
# Load the data
with open('paths_modified_5.json', 'r') as file:
    data = json.load(file)


# Test
object_name = "toy"


# Specify desired contexts here
desired_contexts = [
    "kitchen", "child's_bedroom", "office", "playroom", "living_room", "bedroom", "dining_room", "pantry", "garden", "laundry_room", "bathroom"
    ]  



# Prompt the user for tasks
available_contexts = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", 
                     "dining_room", "pantry", "garden", "laundry_room"]

prompt_message = ("Please input what contexts or multiple contexts separated by commas for the robot to focus on. "
                 f"These are the possible contexts: {', '.join(available_contexts)} "
                 "(or press Enter to continue without specifying tasks): ")

while True:
    user_input = input(prompt_message).strip()

    # Split the input by commas and strip whitespace
    robot_focus = [task.strip() for task in user_input.split(",")] if user_input else []

    # Check if all tasks are in available_contexts
    if all(task in available_contexts for task in robot_focus) or not robot_focus:

        if robot_focus:
            print(f"You have set the robot's focus on: {', '.join(robot_focus)}")
        else:
            print("There will be no focus.")
        break
    else:
        print("One or more of the contexts you entered are not valid. Please try again.")


# Get the sorted paths for the specified object
# ... [rest of the code]

# Get the sorted paths for the specified object
sorted_paths = get_object_context(data, object_name, desired_contexts, robot_focus)

# Print the top 100 paths
# print(f"Top 100 paths for {object_name}:")
for i, (path, weight, degree_of_separation) in enumerate(sorted_paths[:10]):
    path_elements = []
    for edge in path:
        if edge[1] in ['IsA', 'AtLocation']:
            arrow = " <- "
        else:
            arrow = " -> "
        path_elements.append(f"{edge[0]} ({edge[1]}){arrow}")
    readable_path = ''.join(path_elements) + object_name
    print(f"{i+1}. Path: {readable_path}")
    print(f"   Average Weight: {weight:.2f}")
    print(f"   Degree of Separation: {degree_of_separation}")

# ... [rest of the code]

# context, path, weight, degree_of_separation = get_object_context(data, object_name, desired_contexts, robot_focus)
# print(f"The most relevant context for {object_name} is {context}.")
# if context and not context.startswith("No paths found"):
#     print(f"Path: {path}")
#     print(f"Average_Weight: {weight:.2f}")
#     print(f"Degree of Separation: {degree_of_separation}")
# else:
#     print("No relevant paths found.")