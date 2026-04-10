import pandas as pd

def transform_daily_food_nutrition(df: pd.DataFrame) -> dict:
    """
    Nettoie et sépare le DataFrame en 4 tables :
    categories, meal_types, foods, nutrition_logs
    """

    # --- Nettoyage général ---
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df.drop_duplicates(inplace=True)

    # Renommage pour coller au schéma init.sql
    df = df.rename(columns={
        "food_item":        "name",
        "category":         "category_name",
        "calories_(kcal)":  "calories",
        "protein_(g)":      "protein",
        "carbohydrates_(g)":"carbohydrates",
        "fat_(g)":          "fat",
        "fiber_(g)":        "fiber",
        "sugars_(g)":       "sugars",
        "sodium_(mg)":      "sodium",
        "cholesterol_(mg)": "cholesterol",
        "meal_type":        "meal_type_name",
        "water_intake_(ml)":"water_intake"
    })

    # --- Table categories (valeurs uniques) ---
    categories = pd.DataFrame(
        df["category_name"].dropna().str.strip().unique(),
        columns=["name"]
    ).sort_values("name").reset_index(drop=True)

    # --- Table meal_types (valeurs uniques) ---
    meal_types = pd.DataFrame(
        df["meal_type_name"].dropna().str.strip().unique(),
        columns=["name"]
    ).sort_values("name").reset_index(drop=True)

    # --- Table foods (nom + catégorie) ---
    foods = df[["name", "category_name"]].copy()
    foods["name"]          = foods["name"].str.strip()
    foods["category_name"] = foods["category_name"].str.strip()
    foods.dropna(subset=["name", "category_name"], inplace=True)
    foods.drop_duplicates(subset=["name"], inplace=True)
    foods.reset_index(drop=True, inplace=True)

    # --- Table nutrition_logs ---
    nutrition_logs = df[[
        "name", "meal_type_name",
        "calories", "protein", "carbohydrates", "fat",
        "fiber", "sugars", "sodium", "cholesterol", "water_intake"
    ]].copy()

    numeric_cols = [
        "calories", "protein", "carbohydrates", "fat",
        "fiber", "sugars", "sodium", "cholesterol"
    ]
    for col in numeric_cols:
        nutrition_logs[col] = pd.to_numeric(nutrition_logs[col], errors="coerce")
        nutrition_logs[col] = nutrition_logs[col].replace({float('nan'): None})

    nutrition_logs["water_intake"] = pd.to_numeric(
        nutrition_logs["water_intake"], errors="coerce"
    ).fillna(0).astype(int)

    nutrition_logs.dropna(subset=["name", "meal_type_name"], inplace=True)
    nutrition_logs.reset_index(drop=True, inplace=True)

    print(f"[TRANSFORM] categories   : {len(categories)} lignes")
    print(f"[TRANSFORM] meal_types   : {len(meal_types)} lignes")
    print(f"[TRANSFORM] foods        : {len(foods)} lignes")
    print(f"[TRANSFORM] nutrition_logs: {len(nutrition_logs)} lignes")

    return {
        "categories":     categories,
        "meal_types":     meal_types,
        "foods":          foods,
        "nutrition_logs": nutrition_logs
    }