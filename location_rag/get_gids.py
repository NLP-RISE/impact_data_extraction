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
documents = pd.read_csv("data/gadm_world_textual.csv")["text"]
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
        "location_information": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "properties": {
                    "location_name": {
                        "type": "string",
                        "description": "The name of the location, as mentioned in the text exactly",
                    },
                    "GID": {
                        "type": "array",
                        "minItems": 1,
                        "description": "A list containing one or more GIDs to describe this location extracted from the sentence.",
                    },
                },
            },
        },
    },
}


def generate_response(query, retrieved_docs):
    """Generate response using retrieved context"""
    # Combine retrieved documents
    print("retrieved_docs")
    print(retrieved_docs)
    context = " ".join(retrieved_docs).strip()

    # Create input prompt
    # Make example more advanced soon
    prompt = f"""You will be given a passage with information about different locations and their special ID code (called 'GID'). As input, you will take in one or more location names or sometimes a sentence describing the impacts of some natural disaster on human societies in one or more locations. Your task is to extract each location name and find the best GID that describes it based on the CONTEXT.
    
    Examples of successful output: 
    
    QUERY: "due to the heatwave, two casualties were recorded in Nothern Togo" 
    OUTPUT: {{
        "location_information": [{{"location_name": "Nothern Togo", "GID": ["TGO"]}}] 
    }}

    QUERY: "two injuries were recorded in Paris, 3 more in the Pays de la Loire region" 
    OUTPUT: {{
        "location_information": [
                {{"location_name": "Paris", "GID": ["FRA.8.3_1"]}}, 
                {{"location_name": "Pays de la Loire", "GID": ["FRA.12_1"]}}
                                ] 
    }}

    
    CONTEXT: {context}\n
    QUERY: {query}
    """

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
