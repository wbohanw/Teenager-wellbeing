from langchain.embeddings.openai import OpenAIEmbeddings
from pinecone import Pinecone as PineconeClient, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
import pandas as pd
from pinecone import Pinecone, ServerlessSpec

load_dotenv()

cloud = os.environ.get('PINECONE_CLOUD') or 'aws'
region = os.environ.get('PINECONE_REGION') or 'us-east-1'
OPENAI_API_KEY = os.getenv("AIHUBMIX_API_KEY")


embed_model = "text-embedding-ada-002"

def create_vectorstore(path):
    pc = Pinecone(api_key="6d5cdd0a-90b1-454c-bb02-57c80dac0797")

    pinecone_index_name = "newadvice"

    embed_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, base_url="https://aihubmix.com/v1")
    if pinecone_index_name not in pc.list_indexes().names():
        pc.create_index(
            name=pinecone_index_name, 
            dimension=1536, 
            metric='cosine',
            spec=ServerlessSpec(
                cloud='aws',
                region='us-east-1'
            )
        )
    index = pc.Index(pinecone_index_name)
    advices = pd.read_csv(path)
    for i, row in advices.iterrows():
        advice = row['Advice']
        embedding = embed_model.embed_query(advice)
        metadata = {'text': advice}
        index.upsert(vectors=[(str(i), embedding, metadata)])

    print(f"Added {len(advices)} advice documents to the vector store.")

    return index

def search_vectorstore(query, vectorstore, k=3):
    results = vectorstore.similarity_search_with_score(query, k=k)
    return results

if __name__ == "__main__":
    vectorstore_instance = create_vectorstore("Wellbeing RAG/CBT_Logic/advice_sample.csv")
    
    