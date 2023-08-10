import requests
from collections import deque, defaultdict
import json
import os
import time

API_ENDPOINT = "http://127.0.0.1:8084/query"

def fetch_related_data(node, rel_type):
    url = f"{API_ENDPOINT}?node=/c/en/{node}&rel=/r/{rel_type}&limit=1000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data for node {node} and relation {rel_type}: {e}")
        return {"edges": []}

def extract_first_100_nodes(start, max_degree=2):
    queue = deque([(start, [], set([start]), None)])
    global_visited = set([start])
    first_100_nodes = []

    while queue and len(first_100_nodes) < 100:
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
                start_label = edge["start"]["label"]
                end_label = edge["end"]["label"]

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
                    if next_node not in global_visited:
                        first_100_nodes.append(next_node)
                        if len(first_100_nodes) >= 100:
                            break
                    global_visited.add(next_node)
                    new_visited = pathwise_visited.copy()
                    new_visited.add(next_node)
                    new_path = path + [(node, relation, weight)]
                    current_first_edge_weight = first_edge_weight if first_edge_weight is not None else weight
                    queue.append((next_node, new_path, new_visited, current_first_edge_weight))
            if len(first_100_nodes) >= 100:
                break

    return first_100_nodes

# Sample usage:
nodes = extract_first_100_nodes("house")
print(nodes)
