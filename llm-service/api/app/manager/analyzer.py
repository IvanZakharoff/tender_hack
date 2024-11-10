import ollama
from openai import OpenAI
import torch

class LLMManager:
    # SYSTEM_MESSAGE = 'You are a helpful assistant that is an expert at extracting the most useful information from a given text. Also bring in extra relevant infromation to the user query from outside the given context.'
    SYSTEM_MESSAGE = 'You are a helpful assistant that is an expert at extracting the most useful information from a given text. Imagine that you are a moderator on the site and are looking for answers to questions in the documents. You must always give answers to questions in the form: question: answer(yes or no). explanation: your explanation of the answer'
    MODEL = "ilyagusev/saiga_llama3"
    EMBEDDING_MODEL = 'nomic-embed-text'
    TEMPERATURE = 0.08
    OLAMA_URL = 'http://localhost:11434/v1'

    MAX_TOKENS =  200

    def __init__(self, text):
        self.text = text
        self.text_lines = []
        self.ollama_client = OpenAI(
            base_url=self.OLAMA_URL,
            api_key=self.MODEL
        )
        self.init_embeggins()

    def _get_embeggings(self, text):
        lines = text.split('\n') # TODO: some \n
        result = []
        for line in lines:
            response = ollama.embeddings(model=self.EMBEDDING_MODEL, prompt=line) 
            result.append(response["embedding"])
        return result 
    
    def init_embeggins(self):
        self._embegging_tensor = torch.tensor(self._get_embeggings(self.text))  
    
    def init_context(self, input):
        self._context = self.get_relevant_context(input)

    def _get_relevant_context_by_input(self, input, top_k=3):
        if self._embegging_tensor.nelement() == 0:  # Check if the tensor has any elements
            return []
        # Encode the rewritten input
        input_embedding = ollama.embeddings(model=self.EMBEDDING_MODEL, prompt=input)["embedding"]
        # Compute cosine similarity between the input and vault embeddings
        cos_scores = torch.cosine_similarity(torch.tensor(input_embedding).unsqueeze(0), self._embegging_tensor)
        # Adjust top_k if it's greater than the number of available scores
        top_k = min(top_k, len(cos_scores))
        # Sort the scores and get the top-k indices
        top_indices = torch.topk(cos_scores, k=top_k)[1].tolist()
        # Get the corresponding context from the vault
        relevant_context = [self.text_lines[idx].strip() for idx in top_indices]
        return relevant_context
    
    def ask_saiga(self, queries:list[str]):
        responses = []
        for query in queries:
            context = self._get_relevant_context_by_input(query)
            messages = [
                {"role": "system", "content": self.SYSTEM_MESSAGE},
                {"role": "user", "content": f"{query}\n\nRelevant Context:\n\n{context}"},
            ]

            
            response = self.ollama_client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                max_tokens=self.MAX_TOKENS,
                temperature=self.TEMPERATURE,
                
            )
            responses.append(response.choices[0].message.content)
        return responses
