"""
RAG retriever for searching and ranking use cases.
"""
from typing import List, Dict, Optional
from langchain.schema import Document
from src.rag.vector_store import UseCaseVectorStore


class UseCaseRetriever:
    """Retriever for use case recommendations."""
    
    def __init__(self, k: int = 5, score_threshold: float = 0.7):
        self.vector_store = UseCaseVectorStore()
        self.k = k
        self.score_threshold = score_threshold
        self.retriever = None
    
    def initialize(self):
        """Initialize the retriever."""
        self.retriever = self.vector_store.get_retriever(
            k=self.k,
            score_threshold=self.score_threshold
        )
    
    def retrieve(self, query: str, k: Optional[int] = None, 
                 filters: Optional[Dict] = None) -> List[Dict]:
        """
        Retrieve relevant use cases based on query.
        
        Args:
            query: User query string
            k: Number of results to return
            filters: Optional filters (industry, framework, etc.)
        
        Returns:
            List of relevant use cases with scores
        """
        if self.retriever is None:
            self.initialize()
        
        # Adjust k if provided
        if k is not None:
            self.retriever.search_kwargs["k"] = k
        
        # Perform search
        results = self.vector_store.search(query, k=k or self.k)
        
        # Apply filters if provided
        if filters:
            results = self._apply_filters(results, filters)
        
        # Format results
        formatted = []
        for result in results:
            formatted.append({
                'use_case': result['metadata'].get('use_case', ''),
                'industry': result['metadata'].get('industry', ''),
                'framework': result['metadata'].get('framework', 'Unknown'),
                'description': result['metadata'].get('description', ''),
                'github_link': result['metadata'].get('github_link', ''),
                'complexity': result['metadata'].get('complexity', 'Medium'),
                'relevance_score': 1.0 - result['score']  # Convert distance to similarity
            })
        
        return formatted
    
    def _apply_filters(self, results: List[Dict], filters: Dict) -> List[Dict]:
        """Apply filters to search results."""
        filtered = []
        for result in results:
            metadata = result['metadata']
            
            # Industry filter
            if 'industry' in filters:
                if filters['industry'].lower() not in metadata.get('industry', '').lower():
                    continue
            
            # Framework filter
            if 'framework' in filters:
                if filters['framework'].lower() != metadata.get('framework', '').lower():
                    continue
            
            # Complexity filter
            if 'complexity' in filters:
                if filters['complexity'].lower() != metadata.get('complexity', '').lower():
                    continue
            
            filtered.append(result)
        
        return filtered
    
    def get_all_industries(self) -> List[str]:
        """Get list of all unique industries."""
        use_cases = self.vector_store.load_use_cases()
        industries = set()
        for uc in use_cases:
            industry = uc.get('industry', '').strip()
            if industry:
                industries.add(industry)
        return sorted(list(industries))
    
    def get_all_frameworks(self) -> List[str]:
        """Get list of all unique frameworks."""
        use_cases = self.vector_store.load_use_cases()
        frameworks = set()
        for uc in use_cases:
            framework = uc.get('framework', '').strip()
            if framework and framework != 'Unknown':
                frameworks.add(framework)
        return sorted(list(frameworks))

