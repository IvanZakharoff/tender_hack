import torch
import ollama


def semantic_compare_strigs(phrase1, phrase2):
    input_embedding = ollama.embeddings(model='nomic-embed-text', prompt=phrase1)["embedding"]
    another_embedding = ollama.embeddings(model='nomic-embed-text', prompt=phrase2)["embedding"]

    cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), torch.tensor(another_embedding).unsqueeze(0))
    return cos_scores[0]
