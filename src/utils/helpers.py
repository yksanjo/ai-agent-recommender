"""
Helper utility functions.
"""
import json
from typing import List, Dict, Optional
from pathlib import Path


def export_recommendations(recommendations: List[Dict], output_path: str, format: str = "json"):
    """
    Export recommendations to a file.
    
    Args:
        recommendations: List of recommendation dictionaries
        output_path: Path to save the file
        format: Export format ('json', 'csv', 'markdown')
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    if format == "json":
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(recommendations, f, indent=2, ensure_ascii=False)
    
    elif format == "csv":
        import csv
        if recommendations:
            fieldnames = recommendations[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(recommendations)
    
    elif format == "markdown":
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("# AI Agent Recommendations\n\n")
            for i, rec in enumerate(recommendations, 1):
                f.write(f"## {i}. {rec.get('use_case', 'Unknown')}\n\n")
                f.write(f"- **Industry:** {rec.get('industry', 'N/A')}\n")
                f.write(f"- **Framework:** {rec.get('framework', 'Unknown')}\n")
                f.write(f"- **Complexity:** {rec.get('complexity', 'Medium')}\n")
                f.write(f"- **Relevance:** {rec.get('relevance_score', 0):.1%}\n")
                f.write(f"- **Description:** {rec.get('description', 'N/A')}\n")
                if rec.get('github_link'):
                    f.write(f"- **GitHub:** {rec.get('github_link')}\n")
                f.write("\n")
    
    print(f"Exported {len(recommendations)} recommendations to {output_path}")


def validate_environment():
    """Validate that required environment variables are set."""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment. "
            "Please set it in your .env file or environment variables."
        )
    
    return True

