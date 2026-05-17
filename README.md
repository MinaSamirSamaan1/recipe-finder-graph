# Recipe Finder with Ingredient Sourcing 🍳

A LangGraph-powered application that helps you find recipes and source ingredients from Egyptian online markets.

## Features

- 🔍 **Recipe Search**: Uses Tavily to search for up to 5 recipes based on your query
- 👤 **User Recipe Selection**: Choose your preferred recipe from the search results
- 📝 **Ingredient Extraction**: Automatically extracts ingredients using OpenAI's GPT
- 🛒 **Product Sourcing**: Finds URLs to buy ingredients from Egyptian online markets
- 🤖 **LangGraph Workflow**: Orchestrates the entire process using a state machine

## Architecture

The application uses a LangGraph workflow with 4 nodes:

1. **Search Recipes Node**: Searches for recipes using Tavily API
2. **Extract Ingredients Node**: Uses LLM to extract ingredients from recipe content
3. **Find Product URLs Node**: Searches for ingredient purchase links in Egyptian markets
4. **Generate Response Node**: Compiles all information into a user-friendly response

## Supported Egyptian Markets

- Jumia Egypt (jumia.com.eg)
- Noon Egypt (noon.com/egypt)
- Amazon Egypt (amazon.eg)
- Carrefour Egypt (carrefouregypt.com)

## Prerequisites

- Python 3.14+
- OpenAI API Key
- Tavily API Key
- LangSmith API Key (optional, for tracing)

## Installation

1. Clone the repository:
```bash
cd recipe-finder-graph
```

2. Install dependencies using uv:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp .env.example .env
```

4. Edit `.env` and add your API keys:
```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
LANGSMITH_API_KEY=your_langsmith_key (optional)
```

## Usage

Run the application:

```bash
uv run python main.py
```

Or activate the virtual environment first:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

### Example Interaction

```
💬 What would you like to cook today? pizza

🔍 Searching for recipes: pizza
✅ Found 5 recipes

📋 Available Recipes:
============================================================

1. New York Style Pizza Recipe
   URL: https://example.com/ny-pizza
   Preview: Classic New York style pizza with thin crust...

2. Authentic Neapolitan Pizza
   URL: https://example.com/neapolitan
   Preview: Traditional Italian pizza from Naples...

3. Chicago Deep Dish Pizza
   URL: https://example.com/deep-dish
   Preview: Thick crust pizza with layers of cheese...

👉 Select a recipe (1-5): 2

✅ Selected: Authentic Neapolitan Pizza

📝 Extracting ingredients from recipe...
✅ Extracted 5 ingredients: mozzarella cheese, basil, olive oil, flour, dry yeast

🛒 Finding product URLs in Egyptian markets...
✅ Found 5 product URLs

🍳 YOUR SELECTED RECIPE
==================================================

✅ Authentic Neapolitan Pizza
   URL: https://example.com/neapolitan

📚 OTHER RECIPE OPTIONS
==================================================

1. New York Style Pizza Recipe
   URL: https://example.com/ny-pizza

3. Chicago Deep Dish Pizza
   URL: https://example.com/deep-dish

📝 INGREDIENTS NEEDED
==================================================
1. mozzarella cheese
2. basil
3. olive oil
4. flour
5. dry yeast

🛒 WHERE TO BUY (Egyptian Markets)
==================================================

• mozzarella cheese
  Mozzarella Cheese 250g
  🔗 https://amazon.eg/...

• basil
  Fresh Basil 100g
  🔗 https://carrefouregypt.com/...

• olive oil
  Extra Virgin Olive Oil
  🔗 https://noon.com/egypt/...
```

## Project Structure

```
recipe-finder-graph/
├── main.py              # Main entry point and workflow orchestration
├── state.py             # State schema definition
├── nodes.py             # LangGraph node implementations
├── tools.py             # Utility functions and API clients
├── pyproject.toml       # Project dependencies
├── .env                 # Environment variables (not in git)
├── .env.example         # Example environment variables
├── README.md            # This file
└── .venv/               # Virtual environment
```

### Module Descriptions

- **main.py**: Entry point that creates the LangGraph workflow and handles user interaction
- **state.py**: Defines the `RecipeFinderState` TypedDict for the workflow state
- **nodes.py**: Contains all LangGraph node functions (search, extract, find, generate)
- **tools.py**: Utility functions for Tavily searches, LLM calls, and API client initialization

## Dependencies

- `langchain-openai`: OpenAI integration for LangChain
- `langgraph`: State machine framework for building agent workflows
- `tavily-python`: Tavily search API client
- `python-dotenv`: Environment variable management

## How It Works

1. **User Input**: User provides a query about what to cook
2. **Recipe Search**: Tavily searches the web for relevant recipes
3. **Ingredient Extraction**: LLM analyzes recipe content and extracts ingredients
4. **Product Search**: Tavily searches for each ingredient in Egyptian online markets
5. **Response Generation**: All information is compiled into a structured response

## LangGraph Workflow

```
┌─────────────────┐
│  Start          │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Search Recipes  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Extract Ingred.  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Find Product URLs│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Generate Response│
└────────┬────────┘
         │
         ▼
      ┌─────┐
      │ End │
      └─────┘
```

## Troubleshooting

### API Key Issues
- Ensure all required API keys are set in `.env`
- Check that keys are valid and have sufficient credits

### No Product URLs Found
- The search might not find Egyptian market URLs for all ingredients
- Try more common ingredient names
- Check if the Egyptian markets are accessible

### LangSmith Tracing
- Set `LANGSMITH_TRACING=true` in `.env` to enable tracing
- View traces at https://smith.langchain.com

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.