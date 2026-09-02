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

# Root route for Render health check (Required)
@app.get("/")
def read_root():
    return {"status": "online", "message": "Reality Backend API is running"}

# Initialize Pinecone Client via environment variables set in Render
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY", "")
INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME", "reality-key")

pc = Pinecone(api_key=PINECONE_API_KEY) if PINECONE_API_KEY else None

@app.post("/search")
async def search_target(
    file: UploadFile = File(...),
    location: str = Form(...)
):
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    formatted_results = []

    try:
        # 1. Extract facial vector embedding using DeepFace
        embedding_objs = DeepFace.represent(
            img_path=temp_file_path, 
            model_name="Facenet", 
            detector_backend="skip", 
            enforce_detection=False
        )
        target_vector = embedding_objs[0]["embedding"]

        # 2. Connect to Pinecone and query the vector database
        if pc:
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
    finally:
        # Clean up temporary uploaded file safely
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

    return {"results": formatted_results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)