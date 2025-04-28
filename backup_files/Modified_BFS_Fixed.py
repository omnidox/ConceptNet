
import time
from collections import deque, defaultdict

def bfs_modified_with_pathwise_visited(start, max_degree=2):
    """Modified BFS function with tracking, progress updates, and timer."""
    
    start_time = time.time()  # Record the start time
    
    # Initial queue with (node, path, visited set for the path, and weight of the first edge)
    queue = deque([(start, [], set([start]), None)])
    
    paths = defaultdict(list)
    global_visited = set([start])
    path_counter = 0

    while queue:
        node, path, pathwise_visited, first_edge_weight = queue.popleft()

        degree_counter = len(path)

        if degree_counter > max_degree:
            continue

        rel_types = ["AtLocation", "UsedFor"] if degree_counter == 0 else ["RelatedTo", "Synonym", "IsA"]

        for rel_type in rel_types:
            data = fetch_related_data(node, rel_type)

            for edge in data["edges"]:
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
    current_path_string = str(new_path)
    if current_path_string not in paths[next_node]:
        paths[next_node][current_path_string] = current_first_edge_weight

                        path_counter += 1
                        paths[next_node].append((new_path, current_first_edge_weight))
                        if path_counter % 5 == 0:
                            elapsed_time = (time.time() - start_time)/60
                            print(f"Progress: {path_counter} paths found. Elapsed time: {elapsed_time:.2f} minutes...")

        if len(global_visited) % 100 == 0:
            elapsed_time = (time.time() - start_time)/60
            print(f"Progress: Visited {len(global_visited)} unique nodes. Current location: {start}. Current degree: {degree_counter}. Elapsed time: {elapsed_time:.2f} minutes...")

    return paths
