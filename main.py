"""
Recipe Finder with Ingredient Sourcing
A LangGraph application that finds recipes and sources ingredients from Egyptian markets
"""
from langgraph.graph import StateGraph, END
from state import RecipeFinderState
from nodes import (
    search_recipes_node,
    extract_ingredients_node,
    find_product_urls_node,
    generate_final_response_node
)


def create_recipe_finder_graph():
    """
    Create the LangGraph workflow
    """
    # Initialize the graph
    workflow = StateGraph(RecipeFinderState)
    
    # Add nodes
    workflow.add_node("search_recipes", search_recipes_node)
    workflow.add_node("extract_ingredients", extract_ingredients_node)
    workflow.add_node("find_product_urls", find_product_urls_node)
    workflow.add_node("generate_response", generate_final_response_node)
    
    # Define the flow
    workflow.set_entry_point("search_recipes")
    workflow.add_edge("search_recipes", "extract_ingredients")
    workflow.add_edge("extract_ingredients", "find_product_urls")
    workflow.add_edge("find_product_urls", "generate_response")
    workflow.add_edge("generate_response", END)
    
    # Compile the graph
    return workflow.compile()


def main():
    """
    Main function to run the recipe finder
    """
    print("=" * 60)
    print("🍽️  RECIPE FINDER WITH INGREDIENT SOURCING")
    print("=" * 60)
    
    # Get user input
    user_query = input("\n💬 What would you like to cook today? ")
    
    if not user_query.strip():
        print("❌ Please provide a valid query!")
        return
    
    # Create the graph
    app = create_recipe_finder_graph()
    
    # Run the workflow
    initial_state: RecipeFinderState = {
        "user_query": user_query,
        "recipe_results": [],
        "selected_recipe_index": 0,
        "selected_recipe": "",
        "ingredients": [],
        "product_urls": [],
        "final_response": ""
    }
    
    print("\n🚀 Starting recipe finder workflow...\n")
    
    try:
        # Execute the graph
        final_state = app.invoke(initial_state)
        
        # Display the final response
        print("\n" + "=" * 60)
        print(final_state["final_response"])
        print("\n" + "=" * 60)
        print("\n✨ Done! Happy cooking! 🍳")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Please check your API keys in the .env file")


if __name__ == "__main__":
    main()

