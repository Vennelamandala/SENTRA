import os
import numpy as np
from sklearn.preprocessing import StandardScaler


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TRAIN_DIR = os.path.join(BASE_DIR, "data", "raw", "train")
TEST_DIR = os.path.join(BASE_DIR, "data", "raw", "test")

PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")


def clean_data(data):
    """Clean invalid and missing telemetry values."""

    data = data.astype(np.float32)

    # Replace infinite values with NaN
    data[~np.isfinite(data)] = np.nan

    # Calculate mean for each feature
    column_means = np.nanmean(data, axis=0)

    # Replace invalid means with zero
    column_means = np.nan_to_num(column_means, nan=0.0)

    # Find missing values
    rows, columns = np.where(np.isnan(data))

    # Replace missing values with column mean
    for row, column in zip(rows, columns):
        data[row, column] = column_means[column]

    return data


def fit_scaler(data):
    """Fit a scaler for one telemetry file."""

    scaler = StandardScaler()

    data = clean_data(data)

    scaler.fit(data)

    return scaler


def preprocess_file(input_path, output_path):
    """Preprocess one telemetry file."""

    data = np.load(input_path)

    print(
        f"Processing {os.path.basename(input_path)} "
        f"shape={data.shape}"
    )

    # Clean data
    data = clean_data(data)

    # Create a scaler specifically for this file
    scaler = fit_scaler(data)

    # Normalize
    data = scaler.transform(data)

    # Save processed data
    np.save(output_path, data.astype(np.float32))


def process_folder(input_dir, output_dir):

    os.makedirs(output_dir, exist_ok=True)

    files = sorted(
        file for file in os.listdir(input_dir)
        if file.endswith(".npy")
    )

    print(f"\nFound {len(files)} files.")

    for file in files:

        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file)

        preprocess_file(input_path, output_path)


def process_dataset():

    train_output = os.path.join(PROCESSED_DIR, "train")
    test_output = os.path.join(PROCESSED_DIR, "test")

    print("=== OrbitGuard Preprocessing ===")

    print("\n--- Training Data ---")
    process_folder(TRAIN_DIR, train_output)

    print("\n--- Testing Data ---")
    process_folder(TEST_DIR, test_output)

    print("\n=== Preprocessing Completed Successfully ===")

    print(f"\nProcessed training data:")
    print(train_output)

    print(f"\nProcessed testing data:")
    print(test_output)


if __name__ == "__main__":
    process_dataset()
