import os 
import time
from langchain_chroma import Chroma 
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001", 
    google_api_key="AIzaSyApebX5V5U236iEH8wq0wBFWTqsla4-J2A"
)

loader = DirectoryLoader("./AgricultureNB_LM")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
docs = text_splitter.split_documents(docs)

# Process in smaller batches with delays
def create_vectorstore_with_batches(docs, embeddings, batch_size=10, delay=2):
    """Create vectorstore in batches to avoid rate limits"""
    
    vectorstore = None
    
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        print(f"Processing batch {i//batch_size + 1}: documents {i+1} to {min(i+batch_size, len(docs))}")
        
        try:
            if vectorstore is None:
                # Create initial vectorstore
                vectorstore = Chroma.from_documents(
                    documents=batch,
                    embedding=embeddings,
                    persist_directory="./agriculture_chromaV2",
                    collection_name="agriculture",
                )
            else:
                # Add to existing vectorstore
                vectorstore.add_documents(batch)
            
            if i + batch_size < len(docs):  # Don't delay after the last batch
                print(f"Waiting {delay} seconds before next batch...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"Error processing batch {i//batch_size + 1}: {e}")
            if "quota" in str(e).lower() or "429" in str(e):
                print("Rate limit hit. Waiting longer...")
                time.sleep(10)
                continue
    
    return vectorstore

# Process with batches
vectorstore = create_vectorstore_with_batches(docs, embeddings)
print(f"Successfully created vector store with {len(docs)} documents")