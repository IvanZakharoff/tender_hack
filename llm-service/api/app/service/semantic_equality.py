import torch
import ollama
from  strsimpy.levenshtein import Levenshtein


def semantic_cosine(phrase1, phrase2):
    input_embedding = ollama.embeddings(model='nomic-embed-text', prompt=phrase1)["embedding"]
    another_embedding = ollama.embeddings(model='nomic-embed-text', prompt=phrase2)["embedding"]

    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), torch.tensor(another_embedding).unsqueeze(0))
    return cos_scores[0]

def symbolic_levenshtein(phrase1, phrase2):
    return Levenshtein.distance(phrase1, phrase2)

    