import requests
from collections import deque, defaultdict
import json

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

MAX_DEGREE = 4

# BFS Implementation
def bfs(start):
    visited = set()
    queue = deque([(start, [], 0)])  # node, path, degree
    paths = defaultdict(list)

    while queue:
        node, path, degree = queue.popleft()

        if degree > MAX_DEGREE:
            continue

        rel_type = None
        if degree == 0:
            rel_types = ["AtLocation", "UsedFor"]
        else:
            rel_types = ["RelatedTo", "Synonym", "IsA"]

        for rel_type in rel_types:
            response = requests.get(f"http://127.0.0.1:8084/query?node=/c/en/{node}&rel=/r/{rel_type}&limit=1000")
            data = response.json()

            for edge in data["edges"]:
                if edge["rel"]["lang"] != "en":
                    continue

                next_node = None
                weight = edge["weight"]
                relation = edge["rel"]["label"]

                if degree == 0:
                    if "AtLocation" in edge["rel"]["label"] and edge["start"]["label"] != node:
                        next_node = edge["start"]["label"]
                    elif "UsedFor" in edge["rel"]["label"] and edge["end"]["label"] != node:
                        next_node = edge["end"]["label"]

                else:
                    if "RelatedTo" in edge["rel"]["label"] or "Synonym" in edge["rel"]["label"]:
                        if edge["start"]["label"] != node and edge["start"]["label"] not in visited:
                            next_node = edge["start"]["label"]
                        elif edge["end"]["label"] != node and edge["end"]["label"] not in visited:
                            next_node = edge["end"]["label"]
                    elif "IsA" in edge["rel"]["label"] and edge["start"]["label"] != node and edge["start"]["label"] not in visited:
                        next_node = edge["start"]["label"]


                if next_node and next_node not in visited:
                    visited.add(next_node)
                    new_path = path + [(node, relation, weight)]
                    queue.append((next_node, new_path, degree + 1))

                    if next_node in OBJECTS:
                        paths[next_node].append(new_path)

        print(f"Progress: Visited {len(visited)} nodes...")

    return paths

# Main Execution
all_paths = {}
for location in LOCATIONS:
    all_paths[location] = bfs(location)

# Save to JSON
with open("paths.json", "w") as f:
    json.dump(all_paths, f)

print("Data saved to paths.json")
