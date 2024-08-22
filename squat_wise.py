import json
from typing import Optional

import faiss
import torch
from sentence_transformers import SentenceTransformer
from transformers import GPT2LMHeadModel, GPT2Tokenizer

MODEL = "gpt2-squat-university"
PATH_TO_INDEX = "squat_university_faiss_index"
PATH_TO_INDEXED_DATA = "squat_university_indexed_data.json"
PROMPT = ("You are an AI assistant trained to respond like Squat University. "
          "Use the following information to answer the query:\n\n")


class SquatWise:
    def __init__(self, model: Optional[str] = MODEL, path_to_index: Optional[str] = PATH_TO_INDEX, path_to_indexed_data: Optional[str] = PATH_TO_INDEXED_DATA, **kwargs):
        self._model = model
        self._path_to_index = path_to_index
        self._path_to_indexed_data = path_to_indexed_data
        self.prompt = kwargs.get("prompt", PROMPT)
        self.max_length = kwargs.get("max_length", 1024)
        self.max_new_tokens = kwargs.get("max_new_tokens", 1024)
        self.model = GPT2LMHeadModel.from_pretrained(self._model)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.index = faiss.read_index(self._path_to_index)
        with open('squat_university_indexed_data.json', 'r') as f:
            self.indexed_data = json.load(f)

        # Initialize the sentence transformer model for query encoding
        self.st_model = SentenceTransformer('all-MiniLM-L6-v2')

    def retrieve_relevant_info(self, query: str, k: int=3) -> list[dict]:
        # Encode the query
        query_vector = self.st_model.encode([query])
        faiss.normalize_L2(query_vector)

        # Search the index
        _, result = self.index.search(query_vector, k)
        
        # Fetch the relevant information
        relevant_info = [self.indexed_data[i] for i in result[0]]
        return relevant_info

    def generate_response(self, query: str, relevant_info: list[dict]):
        prompt = self.prompt
        # Craft the prompt
        for info in relevant_info:
            prompt += f"Title: {info['title']}\nContent: {info['content'][:400]}...\n\n"
        prompt += f"Query: {query}\nResponse:"
        print("Found relevent info!")

        # Generate the response
        inputs = self.tokenizer(prompt, return_tensors="pt", max_length=self.max_length, truncation=True)
        inputs = inputs.to(self.device)

        # Generate the response
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=self.max_length,
                num_return_sequences=1,
                temperature=0.9,
                top_k=50,
                top_p=0.95,
                do_sample=True,
                no_repeat_ngram_size=2,
                early_stopping=False
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract only the generated response, not the entire prompt
        response = response#.split("Response:")[-1].strip()

        return response
    def ask(self, query: str) -> str:
        relevant_info = self.retrieve_relevant_info(query)
        return self.generate_response(query, relevant_info)


