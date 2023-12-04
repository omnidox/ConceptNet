from transformers import AutoTokenizer, AutoModel
from scipy.spatial.distance import cosine
import gensim.downloader as api
import numpy as np


# Load pre-trained BERT model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
bert_model = AutoModel.from_pretrained("bert-base-uncased")

# Load pre-trained Word2Vec and GloVe models
word2vec_model = api.load("word2vec-google-news-300")
glove_model = api.load("glove-wiki-gigaword-300")

def get_bert_vector(text):
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
    outputs = bert_model(**inputs)
    # return outputs[0].detach().numpy().mean(axis=1)
    # Ensure the output is 1-D by reshaping
    return outputs[0].detach().numpy().mean(axis=1).reshape(-1)

def get_word2vec_glove_vector(model, word):
    underscore_word = word.replace(" ", "_")
    space_word = word.replace("_", " ")

    if underscore_word in model.key_to_index:
        return model[underscore_word]
    elif space_word in model.key_to_index:
        return model[space_word]
    else:
        parts = underscore_word.split('_')
        if all(part in model.key_to_index for part in parts):
            vectors = [model[part] for part in parts]
            return np.mean(vectors, axis=0)
        else:
            raise ValueError(f"'{word}' is not in the model vocabulary.")

def calculate_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

# Example usage
word1 = "apple"
word2 = "fruit"

# Get vectors for each model
bert_vec1 = get_bert_vector(word1)
bert_vec2 = get_bert_vector(word2)
word2vec_vec1 = get_word2vec_glove_vector(word2vec_model, word1)
word2vec_vec2 = get_word2vec_glove_vector(word2vec_model, word2)
glove_vec1 = get_word2vec_glove_vector(glove_model, word1)
glove_vec2 = get_word2vec_glove_vector(glove_model, word2)

# Calculate cosine similarity for each model
bert_similarity = calculate_similarity(bert_vec1, bert_vec2)
word2vec_similarity = calculate_similarity(word2vec_vec1, word2vec_vec2)
glove_similarity = calculate_similarity(glove_vec1, glove_vec2)

# Print individual similarities
print(f"BERT Similarity: {bert_similarity}")
print(f"Word2Vec Similarity: {word2vec_similarity}")
print(f"GloVe Similarity: {glove_similarity}")

# Average the scores
average_similarity = (bert_similarity + word2vec_similarity + glove_similarity) / 3

print(f"Average Semantic Similarity Score: {average_similarity}")
