import requests

objects = ['apple', 'orange', 'peach', 'strawberry', 'grape', 'pear', 'lemon', 'banana',
               'bottle', 'beer', 'juice', 'wine',
               'carrot', 'bell_pepper', 'cucumber', 'broccoli', 'asparagus', 'zucchini', 'radish', 'artichoke', 'mushroom', 'potato',
               'pretzel', 'popcorn', 'muffin', 'cheese', 'cake', 'cookie', 'pastry', 'doughnut',
               'pen', 'adhesive_tape', 'pencil_case', 'stapler', 'scissors', 'ruler',
               'ball', 'balloon', 'dice', 'flying_disc', 'teddy_bear',
               'platter', 'bowl', 'knife', 'spoon', 'saucer', 'chopsticks', 'drinking_straw', 'mug',
               'glove', 'belt', 'sock', 'tie', 'watch', 'computer_mouse', 'coin', 'calculator', 'box', 'boot', 'towel', 'shorts', 'swimwear',
               'shirt', 'clock', 'hat', 'scarf', 'roller_skates', 'skirt', 'mobile_phone',
               'plastic_bag', 'high_heels', 'handbag', 'clothing', 'oyster', 'tablet_computer', 'book', 'flower', 'candle', 'camera', 'remote_control']

locations = ["kitchen", "office", "child's_bedroom", "living_room", "bedroom", "dining_room", "pantry", "garden", "laundry_room"]


def check_conceptnet_results(lists):
    objects_without_results = []
    for obj in lists:
        response = requests.get(f"http://127.0.0.1:8084/c/en/{obj}?limit=1000")
        edge_exists = len(response.json()['edges']) > 0
        if not edge_exists:
            objects_without_results.append(obj)

    if objects_without_results:
        print("Objects without results:")
        for obj in objects_without_results:
            print(obj)
    else:
        print(f"All {lists} had results.")


check_conceptnet_results(objects)

check_conceptnet_results(locations)