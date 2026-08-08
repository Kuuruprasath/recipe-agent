import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Set your API key and search query
api_key = os.getenv("FOODAPI")
url = "https://api.spoonacular.com/recipes/findByIngredients"

def getRecipe(ingredients):
    ingredients
    params = {
        "apiKey": api_key,
        "ingredients": "tomato,cheese,egg", 
        "number": 1,
        "ranking": 1,
        "ignorePantry": True
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        recipe = response.json()
        recipe = recipe[0]
        menu_id = recipe['id']
        menu_title = recipe['title']
        menu_missed_ingredient = [item['name'] for item in recipe['missedIngredients']]
    else:
        print(f"Error: {response.status_code} - {response.text}")

    return [menu_id,menu_title,menu_missed_ingredient]
