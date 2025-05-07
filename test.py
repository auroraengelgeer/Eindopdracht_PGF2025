import requests

API_KEY = "d134c3398b9e4a3c8e311403c3589bbc"
BASE_URL = "https://api.spoonacular.com"

# Emoji verklaring:
# \U0001F37D - 🍽 (bord met mes en vork)
# \U0001F50D - 🔍 (vergrootglas)
# \U0001F539 - 🔹 (blauwe ruit)
# \U00002705 - ✅ (groen vinkje)
# \U0000274C - ❌ (rood kruis)
# \U0001F3B2 - 🎲 (dobbelsteen)
# \U000023F1 - ⏱ (stopwatch)
# \U0001F37D - 🍽 (bord met mes en vork -zelfde als boven)
# \U0001F517 - 🔗 (kettinglink)
# \U0001F4CA - 📊 (balkdiagram)
# \U0001F525 - 🔥 (vuur)
# \U0001F95A - 🥚 (ei)
# \U0001F9C2 - 🧈 (boter)
# \U0001F33E - 🌾 (korenaar)
# \U0001F44B - 👋 (zwaaiende hand)

def toon_menu():
    print("\n\U0001F37D MINI RECIPE APP")
    print("1. Zoek recepten op ingrediënten")
    print("2. Krijg een random recept")
    print("3. Bekijk voedingsinformatie (via ID)")
    print("4. Vraag recept URL op (via ID)")
    print("5. Afsluiten")

def zoek_recepten_op_ingredienten():
    try:
        print("\n\U0001F50D Voer ingrediënten in (in het Engels, gescheiden door komma's)")
        print("Voorbeeld: chicken,potato,carrot of pasta,tomato,cheese")
        ingrediënten_input = input("> ").strip()

        if not ingrediënten_input:
            print("\U0000274C Je moet minstens 1 ingrediënt invoeren")
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
            print(f"\n\U0000274C Geen recepten gevonden met: {', '.join(ingrediënten)}")
            return

        print(f"\n\U0001F37D {len(recepten)} recepten gevonden met: {', '.join(ingrediënten)}")
        for idx, recept in enumerate(recepten, 1):
            print(f"\n\U0001F539 [ID: {recept['id']}] {recept['title']}")
            print(f"   \U00002705 Gebruikt {len(recept.get('usedIngredients', []))} ingrediënten")
            print(f"   \U0000274C Mist {len(recept.get('missedIngredients', []))} ingrediënten")

            if 'sourceUrl' in recept and recept['sourceUrl']:
                print(f"   \U0001F517 Recept URL: {recept['sourceUrl']}")

    except Exception as e:
        print(f"\n\U0000274C Fout: {str(e)}")

def krijg_random_recept():
    try:
        url = f"{BASE_URL}/recipes/random"
        params = {"apiKey": API_KEY, "number": 1}

        response = requests.get(url, params=params)
        response.raise_for_status()
        recept = response.json()['recipes'][0]

        print("\n\U0001F3B2 Willekeurig recept:")
        print(f"\n\U0001F539 [ID: {recept['id']}] {recept['title']}")
        print(f"\U000023F1 {recept.get('readyInMinutes', '?')} minuten | \U0001F37D {recept.get('servings', '?')} porties")

        if 'sourceUrl' in recept:
            print(f"\n\U0001F517 Volledig recept: {recept['sourceUrl']}")

    except Exception as e:
        print(f"\n\U0000274C Fout: {str(e)}")

def toon_voedingsinfo():
    try:
        recept_id = input("\nVoer recept-ID in (zie bij optie 1/2): ").strip()
        if not recept_id.isdigit():
            print("\U0000274C Voer een geldig ID in (cijfers)")
            return

        url = f"{BASE_URL}/recipes/{recept_id}/nutritionWidget.json"
        params = {"apiKey": API_KEY}

        response = requests.get(url, params=params)
        response.raise_for_status()
        voeding = response.json()

        print("\n\U0001F4CA Voedingswaarden per portie:")
        print(f"\U0001F525 Calorieën: {voeding.get('calories', '?')}")
        print(f"\U0001F95A Eiwit: {voeding.get('protein', '?')}g")
        print(f"\U0001F9C2 Vet: {voeding.get('fat', '?')}g")
        print(f"\U0001F33E Koolhydraten: {voeding.get('carbs', '?')}g")

    except Exception as e:
        print(f"\n\U0000274C Fout: {str(e)}")

def vraag_recept_url_op():
    try:
        recept_id = input("\nVoer recept-ID in om de URL op te vragen: ").strip()
        if not recept_id.isdigit():
            print("\U0000274C Voer een geldig ID in (cijfers)")
            return

        url = f"{BASE_URL}/recipes/{recept_id}/information"
        params = {"apiKey": API_KEY}

        response = requests.get(url, params=params)
        response.raise_for_status()
        recept_info = response.json()

        if 'sourceUrl' in recept_info and recept_info['sourceUrl']:
            print(f"\n\U0001F517 Recept URL voor ID {recept_id}:")
            print(recept_info['sourceUrl'])
        else:
            print(f"\n\U0000274C Geen URL gevonden voor recept met ID {recept_id}")

    except Exception as e:
        print(f"\n\U0000274C Fout: {str(e)}")

if __name__ == "__main__":
    print("\U00002728 WELKOM BIJ DE RECEPTEN APP \U00002728")
    print("Je kunt bij elk recept het ID vinden voor voedingsinfo en URL's")

    while True:
        toon_menu()
        keuze = input("\nMaak je keuze (1-5): ").strip()

        if keuze == "1":
            zoek_recepten_op_ingredienten()
        elif keuze == "2":
            krijg_random_recept()
        elif keuze == "3":
            toon_voedingsinfo()
        elif keuze == "4":
            vraag_recept_url_op()
        elif keuze == "5":
            print("\n\U0001F44B Bedankt en eet smakelijk!")
            break
        else:
            print("\U0000274C Ongeldige keuze")

        input("\nDruk op Enter om verder te gaan...")