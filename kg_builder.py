import requests
import json

def get_related_concepts(start_locations):
    related_concepts = []
    queue = [(location, 0) for location in start_locations]  # Term, degree of separation
    visited = set(start_locations)

    while queue:
        current_term, degree = queue.pop(0)
        print(f"Processing term: {current_term}, Degree: {degree}")  # Progress update

        # Determine the relationship types based on the degree of separation
        if degree == 0:
            relationship_types = ["/r/AtLocation", "/r/UsedFor"]
        elif degree < 4:
            relationship_types = ["/r/RelatedTo", "/r/IsA"]
        else:
            continue

        for rel_type in relationship_types:
            url = f"http://api.conceptnet.io/query?node=/c/en/{current_term}&rel={rel_type}&limit=10"
            response = requests.get(url)
            data = response.json()

            for edge in data['edges']:
                if degree == 0:
                    if 'AtLocation' in edge['rel']['label']:
                        related_term = edge['start']['label']
                    elif 'UsedFor' in edge['rel']['label']:
                        related_term = edge['end']['label']
                    else:
                        continue
                elif 'RelatedTo' in edge['rel']['label']:
                    related_term = edge['start']['label'] if edge['start']['label'] != current_term else edge['end']['label']
                else:  # IsA relationship
                    related_term = edge['start']['label']

                relationship = edge['rel']['label']
                confidence = edge['weight']

                if related_term not in visited:
                    related_concepts.append((current_term, related_term, relationship, degree + 1, confidence))
                    queue.append((related_term, degree + 1))
                    visited.add(related_term)

    return related_concepts


locations = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", "dining_room", "pantry", "garden", "laundry_room"]
related_concepts = get_related_concepts(locations)

with open('related_concepts.json', 'w') as file:
    json.dump(related_concepts, file)


def trace_connections(object_name):
    with open('related_concepts.json', 'r') as file:
        related_concepts = json.load(file)

    for concept in related_concepts:
        source, target, relationship, degree, weight = concept
        if target == object_name and relationship in ["/r/AtLocation", "/r/UsedFor"]:
            print(f"{source} -> {target} (Relationship: {relationship}, Weight: {weight})")

trace_connections("spoon")
