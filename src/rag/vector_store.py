"""
Vector store setup using ChromaDB for use case embeddings.
"""
import os
import json
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
from chromadb.config import Settings
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()


class UseCaseVectorStore:
    """Manages vector store for use case embeddings."""
    
    def __init__(self, persist_directory: str = "./data/embeddings", 
                 collection_name: str = "use_cases"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = None
        
    def load_use_cases(self, file_path: str = "data/use_cases.json") -> List[Dict]:
        """Load use cases from JSON file."""
        # Try processed first, then fallback to raw
        processed_path = file_path.replace('.json', '_processed.json')
        if Path(processed_path).exists():
            file_path = processed_path
        
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_vector_store(self, use_cases: Optional[List[Dict]] = None):
        """Create or load vector store from use cases."""
        if use_cases is None:
            use_cases = self.load_use_cases()
        
        # Prepare documents and metadata
        documents = []
        metadatas = []
        ids = []
        
        for i, use_case in enumerate(use_cases):
            # Create document text
            doc_text = f"""
            Use Case: {use_case.get('use_case', '')}
            Industry: {use_case.get('industry', '')}
            Description: {use_case.get('description', '')}
            Framework: {use_case.get('framework', 'Unknown')}
            Complexity: {use_case.get('complexity', 'Medium')}
            """
            
            documents.append(doc_text.strip())
            
            # Create metadata
            metadata = {
                'use_case': use_case.get('use_case', ''),
                'industry': use_case.get('industry', ''),
                'framework': use_case.get('framework', 'Unknown'),
                'complexity': use_case.get('complexity', 'Medium'),
                'github_link': use_case.get('github_link', ''),
                'description': use_case.get('description', '')[:500]  # Limit length
            }
            metadatas.append(metadata)
            ids.append(f"use_case_{i}")
        
        # Create vector store
        print(f"Creating vector store with {len(documents)} documents...")
        self.vectorstore = Chroma.from_texts(
            texts=documents,
            metadatas=metadatas,
            ids=ids,
            embedding=self.embeddings,
            persist_directory=self.persist_directory,
            collection_name=self.collection_name
        )
        
        print(f"Vector store created and persisted to {self.persist_directory}")
        return self.vectorstore
    
    def load_vector_store(self):
        """Load existing vector store."""
        if Path(self.persist_directory).exists():
            print(f"Loading existing vector store from {self.persist_directory}...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings,
                collection_name=self.collection_name
            )
            print("Vector store loaded successfully")
            return self.vectorstore
        else:
            print("No existing vector store found. Creating new one...")
            return self.create_vector_store()
    
    def get_retriever(self, k: int = 5, score_threshold: Optional[float] = None):
        """Get a retriever from the vector store."""
        if self.vectorstore is None:
            self.load_vector_store()
        
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": k}
        )
        
        if score_threshold:
            retriever.search_kwargs["score_threshold"] = score_threshold
        
        return retriever
    
    def search(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar use cases."""
        if self.vectorstore is None:
            self.load_vector_store()
        
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        
        formatted_results = []
        for doc, score in results:
            formatted_results.append({
                'content': doc.page_content,
                'metadata': doc.metadata,
                'score': float(score)
            })
        
        return formatted_results


def main():
    """Main function to build vector store."""
    # First, ensure we have processed data
    from src.data.processor import process_use_cases
    print("Processing use cases...")
    process_use_cases()
    
    # Create vector store
    print("\nBuilding vector store...")
    vector_store = UseCaseVectorStore()
    vector_store.create_vector_store()
    print("Vector store built successfully!")


if __name__ == "__main__":
    main()

