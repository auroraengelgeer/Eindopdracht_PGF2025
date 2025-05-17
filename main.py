import requests
from dotenv import load_dotenv
import os
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


def show_menu():
    print("\U0001f37d\ufe0f What's on the menu today?")
    print("1. Find recipes with ingredients I have in my fridge")
    print("2. Need inspiration? Get a random recipe")
    print("3. Check nutritional value (need recipe ID)")
    print("4. Get the recipe URL (need recipe ID)")
    print("5. Exit (I'm full!)")


def find_recipes_by_ingredients():
    while True:
        try:
            print("\U0001f50dWhat's in your fridge? (separate with commas)")
            print("Like: eggs,milk,flour or chicken,rice,broccoli")
            ingredients = input("> ").strip()

            if not ingredients:
                print("\U0001f635 Oops! You need to enter at least one ingredient")
                continue

            ingredients_list = [i.strip() for i in ingredients.split(",")]
            ingredients_list = [i for i in ingredients_list if i]

            url = f"{BASE_URL}/recipes/findByIngredients"
            params = {
                "apiKey": API_KEY,
                "ingredients": ",".join(ingredients_list),
                "number": 5,
                "ignorePantry": True,
                "ranking": 2
            }

            response = requests.get(url, params=params)
            response.raise_for_status()

            recipes = response.json()

            if not recipes:
                print(f"\n\U0001f625No recipes found with: {', '.join(ingredients_list)}")
                print("Please try different ingredients")
                continue

            print(f"\n\U0001f374 Found {len(recipes)} recipes with your ingredients:")
            for recipe in recipes:
                print(f"\n\U0001f194 [ID: {recipe['id']}] {recipe['title']}")
                print(f"   \u2705 Uses: {len(recipe.get('usedIngredients', []))} ingredients")
                print(f"   \u274e Missing: {len(recipe.get('missedIngredients', []))} ingredients")

            break

        except Exception as error:
            print(f"\n\u26a0\ufe0f Whoops! Something went wrong: {error}")
            print("Let's try that again...")


def get_random_recipe():
    try:
        print("\n\U0001f3b2 Let's get a random recipe!")

        url = f"{BASE_URL}/recipes/random"
        params = {"apiKey": API_KEY, "number": 1}

        response = requests.get(url, params=params)
        response.raise_for_status()

        recipe = response.json()['recipes'][0]

        print(f"\n\U0001f194 [ID: {recipe['id']}] {recipe['title']}")
        print(f"\u23f0 {recipe.get('readyInMinutes', '?')} minutes")
        print(f"\U0001f37d\ufe0f Serves {recipe.get('servings', '?')}")

        if 'sourceUrl' in recipe:
            print(f"\n\U0001f517 Full recipe here: {recipe['sourceUrl']}")
        else:
            print("\n(No link available for this recipe)")

    except Exception as error:
        print(f"\n\u26a0\ufe0f Oops! Error getting random recipe: {error}")


def show_nutritional_info():
    while True:
        try:
            print("\n\U0001f4ca Let's check the nutritional value!")
            recipe_id = input("Enter the recipe ID (from option 1 or 2): ").strip()

            if not recipe_id.isdigit():
                print("\U0001f635 That doesn't look like a valid ID! Use numbers only.")
                continue

            url = f"{BASE_URL}/recipes/{recipe_id}/nutritionWidget.json"
            params = {"apiKey": API_KEY}

            response = requests.get(url, params=params)
            response.raise_for_status()

            nutrition = response.json()

            print("\n\U0001f35c Nutrition per serving:")
            print(f"\U0001f525 Calories: {nutrition.get('calories', '?')} kcal")
            print(f"\U0001f4AA Protein: {nutrition.get('protein', '?')}g")
            print(f"\U0001f9c8 Fat: {nutrition.get('fat', '?')}g")
            print(f"\U0001f33E Carbs: {nutrition.get('carbs', '?')}g")

            break

        except Exception as error:
            print(f"\n\u26a0\ufe0f Nutrition info error: {error}")
            print("Please try again with a different ID")


def get_recipe_link():
    while True:
        try:
            print("\n\U0001f517 Need the full recipe?")
            recipe_id = input("Enter recipe ID: ").strip()

            if not recipe_id.isdigit():
                print("\U0001f635 ID should be numbers only!")
                continue

            url = f"{BASE_URL}/recipes/{recipe_id}/information"
            params = {"apiKey": API_KEY}

            response = requests.get(url, params=params)
            response.raise_for_status()

            recipe_info = response.json()

            if 'sourceUrl' in recipe_info and recipe_info['sourceUrl']:
                print(f"\n\U0001f310 Here's the recipe: {recipe_info['sourceUrl']}")
            else:
                print("\n\U0001f622 Sorry, couldn't find a link for this recipe")
                print("Please try a different recipe ID")
                continue

            break

        except Exception as error:
            print(f"\n\u26a0\ufe0f Error getting recipe link: {error}")
            print("Let's try that again...")

if __name__ == "__main__":
    print("\n\U0001f951 Welcome to the Recipe Finder App! \U0001f951")

    while True:
        show_menu()
        choice = input("\nWhat would you like to do? (1-5): ").strip()

        if choice == "1":
            find_recipes_by_ingredients()
        elif choice == "2":
            get_random_recipe()
        elif choice == "3":
            show_nutritional_info()
        elif choice == "4":
            get_recipe_link()
        elif choice == "5":
            print("\n\U0001faf6 Thanks for using this app! Happy cooking and enjoy your meal!")
            break
        else:
            print("\u274c Please choose 1-5")

        input("Press Enter to continue...")