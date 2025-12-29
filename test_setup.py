#!/usr/bin/env python3
"""
Simple test script to verify the setup is working.
"""
import os
import sys
from pathlib import Path

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    try:
        from src.data.scraper import scrape_all_use_cases
        from src.data.processor import process_use_cases
        from src.rag.vector_store import UseCaseVectorStore
        from src.rag.retriever import UseCaseRetriever
        from src.agent.recommender_agent import create_agent
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_data_files():
    """Test that data files exist."""
    print("\nTesting data files...")
    data_file = Path("data/use_cases.json")
    if data_file.exists():
        print(f"✓ Found {data_file}")
        return True
    else:
        print(f"✗ {data_file} not found. Run 'python -m src.cli.main setup' first.")
        return False

def test_env():
    """Test that environment variables are set."""
    print("\nTesting environment...")
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print("✓ OPENAI_API_KEY is set")
        return True
    else:
        print("✗ OPENAI_API_KEY not found. Please set it in .env file.")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("AI Agent Recommender - Setup Verification")
    print("=" * 50)
    
    results = []
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Environment", test_env()))
    
    print("\n" + "=" * 50)
    print("Summary:")
    print("=" * 50)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name}: {status}")
        if not passed:
            all_passed = False
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to use the recommender.")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("Run 'python -m src.cli.main setup' to initialize the system.")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

