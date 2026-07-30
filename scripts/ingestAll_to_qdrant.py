import os
import sys
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
from langchain_community.document_loaders import (
    PyPDFLoader,
    CSVLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http import models

SUPPORTED_EXTENSIONS = [".pdf", ".csv", ".txt", ".docx"]

load_dotenv()

EMBEDDING_URL = os.getenv("EMBEDDING_URL", "http://143.198.34.29:8081")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "dummy_token")
QDRANT_URL = os.getenv("QDRANT_URL", "http://143.198.34.29:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "ca0a9feebc24ee1915d7bc1b585627efb9bb30ffebfd34ea8a352522d250614b")
COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "Chat-AI")

DATA_DIR = Path(__file__).parent.parent / "data"

def load_file(file_path: Path) -> List[Document]:
    extension = file_path.suffix.lower()
    docs = []
    try:
        if extension == ".pdf":
            loader = PyPDFLoader(str(file_path))
            docs = loader.load()
            
        elif extension == ".csv":
            loader = CSVLoader(
                file_path=str(file_path),
                encoding="utf-8"
            )
            docs = loader.load()
            
        elif extension == ".txt":
            loader = TextLoader(
                file_path=str(file_path),
                encoding="utf-8"
            )
            docs = loader.load()
            
        elif extension == ".docx":
            loader = Docx2txtLoader(str(file_path))
            docs = loader.load()
            
        else:
            print(f"ไม่รองรับไฟล์ประเภท: {extension}")
            return []
            
    except Exception as e:
        print(f"Error loading {file_path.name}: {e}")
        return []

    for doc in docs:
        doc.metadata["source"] = file_path.name
        doc.metadata["file_type"] = extension
        
    return docs

def ingest_documents():
    print(f"รองรับไฟล์: {', '.join(SUPPORTED_EXTENSIONS)}")
   
    all_files = []
    for ext in SUPPORTED_EXTENSIONS:
        all_files.extend(DATA_DIR.glob(f"*{ext}"))
    
    if not all_files:
        print(f"\nไม่พบไฟล์ใน {DATA_DIR}")
        print(f"กรุณาใส่ไฟล์ประเภท: {', '.join(SUPPORTED_EXTENSIONS)}")
        return
    print("\nพบไฟล์")
    files_by_type = {}
    for f in all_files:
        ext = f.suffix.lower()
        if ext not in files_by_type:
            files_by_type[ext] = []
        files_by_type[ext].append(f)
    
    print(f"\nพบไฟล์ทั้งหมด {len(all_files)} ไฟล์:")
    for ext, files in files_by_type.items():
        print(f"\n {ext.upper()} ({len(files)} ไฟล์):")
        for f in files:
            print(f"      - {f.name}")

    all_docs = []
    for file_path in all_files:
        docs = load_file(file_path)
        if docs:
            all_docs.extend(docs)
            if file_path.suffix.lower() == ".pdf":
                print(f"  {file_path.name}: {len(docs)} หน้า")
            elif file_path.suffix.lower() == ".csv":
                print(f" {file_path.name}: {len(docs)} แถว")
            else:
                print(f" {file_path.name}: {len(docs)} เอกสาร")
    
    print(f"\n  รวมทั้งหมด: {len(all_docs)} เอกสาร")
  
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(all_docs)
    print(f"  ได้ทั้งหมด: {len(chunks)} chunks")
 
    embeddings = OpenAIEmbeddings(
        model="intfloat/multilingual-e5-large-instruct",
        base_url=f"{EMBEDDING_URL}/v1",
        api_key=EMBEDDING_API_KEY,
)
    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY if QDRANT_API_KEY else None
    )
    if client.collection_exists(COLLECTION_NAME):
        print(f"  ลบ Collection เดิม '{COLLECTION_NAME}'...")
        client.delete_collection(COLLECTION_NAME)
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
    test_query = "นโยบายการลา"
    results = vector_store.similarity_search(test_query, k=2)
    
    if results:
        print(f" ค้นหา '{test_query}' พบ {len(results)} ผลลัพธ์")
        for i, doc in enumerate(results):
            print(f"\n   --- ผลลัพธ์ที่ {i+1} ---")
            print(f"   {doc.page_content[:150]}...")
    else:
        print("ไม่พบผลลัพธ์")
    
if __name__ == "__main__":
    ingest_documents()