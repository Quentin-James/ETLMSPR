import psycopg2
from psycopg2.extras import execute_values
from config import DB_CONFIG

def load_daily_food_nutrition(tables: dict):
    """
    Insère categories, meal_types, foods et nutrition_logs
    dans PostgreSQL en respectant les FK du schéma init.sql.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # --- Insertion categories ---
        categories = tables["categories"]
        category_map = {}  # name -> id

        for _, row in categories.iterrows():
            cursor.execute("""
                INSERT INTO categories (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id, name
            """, (row["name"],))
            result = cursor.fetchone()
            if result:
                category_map[result[1]] = result[0]

        # Récupérer les ids déjà existants (si ON CONFLICT DO NOTHING)
        cursor.execute("SELECT id, name FROM categories")
        for cid, cname in cursor.fetchall():
            category_map[cname] = cid

        print(f"[LOAD] {len(category_map)} categories insérées/récupérées")

        # --- Insertion meal_types ---
        meal_types = tables["meal_types"]
        meal_type_map = {}  # name -> id

        for _, row in meal_types.iterrows():
            cursor.execute("""
                INSERT INTO meal_types (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING
                RETURNING id, name
            """, (row["name"],))
            result = cursor.fetchone()
            if result:
                meal_type_map[result[1]] = result[0]

        cursor.execute("SELECT id, name FROM meal_types")
        for mid, mname in cursor.fetchall():
            meal_type_map[mname] = mid

        print(f"[LOAD] {len(meal_type_map)} meal_types insérés/récupérés")

        # --- Insertion foods ---
        foods = tables["foods"]
        food_map = {}  # name -> id

        for _, row in foods.iterrows():
            cat_id = category_map.get(row["category_name"])
            if not cat_id:
                continue
            cursor.execute("""
                INSERT INTO foods (name, category_id)
                VALUES (%s, %s)
                RETURNING id, name
            """, (row["name"], cat_id))
            result = cursor.fetchone()
            if result:
                food_map[result[1]] = result[0]

        print(f"[LOAD] {len(food_map)} foods insérés")

        # --- Insertion nutrition_logs ---
        nutrition_logs = tables["nutrition_logs"]
        nl_data = []

        for _, row in nutrition_logs.iterrows():
            food_id      = food_map.get(row["name"])
            meal_type_id = meal_type_map.get(row["meal_type_name"])
            if not food_id or not meal_type_id:
                continue
            nl_data.append((
                food_id, meal_type_id,
                row["calories"], row["protein"], row["carbohydrates"],
                row["fat"], row["fiber"], row["sugars"],
                row["sodium"], row["cholesterol"], row["water_intake"]
            ))

        execute_values(cursor, """
            INSERT INTO nutrition_logs (
                food_id, meal_type_id,
                calories, protein, carbohydrates, fat,
                fiber, sugars, sodium, cholesterol, water_intake
            ) VALUES %s
        """, nl_data)

        print(f"[LOAD] {len(nl_data)} nutrition_logs insérés")

        conn.commit()
        print("[LOAD] Toutes les données insérées avec succès")

    except Exception as e:
        conn.rollback()
        print(f"[LOAD] Erreur : {e}")
        raise

    finally:
        cursor.close()
        conn.close()