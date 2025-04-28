import requests
from collections import deque, defaultdict
import json
import os
import time
import sys

# Constants

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

LOCATIONS = ["kitchen", "office", "playroom", "living_room", "bedroom", "dining_room", "pantry", "garden", "laundry_room", "bathroom"]

API_ENDPOINT = "http://127.0.0.1:8084/query"

start_time = time.time()  # Record the start time

CACHE_FILE = ''
node_data_cache2 = {}

def save_cache_to_file():
    with open(CACHE_FILE, 'w') as f:
        json.dump(node_data_cache2, f)

def load_cache_from_file():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return {}

node_data_cache2 = load_cache_from_file()

def fetch_related_data(node, rel_type):
    """Fetch related data for a given node and relationship type from the API, with caching."""
    # Check if data for the node is present in cache
    if node in node_data_cache2 and rel_type in node_data_cache2[node]:
        return node_data_cache2[node][rel_type]

    # If not present in cache, make the API call
    url = f"{API_ENDPOINT}?node=/c/en/{node}&rel=/r/{rel_type}&limit=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()

        # Cache the result
        if node not in node_data_cache2:
            node_data_cache2[node] = {}
        node_data_cache2[node][rel_type] = response.json()

        return node_data_cache2[node][rel_type]
    except requests.RequestException as e:
        print(f"Error fetching data for node {node} and relation {rel_type}: {e}")
        return {"edges": []}


def bfs_modified_with_pathwise_visited(start, max_degree=3):
    """Modified BFS function with tracking, progress updates, and timer."""
    
    # start_time = time.time()  # Record the start time
    
    # Initial queue with (node, path, visited set for the path, and weight of the first edge)
    queue = deque([(start, [], set([start]), None)])
    
    paths = defaultdict(list)
    global_visited = set([start])
    path_counter = 0
    
    # Introducing the processed_edges set
    
    try:
        while queue:
            node, path, pathwise_visited, first_edge_weight = queue.popleft()

            # processed_edges = set()
            
            degree_counter = len(path)

            if degree_counter > max_degree:
                continue

            rel_types = ["AtLocation", "UsedFor", "Synonym", "IsA"] if degree_counter == 0 else ["AtLocation", "UsedFor", "RelatedTo", "IsA"]

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


                    if start_label != node and end_label != node:
                        continue

                    if relation == "AtLocation" and start_label != node and start_label not in pathwise_visited:
                        next_node = start_label
                    elif relation == "UsedFor" and end_label != node and end_label not in pathwise_visited:
                        next_node = end_label


                    elif relation == "Synonym":
                            if start_label != node and start_label not in pathwise_visited:
                                next_node = start_label
                            elif end_label != node and end_label not in pathwise_visited:
                                next_node = end_label 

                    elif relation == "RelatedTo":
                            # print (weight)
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
                        modified_next_node = next_node.split('/')[0]

                        if modified_next_node in OBJECTS:
                            path_counter += 1
                            paths[next_node].append((new_path, current_first_edge_weight))
                            if path_counter % 5 == 0:
                                elapsed_time = (time.time() - start_time)/60
                                print(f"Progress: {path_counter} paths found. Elapsed time: {elapsed_time:.2f} minutes Current location: {start}. Current degree: {degree_counter}...")

            if len(global_visited) % 100 == 0:
                elapsed_time = (time.time() - start_time)/60
                print(f"Progress: Visited {len(global_visited)} unique nodes. Current location: {start}. Current degree: {degree_counter}. Elapsed time: {elapsed_time:.2f} minutes...")

        return paths, True


    except KeyboardInterrupt:
        print("\\nUser interrupted the BFS traversal. Saving any necessary data...")
        return paths, False
        # raise  # Propagate the exception upwards

# Update the main function to call the new BFS function
def main():
    all_paths = {}
    not_found_objects = set(OBJECTS)

    for location in LOCATIONS:
        location_paths, success = bfs_modified_with_pathwise_visited(location)


        for obj, obj_paths in location_paths.items():
            if obj in not_found_objects:
                not_found_objects.remove(obj)
            all_paths[f"{location}:{obj}"] = obj_paths

        if not success:
            break

    output_file = "paths_modified_6.json"
    if os.path.exists(output_file):
        print(f"Warning: {output_file} already exists. Data will be overwritten.")

    with open(output_file, "w") as f:
        json.dump(all_paths, f)

    print(f"Data saved to {output_file}")
    if not_found_objects:
        print(f"Objects not found: {', '.join(not_found_objects)}")

    #uncomment the following line to save the cache to file
    # save_cache_to_file()

    elapsed_time = (time.time() - start_time)/60
    print(f"Elapsed time: {elapsed_time:.2f} minutes...")

# We can't execute the main_modified function here since it relies on external API calls and other constants defined in the original code.
# However, we've made the necessary modifications to the BFS function.


if __name__ == "__main__":
    main()

