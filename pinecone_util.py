from pinecone import ServerlessSpec, Pinecone

import uuid

class PineConeUtil:

    def __init__(self):
        # Connect to Pinecone vector DB
        pinecone_api_key = "pclocal"
        pinecone_host = "http://localhost:5080"
        self.pc = Pinecone(
            api_key=pinecone_api_key,
            host=pinecone_host
        )

        # Init index if not exists
        index_name = "news-index"
        # embeddings vectors wil be generated via OpenAI 'text-embedding-ada-002', dimension there is 1536
        known_indexes = self.pc.list_indexes()
        known_indexes_names = [idx.name for idx in known_indexes]
        if index_name not in known_indexes_names:
            self.pc.create_index(
                index_name,
                dimension=1536,
                vector_type="dense",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
                deletion_protection="disabled",
                tags={"environment": "development"})
        else:
            for idx in known_indexes:
                if idx.name == index_name:
                    self.index = self.pc.Index(index_name, "http://" + idx.host)

    def insert_new_vectors(self, vectors, metadata):
        pc_vectors = [
            {
                "id": str(uuid.uuid4()),
                "values": vectors,
                "metadata": metadata
            }
        ]
        self.index.upsert(vectors=pc_vectors)

    def query_index(self, query_vector):
        result = self.index.query(vector=query_vector, top_k=3, include_metadata=True)
        if len(result["matches"]) == 0:
            return "no matches"
        return result["matches"]
