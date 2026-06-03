import os
import json
import pickle
import re
import numpy as np
from pypdf import PdfReader
import faiss
from sentence_transformers import SentenceTransformer

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore", "faiss_index")

# Ensure index folder exists
os.makedirs(VECTORSTORE_DIR, exist_ok=True)

class Ingestor:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        print("Loading sentence-transformers model...")
        self.model = SentenceTransformer(model_name)
        print("Model loaded successfully.")

    def chunk_text(self, text, source_name):
        """
        Chunks text documents line-by-line or paragraph-by-paragraph to 
        preserve semantic context of specific sections/bullet points.
        """
        chunks = []
        
        # Split by double newlines or single newlines depending on text structure
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            # Skip page headers or titles
            if line.isupper() and len(line) < 50:
                continue
            if len(line) > 20:
                chunks.append({
                    "content": line,
                    "source": source_name
                })
        return chunks

    def load_pdf(self, file_path):
        text = ""
        try:
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
        return text

    def chunk_pdf(self, text, source_name):
        """
        PDF chunking splits by double newline or policy blocks.
        """
        chunks = []
        # Split by double newlines (paragraphs)
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        for p in paragraphs:
            # Clean newlines inside the paragraph to make it a single line block
            cleaned = re.sub(r'\s+', ' ', p)
            if len(cleaned) > 30:
                chunks.append({
                    "content": cleaned,
                    "source": source_name
                })
        return chunks

    def load_txt(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            return ""

    def load_json(self, file_path):
        chunks = []
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            note = data.get("note", "")
            for room in data.get("room_types", []):
                content = (
                    f"Room Type: {room.get('type')}. "
                    f"Located on floors: {room.get('floor')}. "
                    f"Features: {', '.join(room.get('features', []))}. "
                    f"{note}"
                )
                chunks.append({
                    "content": content,
                    "source": os.path.basename(file_path)
                })
        except Exception as e:
            print(f"Error reading JSON {file_path}: {e}")
        return chunks

    def ingest_all(self):
        all_chunks = []
        
        # 1. Amenities TXT
        amenities_path = os.path.join(DATA_DIR, "amenities.txt")
        if os.path.exists(amenities_path):
            text = self.load_txt(amenities_path)
            chunks = self.chunk_text(text, "amenities.txt")
            all_chunks.extend(chunks)
            print(f"Loaded {len(chunks)} chunks from amenities.txt")
            
        # 2. Hotel Policies PDF
        policies_path = os.path.join(DATA_DIR, "hotel_policies.pdf")
        if os.path.exists(policies_path):
            text = self.load_pdf(policies_path)
            chunks = self.chunk_pdf(text, "hotel_policies.pdf")
            all_chunks.extend(chunks)
            print(f"Loaded {len(chunks)} chunks from hotel_policies.pdf")
            
        # 3. Room Info JSON
        room_info_path = os.path.join(DATA_DIR, "room_info.json")
        if os.path.exists(room_info_path):
            chunks = self.load_json(room_info_path)
            all_chunks.extend(chunks)
            print(f"Loaded {len(chunks)} chunks from room_info.json")

        if not all_chunks:
            print("No data found to index. Make sure you run data generation first.")
            return False

        # Create embeddings
        print(f"Encoding {len(all_chunks)} chunks...")
        texts = [c["content"] for c in all_chunks]
        embeddings = self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
        
        # FAISS Index
        dimension = embeddings.shape[1]
        
        # We normalize embeddings to use InnerProduct (cosine similarity)
        faiss.normalize_L2(embeddings)
        index = faiss.IndexFlatIP(dimension)
        index.add(embeddings)
        
        # Persist Index
        faiss.write_index(index, os.path.join(VECTORSTORE_DIR, "index.faiss"))
        
        # Persist metadata chunks
        with open(os.path.join(VECTORSTORE_DIR, "metadata.pkl"), "wb") as f:
            pickle.dump(all_chunks, f)
            
        print(f"FAISS index built and saved with {index.ntotal} vectors to {VECTORSTORE_DIR}")
        return True

if __name__ == "__main__":
    ingestor = Ingestor()
    ingestor.ingest_all()
