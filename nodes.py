"""
LangGraph nodes for the Recipe Finder workflow
"""
from state import RecipeFinderState
from tools import (
    search_recipes,
    extract_ingredients_with_llm,
    search_product_urls,
    get_egyptian_markets
)


def search_recipes_node(state: RecipeFinderState) -> RecipeFinderState:
    """
    Node 1: Search for recipes using Tavily based on user query
    """
    user_query = state.get('user_query', '')
    print(f"\n🔍 Searching for recipes: {user_query}")
    
    # Search using Tavily
    recipe_results = search_recipes(user_query, max_results=5)
    
    print(f"✅ Found {len(recipe_results)} recipes\n")
    
    # Display recipes for user to choose
    if recipe_results:
        print("📋 Available Recipes:")
        print("=" * 60)
        for i, recipe in enumerate(recipe_results, 1):
            print(f"\n{i}. {recipe['title']}")
            print(f"   URL: {recipe['url']}")
            # Show a snippet of the content
            content_preview = recipe.get('content', '')[:150]
            if content_preview:
                print(f"   Preview: {content_preview}...")
        
        print("\n" + "=" * 60)
        
        # Get user selection
        while True:
            try:
                choice = input(f"\n👉 Select a recipe (1-{len(recipe_results)}): ").strip()
                selected_index = int(choice) - 1
                if 0 <= selected_index < len(recipe_results):
                    break
                else:
                    print(f"❌ Please enter a number between 1 and {len(recipe_results)}")
            except ValueError:
                print("❌ Please enter a valid number")
        
        selected_recipe = recipe_results[selected_index].get('content', '')
        print(f"\n✅ Selected: {recipe_results[selected_index]['title']}")
    else:
        selected_index = 0
        selected_recipe = ""
    
    return {
        "recipe_results": recipe_results,
        "selected_recipe_index": selected_index,
        "selected_recipe": selected_recipe
    }


def extract_ingredients_node(state: RecipeFinderState) -> RecipeFinderState:
    """
    Node 2: Extract ingredients from the selected recipe using LLM
    """
    print("\n📝 Extracting ingredients from recipe...")
    
    selected_recipe = state.get('selected_recipe', '')
    
    if not selected_recipe:
        return {"ingredients": []}
    
    # Use LLM to extract ingredients
    ingredients = extract_ingredients_with_llm(selected_recipe)
    
    print(f"✅ Extracted {len(ingredients)} ingredients: {', '.join(ingredients[:5])}...")
    
    return {"ingredients": ingredients}


def find_product_urls_node(state: RecipeFinderState) -> RecipeFinderState:
    """
    Node 3: Find URLs to buy ingredients from Egyptian markets
    """
    print("\n🛒 Finding product URLs in Egyptian markets...")
    
    ingredients = state.get('ingredients', [])
    product_urls = []
    
    # Get Egyptian markets
    egyptian_markets = get_egyptian_markets()
    
    for ingredient in ingredients[:10]:  # Limit to first 10 ingredients
        # Search for each ingredient in Egyptian markets
        result = search_product_urls(ingredient, egyptian_markets)
        if result:
            product_urls.append(result)
    
    print(f"✅ Found {len(product_urls)} product URLs")
    
    return {"product_urls": product_urls}


def generate_final_response_node(state: RecipeFinderState) -> RecipeFinderState:
    """
    Final node: Generate a comprehensive response for the user
    """
    print("\n📋 Generating final response...")
    
    recipe_results = state.get('recipe_results', [])
    selected_index = state.get('selected_recipe_index', 0)
    ingredients = state.get('ingredients', [])
    product_urls = state.get('product_urls', [])
    
    # Build the final response
    response_parts = []
    
    # Selected recipe information
    response_parts.append("🍳 YOUR SELECTED RECIPE")
    response_parts.append("=" * 50)
    if recipe_results and selected_index < len(recipe_results):
        selected = recipe_results[selected_index]
        response_parts.append(f"\n✅ {selected['title']}")
        response_parts.append(f"   URL: {selected['url']}")
    
    # Other recipe suggestions
    response_parts.append("\n\n📚 OTHER RECIPE OPTIONS")
    response_parts.append("=" * 50)
    for i, recipe in enumerate(recipe_results, 1):
        if i - 1 != selected_index:  # Skip the selected one
            response_parts.append(f"\n{i}. {recipe['title']}")
            response_parts.append(f"   URL: {recipe['url']}")
    
    # Ingredients
    response_parts.append("\n\n📝 INGREDIENTS NEEDED")
    response_parts.append("=" * 50)
    for i, ingredient in enumerate(ingredients, 1):
        response_parts.append(f"{i}. {ingredient}")
    
    # Shopping links
    response_parts.append("\n\n🛒 WHERE TO BUY (Egyptian Markets)")
    response_parts.append("=" * 50)
    if product_urls:
        for item in product_urls:
            response_parts.append(f"\n• {item['ingredient']}")
            response_parts.append(f"  {item['title']}")
            response_parts.append(f"  🔗 {item['url']}")
    else:
        response_parts.append("\nNo specific product URLs found. Try searching on:")
        response_parts.append("- Jumia Egypt (jumia.com.eg)")
        response_parts.append("- Noon Egypt (noon.com/egypt)")
        response_parts.append("- Amazon Egypt (amazon.eg)")
        response_parts.append("- Carrefour Egypt (carrefouregypt.com)")
    
    final_response = "\n".join(response_parts)
    
    print("✅ Final response generated")
    
    return {"final_response": final_response}
