import requests
from dotenv import load_dotenv
import os
load_dotenv()



API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")

def show_menu():
    print("\n\U0001F37D\U0000FE0F What's On The Menu Today?")
    print("1. Find recipes based on ingredients you have in your fridge")
    print("2. Need inspiration? Get a random recipe")
    print("3. Find out about nutritional values (with recipe-ID)")
    print("4. Get the link to your favourite recipe (with recipe-ID)")
    print("5. Close")

def recipes_from_ingredients():
    try:
        print("\n\U0001F50D What ingredients do you have? (divide them with commas)")
        print("Example: chicken,potato,carrot or pasta,tomato,cheese")
        ingrediënten_input = input("> ").strip()

        if not ingrediënten_input:
            print("\U0000274C You have to write down at least 1 ingredient.")
            return

        ingrediënten = [i.strip() for i in ingrediënten_input.split(",") if i.strip()]

        url = f"{BASE_URL}/recipes/findByIngredients"
        params = {
            "apiKey": API_KEY,
            "ingredients": ",".join(ingrediënten),
            "number": 5,
            "ignorePantry": True,
            "ranking": 2
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        recepten = response.json()

        if not recepten:
            print(f"\n\U0000274C No recipes found with: {', '.join(ingrediënten)}")
            return

        print(f"\n\U0001F374 {len(recepten)} recipes found with: {', '.join(ingrediënten)}")
        for idx, recept in enumerate(recepten, 1):
            print(f"\n\U0001F539 [ID: {recept['id']}] {recept['title']}")
            print(f"   \U00002705 Uses: {len(recept.get('usedIngredients', []))} ingredient(s)")
            print(f"   \U0000274C Missing: {len(recept.get('missedIngredients', []))} ingredient(s)")

    except Exception as e:
        print(f"\n\U0000274C Error: {str(e)}")

def get_random_recipe():
    try:
        url = f"{BASE_URL}/recipes/random"
        params = {"apiKey": API_KEY, "number": 1}

        response = requests.get(url, params=params)
        response.raise_for_status()
        recept = response.json()['recipes'][0]

        print("\n\U0001F3B2 Random recipe:")
        print(f"\n\U0001F539 [ID: {recept['id']}] {recept['title']}")
        print(f"\U000023F1\U0000FE0F {recept.get('readyInMinutes')} minutes | \U0001F37D\U0000FE0F {recept.get('servings')} servings")

        if 'sourceUrl' in recept:
            print(f"\n\U0001F517 Full recipe: {recept['sourceUrl']}")

    except Exception as e:
        print(f"\n\U0000274C Error: {str(e)}")

def show_nutrional_value():
    try:
        recept_id = input("\nEnter recipe-ID (see option 1/2): ").strip()
        if not recept_id.isdigit():
            print("\U0000274C Enter a valid ID in numbers")
            return

        url = f"{BASE_URL}/recipes/{recept_id}/nutritionWidget.json"
        params = {"apiKey": API_KEY}

        response = requests.get(url, params=params)
        response.raise_for_status()
        voeding = response.json()

        print("\n\U0001F4CA Nutrional value per serving:")
        print(f"\U0001F525 Calories: {voeding.get('calories')} kcal")
        print(f"\U0001F95A Protein: {voeding.get('protein')}")
        print(f"\U0001F9C2 Fat: {voeding.get('fat')}")
        print(f"\U0001F33E Carbohydrates: {voeding.get('carbs')}")

    except Exception as e:
        print(f"\n\U0000274C Error: {str(e)}")

def get_recipe_url():
    try:
        recept_id = input("\nEnter recipe-ID to get the recipe-URL: ").strip()
        if not recept_id.isdigit():
            print("\U0000274C Enter a valid ID in numbers")
            return

        url = f"{BASE_URL}/recipes/{recept_id}/information"
        params = {"apiKey": API_KEY}

        response = requests.get(url, params=params)
        response.raise_for_status()
        recept_info = response.json()

        if 'sourceUrl' in recept_info and recept_info['sourceUrl']:
            print(f"\n\U0001F517 Recipe URL for ID {recept_id}:")
            print(recept_info['sourceUrl'])
        else:
            print(f"\n\U0000274C No URL found for this recipe-ID {recept_id}")

    except Exception as e:
        print(f"\n\U0000274C Error: {str(e)}")

# Main
if __name__ == "__main__":
    print("\U00002728 Welcome in the Recipe Finder! \U00002728")
    print("Every recipe includes a ID that can be used to request nutritional value and the recipe-URL")

    while True:
        show_menu()
        choice = input("\nChoose your option (1-5): ").strip()

        if choice == "1":
            recipes_from_ingredients()
        elif choice == "2":
            get_random_recipe()
        elif choice == "3":
            show_nutrional_value()
        elif choice == "4":
            get_recipe_url()
        elif choice == "5":
            print("\n\U0001F44B Thank you and enjoy your meal!")
            break
        else:
            print("\U0000274C Invalid choice")

        input("\nPress Enter to continue...")