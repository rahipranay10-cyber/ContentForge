from app.services.embedding_service import generate_embedding


text = "JWT authentication for an ecommerce backend"

embedding = generate_embedding(text)

print("Embedding dimension:", len(embedding))
print("First 5 values:", embedding[:5])