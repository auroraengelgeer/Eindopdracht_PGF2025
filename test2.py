import requests


API_KEY = "d134c3398b9e4a3c8e311403c3589bbc"  # Vervang dit
BASE_URL = "https://api.spoonacular.com"

def toon_menu():
    print("\n🍽️ MINI RECIPE APP")
    print("1. Zoek recepten op ingrediënten")
    print("2. Krijg een random recept")
    print("3. Bekijk voedingsinformatie (via ID)")
    print("4. Afsluiten")


def zoek_recepten_op_ingredienten():
    try:
        print("\n🔍 Voer ingrediënten in (in het Engels, gescheiden door komma's)")
        print("Voorbeeld: chicken,potato,carrot of pasta,tomato,cheese")
        ingredienten_input = input("> ").strip()

        if not ingredienten_input:
            print("❌ Je moet minstens 1 ingrediënt invoeren")
            return

        ingredienten = [i.strip() for i in ingredienten_input.split(",") if i.strip()]

        url = f"{BASE_URL}/recipes/findByIngredients"
        params = {
            "apiKey": API_KEY,
            "ingredients": ",".join(ingredienten),
            "number": 5,
            "ignorePantry": True,
            "ranking": 2
        }

        response = requests.get(url, params=params)
        response.raise_for_status()
        recepten = response.json()

        if not recepten:
            print(f"\n❌ Geen recepten gevonden met: {', '.join(ingredienten)}")
            return

        print(f"\n🍴 {len(recepten)} recepten gevonden met: {', '.join(ingredienten)}")
        for idx, recept in enumerate(recepten, 1):
            print(f"\n🔹 [ID: {recept['id']}] {recept['title']}")
            print(f"   ✅ Gebruikt {len(recept.get('usedIngredients', []))} ingredienten")
            print(f"   ❌ Mist {len(recept.get('missedIngredients', []))} ingredienten")

            if 'sourceUrl' in recept and recept['sourceUrl']:
                print(f"   🔗 Recept URL: {recept['sourceUrl']}")

    except Exception as e:
        print(f"\n❌ Fout: {str(e)}")


def krijg_random_recept():
    try:
        url = f"{BASE_URL}/recipes/random"
        params = {"apiKey": API_KEY, "number": 1}

        response = requests.get(url, params=params)
        response.raise_for_status()
        recept = response.json()['recipes'][0]

        print("\n🎲 Willekeurig recept:")
        print(f"\n🔹 [ID: {recept['id']}] {recept['title']}")
        print(f"⏱️ {recept.get('readyInMinutes', '?')} minuten | 🍽️ {recept.get('servings', '?')} porties")

        if 'sourceUrl' in recept:
            print(f"\n🔗 Volledig recept: {recept['sourceUrl']}")

    except Exception as e:
        print(f"\n❌ Fout: {str(e)}")


def toon_voedingsinfo():
    try:
        recept_id = input("\nVoer recept-ID in (zie bij optie 1/2): ").strip()
        if not recept_id.isdigit():
            print("❌ Voer een geldig ID in (cijfers)")
            return

        url = f"{BASE_URL}/recipes/{recept_id}/nutritionWidget.json"
        params = {"apiKey": API_KEY}

        response = requests.get(url, params=params)
        response.raise_for_status()
        voeding = response.json()

        print("\n📊 Voedingswaarden per portie:")
        print(f"🔥 Calorieën: {voeding.get('calories', '?')}")
        print(f"🥚 Eiwit: {voeding.get('protein', '?')}g")
        print(f"🧈 Vet: {voeding.get('fat', '?')}g")
        print(f"🌾 Koolhydraten: {voeding.get('carbs', '?')}g")

    except Exception as e:
        print(f"\n❌ Fout: {str(e)}")


# Hoofdprogramma
if __name__ == "__main__":
    print("✨ WELKOM BIJ DE RECEPTEN APP✨")
    print("Je kunt bij elk recept het ID vinden voor voedingsinfo")

    while True:
        toon_menu()
        keuze = input("\nMaak je keuze (1-4): ").strip()

        if keuze == "1":
            zoek_recepten_op_ingredienten()
        elif keuze == "2":
            krijg_random_recept()
        elif keuze == "3":
            toon_voedingsinfo()
        elif keuze == "4":
            print("\n👋 Bedankt en eet smakelijk!")
            break
        else:
            print("❌ Ongeldige keuze")

        input("\nDruk op Enter om verder te gaan...")