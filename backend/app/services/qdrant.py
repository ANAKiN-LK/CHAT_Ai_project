from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from app.core.config import settings


class QdrantService:
    _client: QdrantClient = None
    _embeddings: OpenAIEmbeddings = None
    _vector_store: QdrantVectorStore = None

    @classmethod
    def get_client(cls) -> QdrantClient:
        if cls._client is None:
            cls._client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None,
            )
        return cls._client

    @classmethod
    def get_embeddings(cls) -> OpenAIEmbeddings:
        if cls._embeddings is None:
            cls._embeddings = OpenAIEmbeddings(
                model="intfloat/multilingual-e5-large-instruct",
                base_url=f"{settings.EMBEDDING_URL}/v1",
                api_key=settings.EMBEDDING_API_KEY,
            )
        return cls._embeddings

    @classmethod
    def get_vector_store(cls) -> QdrantVectorStore:
        if cls._vector_store is None:
            cls._vector_store = QdrantVectorStore(
                client=cls.get_client(),
                collection_name=settings.QDRANT_COLLECTION,
                embedding=cls.get_embeddings(),
            )
        return cls._vector_store

    @classmethod
    def get_retriever(cls, k: int = 3):
        return cls.get_vector_store().as_retriever(
            search_type="similarity",
            search_kwargs={"k": k},
        )

    @classmethod
    def check_health(cls) -> dict:
        try:
            client = cls.get_client()
            collections = client.get_collections()
            collection_exists = any(
                c.name == settings.QDRANT_COLLECTION
                for c in collections.collections
            )
            return {
                "status": "connected",
                "collection_exists": collection_exists,
                "collection_name": settings.QDRANT_COLLECTION,
            }
        except Exception as e:
            return {"status": "error", "error": str(e)}


def get_retriever(k: int = 3):
    return QdrantService.get_retriever(k)


def check_qdrant_health():
    return QdrantService.check_health()