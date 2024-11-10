import ollama
from openai import OpenAI
import torch

client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ilyagusev/saiga_llama3'
)

class LLMManager:
    SYSTEM_MESSAGE = 'You are a helpful assistant that is an expert at extracting the most useful information from a given text. Also bring in extra relevant infromation to the user query from outside the given context.'

    def embegging(text):
        lines = text.split('\n') # TODO: some \n
        result = []
        for line in lines:
            response = ollama.embeddings(model='nomic-embed-text', prompt=line) 
            result.append(response["embedding"])

    def get_relevant_context(text, vault_embeddings, vault_content, top_k=3):
        if vault_embeddings.nelement() == 0:  # Check if the tensor has any elements
            return []
        # Encode the rewritten input
        input_embedding = ollama.embeddings(model='nomic-embed-text', prompt=text)["embedding"]
        # Compute cosine similarity between the input and vault embeddings
        cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), vault_embeddings)
        # Adjust top_k if it's greater than the number of available scores
        top_k = min(top_k, len(cos_scores))
        # Sort the scores and get the top-k indices
        top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
        # Get the corresponding context from the vault
        relevant_context = [vault_content[idx].strip() for idx in top_indices]
        return relevant_context
    
