"""
State schema for the Recipe Finder LangGraph workflow
"""
from typing import TypedDict, List


class RecipeFinderState(TypedDict, total=False):
    """State for the recipe finder workflow"""
    user_query: str
    recipe_results: List[dict]
    selected_recipe_index: int
    selected_recipe: str
    ingredients: List[str]
    product_urls: List[dict]
    final_response: str

