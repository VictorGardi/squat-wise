import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the data
with open('squat_university_data.json', 'r') as f:
    data = json.load(f)

# Initialize the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Create embeddings
texts = [f"{item['title']} {item['content']}" for item in data]
embeddings = model.encode(texts)

# Normalize the vectors
faiss.normalize_L2(embeddings)

# Create the FAISS index
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings)

# Save the index
faiss.write_index(index, "squat_university_faiss_index")

# Save the data in a format that aligns with the index
with open('squat_university_indexed_data.json', 'w') as f:
    json.dump(data, f)
