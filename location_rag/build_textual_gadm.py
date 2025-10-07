from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from torch import float16
import pandas as pd 

# Load embedding model
encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Sample knowledge base documents
documents = pd.read_csv("gadm_text.csv")["text"]
print("loaded documents")
# Generate embeddings
doc_embeddings = encoder.encode(documents, show_progress_bar=True)
print(f"Created {len(doc_embeddings)} document embeddings")

# Create FAISS index for fast retrieval
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner product similarity

# Add embeddings to index
index.add(doc_embeddings.astype('float32'))

def retrieve_documents(query, top_k=3):
    """Retrieve most relevant documents for query"""
    query_embedding = encoder.encode([query])
    
    # Search index
    scores, indices = index.search(query_embedding.astype('float32'), top_k)
    
    # Return relevant documents
    retrieved_docs = [documents[i] for i in indices[0]]
    return retrieved_docs, scores[0]

# Test retrieval
query = "What is the GID of Zarqa?"
docs, scores = retrieve_documents(query)
print(f"Retrieved {len(docs)} documents")


from transformers import AutoModelForCausalLM, AutoTokenizer

# Load generation model
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
generator = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="balanced", top_k=10, do_sample=True, torch_dtype=float16
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

def generate_response(query, retrieved_docs):
    """Generate response using retrieved context"""
    # Combine retrieved documents
    context = " ".join(retrieved_docs)
    
    # Create input prompt
    prompt = f"Answer the question based on this context: {context} Question: {query}"
    
    # Tokenize input
    inputs = tokenizer.encode(prompt, return_tensors="pt", max_length=512, truncation=True)
    
    # Generate response
    outputs = generator.generate(
        inputs, 
        max_length=150, 
        num_beams=4, 
        temperature=0.7,
        do_sample=True
    )
    
    # Decode response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response


while True:
    # Test complete RAG pipeline
    query = input("enter a query... type /exit to stop.")
    if query == "/exit":
        break
    retrieved_docs, scores = retrieve_documents(query)
    response = generate_response(query, retrieved_docs)

    print(f"Query: {query}")
    print(f"Response: {response}")

