from extractors.extractor_diet_recommendations_dataset import extract_diet_recommendations
from transformers.transformer_diet_recommendations_dataset import transform_diet_recommendations
from loaders.loader_diet_recommendations_dataset import load_diet_recommendations

from extractors.extractor_gym_members import extract_gym_members
from transformers.transformer_gym_members import transform_gym_members
from loaders.loader_gym_members import load_gym_members

#DIET_CSV_PATH = "datasets/diet_recommendations_dataset.csv"
GYM_CSV_PATH  = "datasets/gym_members_exercise_tracking_synthetic_data.csv"

'''def run_diet_pipeline():
    print("\n=== ETL diet_recommendations_dataset ===")
    df     = extract_diet_recommendations(DIET_CSV_PATH)
    tables = transform_diet_recommendations(df)
    load_diet_recommendations(tables)
    print("=== Pipeline terminé ===\n")'''

def run_gym_pipeline():
    print("\n=== ETL gym_members_exercise_tracking ===")
    df     = extract_gym_members(GYM_CSV_PATH)
    tables = transform_gym_members(df)
    load_gym_members(tables)
    print("=== Pipeline terminé ===\n")

if __name__ == "__main__":
    #run_diet_pipeline()
    run_gym_pipeline()