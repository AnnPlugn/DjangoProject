import os
import joblib
from catboost import CatBoostRegressor
import pandas as pd
from datetime import datetime
import logging
import numpy as np

# Настройка логирования
logger = logging.getLogger(__name__)
MODEL_PATH = os.path.join(os.getcwd(), "data", "property_model.cb")
ENCODERS_PATH = os.path.join(os.getcwd(), "data", "label_encoders.pkl")
print(MODEL_PATH)
print(ENCODERS_PATH)

# Check if the model file exists and raise an error if not
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file {MODEL_PATH} does not exist")

# Загрузка модели CatBoost
model = CatBoostRegressor()
model.load_model(MODEL_PATH)

def preprocess_new_data(property_data: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocess new property data with proper handling of categorical features.

    Args:
        property_data: Raw property data as DataFrame or dict

    Returns:
        Preprocessed DataFrame ready for prediction
    """
    try:
        # Convert to DataFrame if needed
        if not isinstance(property_data, pd.DataFrame):
            df = pd.DataFrame([property_data])
        else:
            df = property_data.copy()

        logger.info(f"Input data shape: {df.shape}")

        # 1. Clean numeric columns
        numeric_cols = ["living_meters", "kitchen_meters", "min_to_metro"]
        for col in numeric_cols:
            if col in df.columns:
                if df[col].dtype == "object":
                    df[col] = (
                        df[col]
                        .astype(str)
                        .str.replace(r"[^\d.]", "", regex=True)
                        .replace("", np.nan)
                    )
                df[col] = pd.to_numeric(df[col], errors="coerce")
                df[col] = df[col].fillna(-1)

        # 2. Process year and completion status
        if "year_of_construction" in df.columns:
            df["year_of_construction"] = pd.to_numeric(
                df["year_of_construction"], errors="coerce"
            )
            current_year = datetime.now().year
            df["is_completed"] = np.where(
                (df["year_of_construction"].notna())
                & (df["year_of_construction"] <= current_year)
                & (df["year_of_construction"] > 0),
                1,
                0,
            )
            df["age_of_building"] = current_year - df["year_of_construction"].fillna(
                current_year
            )

        # 3. Feature engineering
        if all(col in df.columns for col in ["kitchen_meters", "total_meters"]):
            df["kitchen_to_total_ratio"] = df["kitchen_meters"] / df[
                "total_meters"
            ].replace(0, 1)

        if all(col in df.columns for col in ["living_meters", "rooms_count"]):
            df["meters_per_room"] = df["living_meters"] / df["rooms_count"].replace(0, 1)

        if all(col in df.columns for col in ["total_meters", "price"]):
            df["price_per_meter"] = df["price"] / df["total_meters"].replace(0, 1)

        # Загрузка энкодеров
        loaded_encoders = joblib.load(ENCODERS_PATH)

        # Handle categorical features
        cat_cols = ["district", "street", "underground"]
        for col in cat_cols:
            if col in df.columns:
                if col in loaded_encoders:
                    df[col] = df[col].astype(str)
                    encoder = loaded_encoders[col]
                    df[col] = df[col].apply(
                        lambda x: x if x in encoder.classes_ else "unknown"
                    )
                    if "unknown" not in encoder.classes_:
                        new_classes = list(encoder.classes_) + ["unknown"]
                        encoder.classes_ = np.array(new_classes)
                    df[col] = encoder.transform(df[col])
                else:
                    df[col] = 0
            else:
                df[col] = 0

        # 5. Ensure all expected features exist
        expected_features = [
            "floor",
            "floors_count",
            "rooms_count",
            "total_meters",
            "year_of_construction",
            "living_meters",
            "kitchen_meters",
            "district",
            "street",
            "underground",
            "age_of_building",
            "kitchen_to_total_ratio",
            "meters_per_room",
            "price_per_meter",
            "min_to_metro",
            "is_completed",
        ]

        for feat in expected_features:
            if feat not in df.columns:
                if feat in ["kitchen_to_total_ratio", "meters_per_room"]:
                    df[feat] = 0.3
                elif feat == "age_of_building":
                    df[feat] = 20
                else:
                    df[feat] = -1

        pd.set_option("display.max_columns", None)
        pd.set_option("display.expand_frame_repr", False)
        pd.set_option("display.width", None)

        # Логирование данных
        logger.info("Processed features:\n" + str(df[expected_features].head()))
        return df[expected_features]

    except Exception as e:
        logger.error(f"Error in preprocessing: {str(e)}", exc_info=True)
        raise

def predict_price(property_data):
    """Predict property price with proper error handling."""
    try:
        # Preprocess data
        features = preprocess_new_data(property_data)

        # Ensure correct format for CatBoost
        if isinstance(features, pd.Series):
            features = features.to_frame().T

        # Convert categorical features to int (CatBoost requirement)
        cat_cols = ["district", "street", "underground"]
        for col in cat_cols:
            if col in features.columns:
                features[col] = features[col].astype(int)

        # Predict
        predicted_price = model.predict(features)
        return predicted_price[0]

    except Exception as e:
        logger.error(f"Prediction error: {str(e)}", exc_info=True)
        return 5_000_000  # Default fallback price