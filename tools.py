"""
Tools and utilities for the Recipe Finder application
"""
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Initialize clients
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)


def search_recipes(query: str, max_results: int = 3) -> list:
    """
    Search for recipes using Tavily API
    
    Args:
        query: The search query
        max_results: Maximum number of results to return
        
    Returns:
        List of recipe dictionaries with title, url, and content
    """
    search_query = f"recipe for {query}"
    results = tavily_client.search(
        query=search_query,
        max_results=max_results,
        search_depth="advanced"
    )
    
    recipe_results = []
    for result in results.get('results', []):
        recipe_results.append({
            'title': result.get('title', ''),
            'url': result.get('url', ''),
            'content': result.get('content', '')
        })
    
    return recipe_results


def extract_ingredients_with_llm(recipe_content: str) -> list:
    """
    Extract ingredients from recipe content using LLM
    
    Args:
        recipe_content: The recipe text content
        
    Returns:
        List of ingredient strings
    """
    if not recipe_content:
        return []
    
    prompt = f"""
    From the following recipe content, extract ONLY the main ingredients as a simple list.
    Return ONLY the ingredient names, one per line, without any quantities, measurements, or descriptions.
    Focus on the core ingredients (vegetables, proteins, grains, spices, etc.).
    Do not include water, salt, or pepper.
    
    Recipe content:
    {recipe_content}
    
    Format: Return each ingredient on a new line, like this:
    chicken
    garlic
    onion
    tomatoes
    """
    
    response = llm.invoke(prompt)
    
    # Handle response content properly
    if hasattr(response, 'content'):
        ingredients_text = str(response.content).strip()
    else:
        ingredients_text = str(response).strip()
    
    # Parse ingredients - split by newlines and clean up
    ingredients = []
    for line in ingredients_text.split('\n'):
        ingredient = line.strip()
        # Remove bullet points, numbers, dashes
        ingredient = ingredient.lstrip('•-*123456789. ')
        if ingredient and len(ingredient) > 2:  # Skip very short entries
            ingredients.append(ingredient)
    
    return ingredients


def search_product_urls(ingredient: str, egyptian_markets: list) -> dict | None:
    """
    Search for product URLs for a specific ingredient in Egyptian markets
    
    Args:
        ingredient: The ingredient to search for
        egyptian_markets: List of Egyptian market domains
        
    Returns:
        Dictionary with ingredient info and URL, or None if not found
    """
    search_query = f"{ingredient} buy online Egypt {' OR '.join(egyptian_markets)}"
    
    try:
        results = tavily_client.search(
            query=search_query,
            max_results=2,
            search_depth="basic"
        )
        
        for result in results.get('results', []):
            url = result.get('url', '')
            # Filter for Egyptian market URLs
            if any(market in url.lower() for market in egyptian_markets):
                return {
                    'ingredient': ingredient,
                    'title': result.get('title', ''),
                    'url': url,
                    'price_info': result.get('content', '')[:200]
                }
    except Exception as e:
        print(f"⚠️  Error searching for {ingredient}: {str(e)}")
    
    return None


def get_egyptian_markets() -> list:
    """
    Get list of Egyptian online market domains
    
    Returns:
        List of market domain strings
    """
    return [
        "jumia.com.eg",
        "noon.com/egypt",
        "amazon.eg",
        "carrefouregypt.com"
    ]

