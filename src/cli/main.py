"""
CLI interface for the AI Agent Recommender.
"""
import click
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from typing import List, Dict
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.agent.recommender_agent import create_agent
from src.rag.retriever import UseCaseRetriever

load_dotenv()

console = Console()


class ConversationManager:
    """Manages conversation history for multi-turn conversations."""
    
    def __init__(self):
        self.history = []
    
    def add_message(self, role: str, content: str):
        """Add a message to history."""
        self.history.append({"role": role, "content": content})
    
    def get_history(self):
        """Get conversation history."""
        return self.history
    
    def clear(self):
        """Clear conversation history."""
        self.history = []


def format_recommendations_table(recommendations: List[Dict]) -> Table:
    """Format recommendations as a rich table."""
    table = Table(title="Recommended AI Agent Use Cases", show_header=True, header_style="bold magenta")
    table.add_column("#", style="dim", width=3)
    table.add_column("Use Case", style="cyan", width=30)
    table.add_column("Industry", width=15)
    table.add_column("Framework", width=12)
    table.add_column("Relevance", justify="right", width=10)
    
    for i, rec in enumerate(recommendations, 1):
        relevance = f"{rec.get('relevance_score', 0):.1%}"
        table.add_row(
            str(i),
            rec.get('use_case', 'Unknown'),
            rec.get('industry', 'N/A'),
            rec.get('framework', 'Unknown'),
            relevance
        )
    
    return table


def display_recommendations(recommendations: List[Dict], detailed: bool = False):
    """Display recommendations in a formatted way."""
    if not recommendations:
        console.print("[yellow]No recommendations found. Try refining your query.[/yellow]")
        return
    
    # Show summary table
    console.print(format_recommendations_table(recommendations))
    
    if detailed:
        console.print("\n")
        for i, rec in enumerate(recommendations, 1):
            panel_content = f"""
[bold cyan]{rec.get('use_case', 'Unknown')}[/bold cyan]

[bold]Industry:[/bold] {rec.get('industry', 'N/A')}
[bold]Framework:[/bold] {rec.get('framework', 'Unknown')}
[bold]Complexity:[/bold] {rec.get('complexity', 'Medium')}
[bold]Relevance:[/bold] {rec.get('relevance_score', 0):.1%}

[bold]Description:[/bold]
{rec.get('description', 'N/A')}

[bold]GitHub:[/bold] {rec.get('github_link', 'N/A')}
"""
            console.print(Panel(panel_content, title=f"Recommendation {i}", border_style="blue"))


@click.group()
def cli():
    """AI Agent Recommender - Find the perfect AI agent use case from 500+ projects."""
    pass


@cli.command()
@click.option('--query', '-q', help='Your search query')
@click.option('--industry', '-i', help='Filter by industry')
@click.option('--framework', '-f', help='Filter by framework (CrewAI, AutoGen, LangGraph, etc.)')
@click.option('--max-results', '-n', default=5, help='Maximum number of results')
@click.option('--detailed', '-d', is_flag=True, help='Show detailed information')
@click.option('--model', default='gpt-4-turbo-preview', help='LLM model to use')
def search(query, industry, framework, max_results, detailed, model):
    """Search for AI agent use cases."""
    if not query:
        console.print("[red]Error: --query is required. Use 'recommender search --help' for usage.[/red]")
        return
    
    console.print(f"[bold green]Searching for:[/bold green] {query}")
    if industry:
        console.print(f"[dim]Industry filter:[/dim] {industry}")
    if framework:
        console.print(f"[dim]Framework filter:[/dim] {framework}")
    console.print()
    
    # Use direct retriever for simple searches
    retriever = UseCaseRetriever()
    retriever.initialize()
    
    filters = {}
    if industry:
        filters['industry'] = industry
    if framework:
        filters['framework'] = framework
    
    recommendations = retriever.retrieve(query, k=max_results, filters=filters)
    display_recommendations(recommendations, detailed=detailed)


@cli.command()
@click.option('--model', default='gpt-4-turbo-preview', help='LLM model to use')
def interactive(model):
    """Start interactive mode for conversational queries."""
    console.print(Panel.fit(
        "[bold cyan]AI Agent Recommender[/bold cyan]\n"
        "Ask me anything about AI agent use cases!\n"
        "Type 'exit' or 'quit' to leave.\n"
        "Type 'clear' to clear conversation history.",
        title="Welcome",
        border_style="green"
    ))
    
    agent = create_agent(model_name=model)
    conversation = ConversationManager()
    
    while True:
        try:
            query = click.prompt("\n[bold]Your query[/bold]", type=str)
            
            if query.lower() in ['exit', 'quit', 'q']:
                console.print("[yellow]Goodbye![/yellow]")
                break
            
            if query.lower() == 'clear':
                conversation.clear()
                console.print("[green]Conversation history cleared.[/green]")
                continue
            
            if not query.strip():
                continue
            
            console.print("[dim]Thinking...[/dim]")
            
            # Get recommendations using agent
            response = agent.recommend(query, conversation_history=conversation.get_history())
            
            # Display response
            console.print(Panel(Markdown(response), title="Recommendations", border_style="blue"))
            
            # Update conversation history
            conversation.add_message("user", query)
            conversation.add_message("assistant", response)
            
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")


@cli.command()
def industries():
    """List all available industries."""
    retriever = UseCaseRetriever()
    industries_list = retriever.get_all_industries()
    
    console.print(f"[bold]Available Industries ({len(industries_list)}):[/bold]\n")
    for industry in industries_list:
        console.print(f"  • {industry}")


@cli.command()
def frameworks():
    """List all available frameworks."""
    retriever = UseCaseRetriever()
    frameworks_list = retriever.get_all_frameworks()
    
    console.print(f"[bold]Available Frameworks ({len(frameworks_list)}):[/bold]\n")
    for framework in frameworks_list:
        console.print(f"  • {framework}")


@cli.command()
@click.option('--query', '-q', required=True, help='Search query')
@click.option('--export-format', type=click.Choice(['json', 'csv', 'markdown']), 
              default='json', help='Format for exporting recommendations')
@click.option('--export-path', default='recommendations.json', 
              help='Path to save exported recommendations')
@click.option('--industry', '-i', help='Filter by industry')
@click.option('--framework', '-f', help='Filter by framework')
@click.option('--max-results', '-n', default=5, help='Maximum number of results')
def export(query, export_format, export_path, industry, framework, max_results):
    """Search and export recommendations to a file."""
    console.print(f"[bold green]Searching and exporting:[/bold green] {query}")
    
    retriever = UseCaseRetriever()
    retriever.initialize()
    
    filters = {}
    if industry:
        filters['industry'] = industry
    if framework:
        filters['framework'] = framework
    
    recommendations = retriever.retrieve(query, k=max_results, filters=filters)
    
    if not recommendations:
        console.print("[yellow]No recommendations found.[/yellow]")
        return
    
    from src.utils.helpers import export_recommendations
    export_recommendations(recommendations, export_path, export_format)
    console.print(f"[green]Exported {len(recommendations)} recommendations to {export_path}[/green]")


@cli.command()
def setup():
    """Set up the system by scraping data and building vector store."""
    console.print("[bold]Setting up AI Agent Recommender...[/bold]\n")
    
    # Step 1: Scrape data
    console.print("[yellow]Step 1:[/yellow] Scraping repository data...")
    try:
        from src.data.scraper import main as scrape_main
        scrape_main()
        console.print("[green]✓[/green] Data scraped successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Error scraping data: {e}")
        return
    
    # Step 2: Process data
    console.print("[yellow]Step 2:[/yellow] Processing data...")
    try:
        from src.data.processor import process_use_cases
        process_use_cases()
        console.print("[green]✓[/green] Data processed successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Error processing data: {e}")
        return
    
    # Step 3: Build vector store
    console.print("[yellow]Step 3:[/yellow] Building vector store...")
    try:
        from src.rag.vector_store import main as vector_main
        vector_main()
        console.print("[green]✓[/green] Vector store built successfully")
    except Exception as e:
        console.print(f"[red]✗[/red] Error building vector store: {e}")
        return
    
    console.print("\n[bold green]Setup complete![/bold green] You can now use the recommender.")


if __name__ == "__main__":
    cli()

