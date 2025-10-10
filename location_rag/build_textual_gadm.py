from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from torch import float16
import pandas as pd
from transformers import AutoModelForCausalLM, AutoTokenizer
from outformer import Jsonformer, highlight_values

# Load embedding model
encoder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Sample knowledge base documents
documents = pd.read_csv("gadm_test.csv")["text"]
print("loaded documents")

# Generate embeddings
doc_embeddings = encoder.encode(
    documents,
    show_progress_bar=True,
)
print(f"Created {len(doc_embeddings)} document embeddings")

# Create FAISS index for fast retrieval
dimension = doc_embeddings.shape[1]
index = faiss.IndexFlatIP(dimension)  # Inner product similarity

# Add embeddings to index
index.add(doc_embeddings.astype("float32"))


def retrieve_documents(query, top_k=3):
    """Retrieve most relevant documents for query"""
    query_embedding = encoder.encode([query])

    # Search index
    scores, indices = index.search(query_embedding.astype("float32"), top_k)

    # Return relevant documents
    retrieved_docs = [documents[i] for i in indices[0]]
    return retrieved_docs, scores[0]


# Load generation model
model_name = "mistralai/Mixtral-8x7B-Instruct-v0.1"
model = AutoModelForCausalLM.from_pretrained(
    model_name, device_map="balanced", top_k=10, do_sample=True, torch_dtype=float16
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

jsonformer = Jsonformer(model, tokenizer, max_tokens_string=200, debug=False)

gid_schema = {
    "type": "object",
    "properties": {
        "gids": {
            "type": "array",
            "minItems": 1,
            "description": """Return a list of GIDs that represent the region or area or city mentioned in the prompt sentence. 

    Examples:

    QUERY: "A flood had hit Tifra and Tichi in the past week" 
    Output: ["DZA.8.44_1", "DZA.8.43_1"]
    
    QUERY: "Rescue teams were heading to the Midlands in Zimbabwe"
    Output: ["ZWE.10_1"]

    If the area overlaps several GIDs, mention all GIDs. Must be a valid GID.
    """,
            # Examples of valid GIDs: ZWE.10.13_2, or AFG.1_1, or DZA.6.57_1, Z03.28_1, or even just ALB.
            "items": {
                "type": "string",
            },
        }
    },
}


def generate_response(query, retrieved_docs):
    """Generate response using retrieved context"""
    # Combine retrieved documents
    print("retrieved_docs")
    print(retrieved_docs)
    context = " ".join(retrieved_docs)

    # Create input prompt
    prompt = f"Some information on locations: {context}.\n Now, respond to this query with a comma-separated valid Python-type list of GIDs with no duplicates.\n QUERY: {query}"

    print("prompt:")
    print(prompt)
    print()
    # Tokenize input
    inputs = tokenizer.encode(
        prompt, return_tensors="pt", max_length=512, truncation=True
    )

    # Generate response
    outputs = model.generate(
        inputs, max_new_tokens=150, num_beams=4, temperature=0.7, do_sample=True
    )

    # Decode response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # respond with outformer
    generated_data = jsonformer.generate(
        schema=gid_schema, prompt=prompt, temperature=0.25, max_attempts=10
    )

    highlight_values(generated_data)

    return response


while True:
    # Test complete RAG pipeline
    query = input("enter a query... type /exit to stop: ")
    if query == "/exit":
        break
    retrieved_docs, scores = retrieve_documents(query)
    response = generate_response(query, retrieved_docs)

    print("------------")
    print(f"Query: {query}")
    print(f"Response: {response}")
    print("------------")
