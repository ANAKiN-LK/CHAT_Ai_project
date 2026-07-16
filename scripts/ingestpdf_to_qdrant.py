import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEndpointEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models

load_dotenv()

EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://localhost:8081")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "dummy_token")
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "Chat-AI")

DATA_DIR = Path(__file__).parent.parent / "data"

def ingest_documents():
    print("Loading PDF files...")
    pdf_files = list(DATA_DIR.glob("*.pdf"))
    if not pdf_files:
        print("No PDF files found.")
        return
    print(f"\n พบไฟล์ PDF {len(pdf_files)} ไฟล์:")
    for f in pdf_files:
        print(f"  - {f.name}")
    all_docs = []
    for pdf_path in pdf_files:
        loader = PyPDFLoader(str(pdf_path))
        docs = loader.load()
        for doc in docs:
            doc.metadata["source"] = pdf_path.name
        all_docs.extend(docs)
        print(f" {pdf_path.name}: {len(docs)} หน้า")
    
    print(f"\n รวมทั้งหมด: {len(all_docs)} หน้า")
    print("\nกำลังหั่นข้อความ (Chunking)...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f" ได้ทั้งหมด: {len(chunks)} chunks")
    embeddings = HuggingFaceEndpointEmbeddings(
        model=EMBEDDING_URL,
        huggingfacehub_api_token=EMBEDDING_API_KEY
    )
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
    )
    if client.collection_exists(COLLECTION_NAME):
        print(f"ลบ Collection เดิม '{COLLECTION_NAME}'...")
        client.delete_collection(COLLECTION_NAME)
    print(f" สร้าง Collection '{COLLECTION_NAME}'...")
    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=1024, 
            distance=models.Distance.COSINE
        )
    )
    vector_store = QdrantVectorStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY if QDRANT_API_KEY else None,
        collection_name=COLLECTION_NAME
    )
    print("Documents uploaded successfully.")
    
    test_query = "นโยบายการลา"
    results = vector_store.similarity_search(test_query, k=2)
    
    if results:
        print(f"ค้นหา '{test_query}' พบ {len(results)} ผลลัพธ์")
        for i, doc in enumerate(results):
            print(f"\n   --- ผลลัพธ์ที่ {i+1} ---")
            print(f"   {doc.page_content[:150]}...")
    else:
         print("No results found.")

if __name__ == "__main__":
    ingest_documents()
