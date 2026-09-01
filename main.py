from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from deepface import DeepFace
from pinecone import Pinecone

app = FastAPI()

# Enable CORS for your Next.js UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Pinecone Client with your key and index
pc = Pinecone(api_key="pcsk_5gucQk_KZWSVcWnNDHyR2U6Ca4Bfjm7b5iTUzeev7SttFwK7bxeTmiSG5YYGztavcmNqQV")
INDEX_NAME = "reality-key"

@app.post("/search")
async def search_target(
    file: UploadFile = File(...),
    location: str = Form(...)
):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # 1. Extract facial vector embedding using DeepFace with detector_backend="skip"
        embedding_objs = DeepFace.represent(
            img_path=temp_file_path, 
            model_name="Facenet", 
            detector_backend="skip", 
            enforce_detection=False
        )
        target_vector = embedding_objs[0]["embedding"]

        # 2. Connect to Pinecone and query the vector database
        index = pc.Index(INDEX_NAME)
        
        # Build metadata filter based on user's selected location jurisdiction node
        filter_query = {}
        if location and "Global" not in location:
            filter_query = {"location": {"$eq": location}}

        query_response = index.query(
            vector=target_vector,
            top_k=3,
            include_metadata=True,
            filter=filter_query if filter_query else None
        )

        matches = query_response.get("matches", [])
        
        formatted_results = []
        for match in matches:
            formatted_results.append({
                "id": match["id"],
                "score": match["score"],
                "metadata": match.get("metadata", {})
            })

        # Fallback if database index has no records yet
        if not formatted_results:
            formatted_results = [{
                "id": "NODE-ZERO-MATCH",
                "score": 0.0,
                "metadata": {
                    "name": "No Vector Match Found",
                    "location": location,
                    "occupation": "Target footprint clear in active sector",
                    "avatar": "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=500"
                }
            }]

    except Exception as e:
        print(f"Neural processing exception: {e}")
        formatted_results = []

    # Clean up temporary uploaded file
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)

    return {"results": formatted_results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)