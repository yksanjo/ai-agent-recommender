"""
Data processor for cleaning and enriching use case data.
"""
import json
from pathlib import Path
from typing import List, Dict, Optional


def load_use_cases(file_path: str = "data/use_cases.json") -> List[Dict]:
    """Load use cases from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    # Remove extra whitespace
    text = ' '.join(text.split())
    # Remove markdown formatting
    text = text.replace('**', '').replace('*', '').replace('`', '')
    return text.strip()


def enrich_use_case(use_case: Dict) -> Dict:
    """Enrich use case with additional metadata."""
    enriched = use_case.copy()
    
    # Clean fields
    enriched['use_case'] = clean_text(enriched.get('use_case', ''))
    enriched['description'] = clean_text(enriched.get('description', ''))
    enriched['industry'] = clean_text(enriched.get('industry', ''))
    
    # Create searchable text
    searchable_text = f"{enriched['use_case']} {enriched['description']} {enriched['industry']}"
    enriched['searchable_text'] = searchable_text
    
    # Add complexity estimate (simple heuristic)
    complexity = "Medium"
    desc_lower = enriched['description'].lower()
    if any(word in desc_lower for word in ['simple', 'basic', 'easy']):
        complexity = "Low"
    elif any(word in desc_lower for word in ['complex', 'advanced', 'multi-agent', 'orchestration']):
        complexity = "High"
    enriched['complexity'] = complexity
    
    return enriched


def process_use_cases(input_path: str = "data/use_cases.json", 
                     output_path: str = "data/use_cases_processed.json") -> List[Dict]:
    """Process and enrich all use cases."""
    use_cases = load_use_cases(input_path)
    processed = [enrich_use_case(uc) for uc in use_cases]
    
    # Save processed data
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed, f, indent=2, ensure_ascii=False)
    
    print(f"Processed {len(processed)} use cases")
    return processed


if __name__ == "__main__":
    process_use_cases()

