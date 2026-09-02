<<<<<<< HEAD
import os
from deepface import DeepFace
from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_5gucQk_KZWSVcWnNDHyR2U6Ca4Bfjm7b5iTUzeev7SttFwK7bxeTmiSG5YYGztavcmNqQV")
INDEX_NAME = "reality-key"

def seed_target():
    # Create a local 'targets' folder if it doesn't exist
    if not os.path.exists("targets"):
        os.makedirs("targets")
        print("Created 'targets' folder inside backend/. Please put a test image inside it named 'target1.jpg' and re-run.")
        return

    img_path = "targets/target1.jpg"
    if not os.path.exists(img_path):
        print(f"Error: Could not find {img_path}. Please add a target photo there first!")
        return

    print("Extracting facial vector embedding using DeepFace...")
    embedding = DeepFace.represent(
        img_path=img_path, 
        model_name="Facenet", 
        detector_backend="skip", 
        enforce_detection=False
    )[0]["embedding"]

    print("Connecting to Pinecone index 'reality-key'...")
    index = pc.Index(INDEX_NAME)

    print("Uploading vector signature and metadata to cloud database...")
    index.upsert(
        vectors=[
            {
                "id": "NODE-TARGET-001",
                "values": embedding,
                "metadata": {
                    "name": "Target Subject Alpha",
                    "location": "Global",
                    "occupation": "Classified / Digital Footprint Tracked",
                    "instagram": "https://instagram.com",
                    "twitter": "https://twitter.com",
                    "github": "https://github.com"
                }
            }
        ]
    )
    print("SUCCESS: Target profile successfully indexed into your Pinecone database!")

if __name__ == "__main__":
=======
import os
from deepface import DeepFace
from pinecone import Pinecone

pc = Pinecone(api_key="pcsk_5gucQk_KZWSVcWnNDHyR2U6Ca4Bfjm7b5iTUzeev7SttFwK7bxeTmiSG5YYGztavcmNqQV")
INDEX_NAME = "reality-key"

def seed_target():
    # Create a local 'targets' folder if it doesn't exist
    if not os.path.exists("targets"):
        os.makedirs("targets")
        print("Created 'targets' folder inside backend/. Please put a test image inside it named 'target1.jpg' and re-run.")
        return

    img_path = "targets/target1.jpg"
    if not os.path.exists(img_path):
        print(f"Error: Could not find {img_path}. Please add a target photo there first!")
        return

    print("Extracting facial vector embedding using DeepFace...")
    embedding = DeepFace.represent(
        img_path=img_path, 
        model_name="Facenet", 
        detector_backend="skip", 
        enforce_detection=False
    )[0]["embedding"]

    print("Connecting to Pinecone index 'reality-key'...")
    index = pc.Index(INDEX_NAME)

    print("Uploading vector signature and metadata to cloud database...")
    index.upsert(
        vectors=[
            {
                "id": "NODE-TARGET-001",
                "values": embedding,
                "metadata": {
                    "name": "Target Subject Alpha",
                    "location": "Global",
                    "occupation": "Classified / Digital Footprint Tracked",
                    "instagram": "https://instagram.com",
                    "twitter": "https://twitter.com",
                    "github": "https://github.com"
                }
            }
        ]
    )
    print("SUCCESS: Target profile successfully indexed into your Pinecone database!")

if __name__ == "__main__":
>>>>>>> dd7d5596183c700bca61ca4f8045ca934c859042
    seed_target()