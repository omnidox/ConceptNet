def count_objects(object_list):
    object_count = len(object_list)
    return object_count

if __name__ == "__main__":
    objects = ['apple', 'orange', 'peach', 'strawberry', 'grape', 'pear', 'lemon', 'banana',
               'bottle', 'beer', 'juice', 'wine',
               'carrot', 'bell_pepper', 'cucumber', 'broccoli', 'garden_asparagus', 'zucchini', 'radish', 'artichoke', 'mushroom', 'potato',
               'pretzel', 'popcorn', 'muffin', 'cheese', 'cake', 'cookie', 'pastry', 'doughnut',
               'pen', 'adhesive_tape', 'pencil_case', 'stapler', 'scissors', 'ruler',
               'ball', 'balloon', 'dice', 'flying_disc', 'teddy_bear',
               'platter', 'bowl', 'knife', 'spoon', 'saucer', 'chopsticks', 'drinking_straw', 'mug',
               'glove', 'belt', 'sock', 'tie', 'watch', 'computer_mouse', 'coin', 'calculator', 'box', 'boot', 'towel', 'shorts', 'swimwear',
               'shirt', 'clock', 'hat', 'scarf', 'roller_skates', 'skirt', 'mobile_phone',
               'plastic_bag', 'high_heels', 'handbag', 'clothing', 'oyster', 'tablet_computer', 'book', 'flower', 'candle', 'camera', 'remote_control']

    total_objects = count_objects(objects)
    print("Total number of objects:", total_objects)
