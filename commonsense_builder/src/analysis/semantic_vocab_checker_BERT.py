import gensim.downloader as api
import numpy as np
from transformers import BertTokenizer, BertModel
import torch

# Load pre-trained Word2Vec and GloVe models
word2vec_model = api.load("word2vec-google-news-300")
glove_model = api.load("glove-wiki-gigaword-300")

# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained('bert-base-uncased')

# Lists of objects and locations

OBJECTS = ['apple', 'orange', 'peach', 'strawberry', 'grape', 'pear', 'lemon', 'banana',
'bottle', 'beer', 'juice', 'wine',
'carrot', 'bell_pepper', 'cucumber', 'broccoli', 'asparagus', 'zucchini', 'radish', 'artichoke', 'mushroom', 'potato',
'pretzel', 'popcorn', 'muffin', 'cheese', 'cake', 'cookie', 'pastry',
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


# Function to check representation in BERT
def check_in_bert(word):
    # Tokenize the word
    inputs = tokenizer(word, return_tensors="pt")

    # Get the token ids for checking if it's split
    token_ids = inputs["input_ids"].numpy()[0]
    tokens = [tokenizer.decode([token_id]) for token_id in token_ids]

    print(f"Word: {word}")
    print("BERT Tokens:", tokens)

    # Get embeddings
    with torch.no_grad():
        outputs = bert_model(**inputs)
    embeddings = outputs.last_hidden_state

    # Further analysis can be done as needed


# Function to check if a word is in a model's vocabulary and handle split words
def check_in_vocab_and_average(model, word, model_name):
    underscore_word = word.replace(" ", "_")
    space_word = word.replace("_", " ")

    # Check if the whole word is in the vocabulary
    if underscore_word in model.key_to_index:
        print(f"'{underscore_word}' (underscore version) is in the {model_name} vocabulary.")
    elif space_word in model.key_to_index:
        print(f"'{space_word}' (space-separated version) is in the {model_name} vocabulary.")
    else:
        # Split the word and check individual parts
        parts = underscore_word.split('_')
        if all(part in model.key_to_index for part in parts):
            # Calculate the average vector for the parts
            vectors = [model[part] for part in parts]
            avg_vector = np.mean(vectors, axis=0)
            print(f"'{word}' is represented as split words in the {model_name} vocabulary. Average vector calculated.")
        else:
            print(f"'{word}' is not in the {model_name} vocabulary.")

# Check each word in the objects and locations lists
for word in OBJECTS + LOCATIONS:
    # check_in_vocab_and_average(word2vec_model, word, "Word2Vec")
    # check_in_vocab_and_average(glove_model, word, "GloVe")
    check_in_bert(word)

print("Vocabulary check complete.")
