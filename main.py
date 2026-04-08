from extractors.extractor_diet_recommendations_dataset import extract_diet_recommendations
from transformers.transformer_diet_recommendations_dataset import transform_diet_recommendations
from loaders.loader_diet_recommendations_dataset import load_diet_recommendations

DIET_CSV_PATH = "datasets/diet_recommendations_dataset.csv"

def run_diet_pipeline():
    print("\n=== ETL diet_recommendations_dataset ===")
    df = extract_diet_recommendations(DIET_CSV_PATH)
    tables = transform_diet_recommendations(df)
    load_diet_recommendations(tables)
    print("=== Pipeline terminé ===\n")

if __name__ == "__main__":
    run_diet_pipeline()