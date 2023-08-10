import requests
from collections import deque, defaultdict
import json
import os
import time

# Constants

OBJECTS = ['mobile_phone', 'calculator']

LOCATIONS = ['house']

API_ENDPOINT = "http://127.0.0.1:8084/query"

def fetch_related_data(node, rel_type):
    """Fetch related data for a given node and relationship type from the API."""
    url = f"{API_ENDPOINT}?node=/c/en/{node}&rel=/r/{rel_type}&limit=1000"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for node {node} and relation {rel_type}: {e}")
        return {"edges": []}


def bfs_modified_with_pathwise_visited(start, max_degree=2):
    """Modified BFS function with tracking, progress updates, and timer."""
    
    start_time = time.time()  # Record the start time
    
    # Initial queue with (node, path, visited set for the path, and weight of the first edge)
    queue = deque([(start, [], set([start]), None)])
    
    paths = defaultdict(list)
    global_visited = set([start])
    path_counter = 0
    
    # Introducing the processed_edges set
    

    while queue:
        node, path, pathwise_visited, first_edge_weight = queue.popleft()

        processed_edges = set()
        
        degree_counter = len(path)

        if degree_counter > max_degree:
            continue

        rel_types = ["AtLocation", "UsedFor"] if degree_counter == 0 else ["RelatedTo", "Synonym", "IsA"]

        for rel_type in rel_types:
            data = fetch_related_data(node, rel_type)

            for edge in data["edges"]:
                
                # Checking if the edge has already been processed
                edge_tuple = (edge["start"]["@id"], edge["end"]["@id"], edge["rel"]["label"])
                if edge_tuple in processed_edges:
                    continue
                
                # Adding the edge to the processed_edges set
                processed_edges.add(edge_tuple)
                
                if edge["start"]["language"] != "en" or edge["end"]["language"] != "en":
                    continue

                next_node = None
                weight = edge["weight"]
                if weight < 1:
                    continue
                relation = edge["rel"]["label"]
                
                start_label = edge["start"]["@id"].replace("/c/en/", "")
                end_label = edge["end"]["@id"].replace("/c/en/", "")

                if relation == "AtLocation" and start_label != node and start_label not in pathwise_visited:
                    next_node = start_label
                elif relation == "UsedFor" and end_label != node and end_label not in pathwise_visited:
                    next_node = end_label
                elif relation in ["RelatedTo", "Synonym"]:
                        if start_label != node and start_label not in pathwise_visited:
                            next_node = start_label
                        elif end_label != node and end_label not in pathwise_visited:
                            next_node = end_label                    
                elif relation == "IsA" and start_label != node and start_label not in pathwise_visited:
                    next_node = start_label

                if next_node and next_node not in pathwise_visited:
                    global_visited.add(next_node)
                    new_visited = pathwise_visited.copy()
                    new_visited.add(next_node)
                    new_path = path + [(node, relation, weight)]
                    current_first_edge_weight = first_edge_weight if first_edge_weight is not None else weight
                    queue.append((next_node, new_path, new_visited, current_first_edge_weight))
                    if next_node in OBJECTS:
                        path_counter += 1
                        paths[next_node].append((new_path, current_first_edge_weight))
                        if path_counter % 5 == 0:
                            elapsed_time = (time.time() - start_time)/60
                            print(f"Progress: {path_counter} paths found. Elapsed time: {elapsed_time:.2f} minutes...")

        if len(global_visited) % 100 == 0:
            elapsed_time = (time.time() - start_time)/60
            print(f"Progress: Visited {len(global_visited)} unique nodes. Current location: {start}. Current degree: {degree_counter}. Elapsed time: {elapsed_time:.2f} minutes...")

    return paths


# Update the main function to call the new BFS function
def main():
    all_paths = {}
    not_found_objects = set(OBJECTS)

    for location in LOCATIONS:
        location_paths = bfs_modified_with_pathwise_visited(location)
        for obj, obj_paths in location_paths.items():
            if obj in not_found_objects:
                not_found_objects.remove(obj)
            all_paths[f"{location}:{obj}"] = obj_paths

    output_file = "paths_modified.json"
    if os.path.exists(output_file):
        print(f"Warning: {output_file} already exists. Data will be overwritten.")

    with open(output_file, "w") as f:
        json.dump(all_paths, f)

    print(f"Data saved to {output_file}")
    if not_found_objects:
        print(f"Objects not found: {', '.join(not_found_objects)}")

# We can't execute the main_modified function here since it relies on external API calls and other constants defined in the original code.
# However, we've made the necessary modifications to the BFS function.


if __name__ == "__main__":
    main()

