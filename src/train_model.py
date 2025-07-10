
import argparse
import logging
from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from joblib import dump

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def train_model(data_path: Path, models_dir: Path):
    """
    Trains a model on the given data and saves it to the models' directory.
    """
    logging.info("Starting model training...")

    # Create models directory if it doesn't exist
    models_dir.mkdir(exist_ok=True)

    # Load the dataset
    logging.info(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)

    # Assume the last column is the target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    logging.info(f"Data split into training and testing sets. Train shape: {X_train.shape}, Test shape: {X_test.shape}")

    # Train a simple Logistic Regression model
    logging.info("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Model accuracy: {acc:.4f}")

    # Save the model
    model_path = models_dir / "model.joblib"
    logging.info(f"Saving model to {model_path}")
    dump(model, model_path)
    logging.info("Model training finished.")


def main():
    parser = argparse.ArgumentParser(description="Train a machine learning model.")
    parser.add_argument("--data_path", type=str, default="data/diabetes.csv", help="Path to the training data.")
    parser.add_argument("--models_dir", type=str, default="models", help="Directory to save the trained model.")
    args = parser.parse_args()

    base_dir = Path(__file__).parent.parent
    data_path = base_dir / args.data_path
    models_dir = base_dir / args.models_dir

    train_model(data_path, models_dir)


if __name__ == "__main__":
    main()

