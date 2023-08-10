
import json

# Load the data
with open('paths_modified.json', 'r') as file:
    data = json.load(file)

def find_max_degree_for_relationship(data, relationship):
    """Determine the maximum degree of separation for paths with the given relationship."""
    max_degree = 0
    for key, paths_list in data.items():
        for path, _ in paths_list:
            for edge in path:
                if edge[1] == relationship:
                    max_degree = max(max_degree, len(path))
                    break
    return max_degree

def search_for_relationship(relationship):
    """Search for paths containing the given relationship and print them."""
    max_degree_relationship = find_max_degree_for_relationship(data, relationship)

    for key, paths_list in data.items():
        parts = key.split('_')
        location, object_ = '_'.join(parts[:-1]), parts[-1]

        # Check if any of the paths for this object contains the specified relationship and has the max degree
        paths_with_relationship = [(path, path_weight) for path, path_weight in paths_list if any(edge[1] == relationship for edge in path) and len(path) == max_degree_relationship]
        
        if paths_with_relationship:
            print("\nPaths from {} to {} containing '{}' with maximum degree of {}:".format(location, object_, relationship, max_degree_relationship))
            for path, path_weight in paths_with_relationship:
                readable_path = " -> ".join([edge[0] + " (" + edge[1] + ")" for edge in path])
                readable_path += " -> " + object_  # Append the object to the end
                print("{} | Weight: {:.2f}".format(readable_path, path_weight))

# Example usage: Uncomment the line below to search for paths containing a specific relationship
search_for_relationship("IsA")
