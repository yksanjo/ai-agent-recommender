"""
Scraper to extract use cases from the 500 AI Agents Projects repository.
"""
import requests
import json
import re
from pathlib import Path
from typing import List, Dict
from bs4 import BeautifulSoup
import markdown


def fetch_readme() -> str:
    """Fetch the README.md from the GitHub repository."""
    url = "https://raw.githubusercontent.com/ashishpatel26/500-AI-Agents-Projects/main/README.md"
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Error fetching README: {e}")
        raise


def parse_markdown_table(markdown_text: str) -> List[Dict]:
    """Parse markdown tables to extract use case data."""
    use_cases = []
    
    # Find the Use Case Table section
    lines = markdown_text.split('\n')
    in_table = False
    table_lines = []
    
    for i, line in enumerate(lines):
        if '| Use Case' in line and 'Industry' in line:
            in_table = True
            # Skip header separator line
            continue
        if in_table:
            if line.strip().startswith('|') and '---' not in line:
                table_lines.append(line)
            elif line.strip() == '' and table_lines:
                # End of table
                break
    
    # Parse table rows
    for line in table_lines:
        if not line.strip() or '---' in line:
            continue
        
        # Split by | and clean
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) >= 4:
            use_case = parts[0].replace('**', '').strip()
            industry = parts[1].strip()
            description = parts[2].strip()
            github_link = parts[3].strip()
            
            # Extract actual GitHub URL from markdown link
            github_url = None
            if '[' in github_link and ']' in github_link:
                match = re.search(r'\(([^)]+)\)', github_link)
                if match:
                    github_url = match.group(1)
            elif github_link.startswith('http'):
                github_url = github_link
            
            # Determine framework from use case or description
            framework = "Unknown"
            if 'crewai' in use_case.lower() or 'crewai' in description.lower():
                framework = "CrewAI"
            elif 'autogen' in use_case.lower() or 'autogen' in description.lower():
                framework = "AutoGen"
            elif 'langgraph' in use_case.lower() or 'langgraph' in description.lower():
                framework = "LangGraph"
            elif 'agno' in use_case.lower() or 'agno' in description.lower():
                framework = "Agno"
            
            use_cases.append({
                'use_case': use_case,
                'industry': industry,
                'description': description,
                'github_link': github_url or github_link,
                'framework': framework
            })
    
    return use_cases


def extract_framework_section(markdown_text: str, framework_name: str) -> List[Dict]:
    """Extract use cases from framework-specific sections."""
    use_cases = []
    
    # Find framework section
    pattern = rf'##.*{framework_name}.*UseCase'
    lines = markdown_text.split('\n')
    in_section = False
    table_lines = []
    
    for i, line in enumerate(lines):
        if re.search(pattern, line, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            if line.strip().startswith('|') and '---' not in line:
                table_lines.append(line)
            elif line.strip().startswith('##') and table_lines:
                # Next section, stop
                break
    
    # Parse table rows (similar to main table)
    for line in table_lines:
        if not line.strip() or '---' in line:
            continue
        
        parts = [p.strip() for p in line.split('|') if p.strip()]
        if len(parts) >= 3:
            use_case = parts[0].replace('**', '').replace('🤖', '').replace('🧠', '').strip()
            industry = parts[1].strip() if len(parts) > 1 else "AI / Workflow"
            description = parts[2].strip() if len(parts) > 2 else ""
            github_link = parts[3].strip() if len(parts) > 3 else ""
            
            github_url = None
            if '[' in github_link and ']' in github_link:
                match = re.search(r'\(([^)]+)\)', github_link)
                if match:
                    github_url = match.group(1)
            elif github_link.startswith('http'):
                github_url = github_link
            
            use_cases.append({
                'use_case': use_case,
                'industry': industry,
                'description': description,
                'github_link': github_url or github_link,
                'framework': framework_name
            })
    
    return use_cases


def scrape_all_use_cases() -> List[Dict]:
    """Scrape all use cases from the repository."""
    print("Fetching README from repository...")
    markdown_text = fetch_readme()
    
    print("Parsing main use case table...")
    use_cases = parse_markdown_table(markdown_text)
    
    # Extract framework-specific sections
    frameworks = ['CrewAI', 'AutoGen', 'LangGraph', 'Agno']
    for framework in frameworks:
        print(f"Parsing {framework} use cases...")
        framework_cases = extract_framework_section(markdown_text, framework)
        use_cases.extend(framework_cases)
    
    # Remove duplicates based on use_case name
    seen = set()
    unique_cases = []
    for case in use_cases:
        key = case['use_case'].lower()
        if key not in seen:
            seen.add(key)
            unique_cases.append(case)
    
    print(f"Found {len(unique_cases)} unique use cases")
    return unique_cases


def save_use_cases(use_cases: List[Dict], output_path: str = "data/use_cases.json"):
    """Save use cases to JSON file."""
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(use_cases, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(use_cases)} use cases to {output_path}")


def main():
    """Main function to scrape and save use cases."""
    use_cases = scrape_all_use_cases()
    save_use_cases(use_cases)


if __name__ == "__main__":
    main()

