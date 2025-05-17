import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")


def show_menu():
    print("\n🍽️ What's on the menu today?")
    print("1. Find recipes with ingredients I have in my fridge")
    print("2. Need inspiration? Get a random recipe")
    print("3. Check nutritional value (need recipe ID)")
    print("4. Get the recipe URL (need recipe ID)")
    print("5. Exit (I'm full!)")


def find_recipes_by_ingredients():
    try:
        print("\n🔍 What's in your fridge? (separate with commas)")
        print("Like: eggs,milk,flour or chicken,rice,broccoli")
        ingredients = input("> ").strip()

        if not ingredients:
            print("❌ Oops! You need to enter at least one ingredient")
            return

        ingredients_list = [i.strip() for i in ingredients.split(",")]
        ingredients_list = [i for i in ingredients_list if i]  # Remove empty strings

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
            print(f"\n😢 No recipes found with: {', '.join(ingredients_list)}")
            return

        print(f"\n🍴 Found {len(recipes)} recipes with your ingredients:")
        for recipe in recipes:
            print(f"\n📝 [ID: {recipe['id']}] {recipe['title']}")
            print(f"   ✔ Uses: {len(recipe.get('usedIngredients', []))} ingredients")
            print(f"   ❌ Missing: {len(recipe.get('missedIngredients', []))} ingredients")

    except Exception as error:
        print(f"\n⚠️ Whoops! Something went wrong: {error}")


def get_random_recipe():
    try:
        print("\n🎲 Let's get a random recipe!")

        url = f"{BASE_URL}/recipes/random"
        params = {"apiKey": API_KEY, "number": 1}

        response = requests.get(url, params=params)
        response.raise_for_status()

        recipe = response.json()['recipes'][0]

        print("\n✨ Here's your random recipe:")
        print(f"\n📝 [ID: {recipe['id']}] {recipe['title']}")
        print(f"⏱️ {recipe.get('readyInMinutes', '?')} minutes")
        print(f"🍽️ Serves {recipe.get('servings', '?')}")

        if 'sourceUrl' in recipe:
            print(f"\n🔗 Full recipe here: {recipe['sourceUrl']}")
        else:
            print("\n(No link available for this recipe)")

    except Exception as error:
        print(f"\n⚠️ Oops! Error getting random recipe: {error}")


def show_nutritional_info():
    try:
        print("\n📊 Let's check the nutritional value!")
        recipe_id = input("Enter the recipe ID (from option 1 or 2): ").strip()

        if not recipe_id.isdigit():
            print("❌ That doesn't look like a valid ID! Use numbers only.")
            return

        url = f"{BASE_URL}/recipes/{recipe_id}/nutritionWidget.json"
        params = {"apiKey": API_KEY}

        response = requests.get(url, params=params)
        response.raise_for_status()

        nutrition = response.json()

        print("\n📈 Nutrition per serving:")
        print(f"🔥 Calories: {nutrition.get('calories', '?')} kcal")
        print(f"💪 Protein: {nutrition.get('protein', '?')}g")
        print(f"🧈 Fat: {nutrition.get('fat', '?')}g")
        print(f"🌾 Carbs: {nutrition.get('carbs', '?')}g")

    except Exception as error:
        print(f"\n⚠️ Nutrition info error: {error}")


def get_recipe_link():
    try:
        print("\n🔗 Need the full recipe?")
        recipe_id = input("Enter recipe ID: ").strip()

        if not recipe_id.isdigit():
            print("❌ ID should be numbers only!")
            return

        url = f"{BASE_URL}/recipes/{recipe_id}/information"
        params = {"apiKey": API_KEY}

        response = requests.get(url, params=params)
        response.raise_for_status()

        recipe_info = response.json()

        if 'sourceUrl' in recipe_info and recipe_info['sourceUrl']:
            print(f"\n🌐 Here's the recipe: {recipe_info['sourceUrl']}")
        else:
            print("\n😢 Sorry, couldn't find a link for this recipe")

    except Exception as error:
        print(f"\n⚠️ Error getting recipe link: {error}")

if __name__ == "__main__":
    print("\n🌟 Welcome to my Recipe Finder App! 🌟")
    print("(Made for my Python class final project)")
    print("Tip: Every recipe has a recipe ID that you can use for more info!")

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
            print("\n👋 Thanks for using my app! Happy cooking!")
            break
        else:
            print("❌ Please choose 1-5")

        input("Press Enter to continue...")