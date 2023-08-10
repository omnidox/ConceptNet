import requests
from collections import deque, defaultdict
import json
import os

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
'plastic_bag', 'high_heels', 'handbag', 'clothing', 'oyster', 'tablet_computer', 'book', 'flower', 'candle', 'camera', 'remote_control']

LOCATIONS = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", "dining_room", "pantry", "garden", "laundry_room"]
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

def bfs_modified(start, max_degree=4):
    """Modified BFS function to start from each location and find each object."""
    visited = set()
    queue = deque([(start, [], None)])  # node, path, weight of the first edge
    paths = defaultdict(list)
    progress_counter = 0

    while queue:
        node, path, first_edge_weight = queue.popleft()

        if len(path) > max_degree:
            continue

        rel_types = ["AtLocation", "UsedFor"] if len(path) == 0 else ["RelatedTo", "Synonym", "IsA"]

        for rel_type in rel_types:
            data = fetch_related_data(node, rel_type)

            for edge in data["edges"]:
                if edge["rel"]["lang"] != "en":
                    continue

                next_node = None
                weight = edge["weight"]
                relation = edge["rel"]["label"]
                
                start_label = edge["start"]["label"]
                end_label = edge["end"]["label"]

                if relation == "AtLocation" and start_label != node:
                    next_node = start_label
                elif relation in ["UsedFor", "RelatedTo", "Synonym"] and end_label != node and end_label not in visited:
                    next_node = end_label
                elif relation == "IsA" and start_label != node and start_label not in visited:
                    next_node = start_label

                if next_node and next_node not in visited:
                    visited.add(next_node)
                    new_path = path + [(node, relation, weight)]
                    # If this is the first edge, record its weight
                    if first_edge_weight is None:
                        first_edge_weight = weight
                    queue.append((next_node, new_path, first_edge_weight))
                    if next_node in OBJECTS:
                        paths[next_node].append((new_path, first_edge_weight))

        progress_counter += 1
        if progress_counter % 100 == 0:
            print(f"Progress: Visited {len(visited)} nodes...")

    return paths

def main():
    """Modified main execution function."""
    all_paths = {}
    not_found_objects = set(OBJECTS)

    for location in LOCATIONS:
        location_paths = bfs_modified(location)
        for obj, obj_paths in location_paths.items():
            if obj in not_found_objects:
                not_found_objects.remove(obj)
            all_paths[(location, obj)] = obj_paths

    output_file = "paths_modified.json"
    if os.path.exists(output_file):
        print(f"Warning: {output_file} already exists. Data will be overwritten.")

    with open(output_file, "w") as f:
        json.dump(all_paths, f)

    print(f"Data saved to {output_file}")
    if not_found_objects:
        print(f"Objects not found: {', '.join(not_found_objects)}")

if __name__ == "__main__":
    main()

