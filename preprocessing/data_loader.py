import os
import numpy as np


# Find the main OrbitGuard project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dataset locations
TRAIN_DIR = os.path.join(BASE_DIR, "data", "raw", "train")
TEST_DIR = os.path.join(BASE_DIR, "data", "raw", "test")


def load_telemetry(file_path):
    """Load one telemetry .npy file."""
    data = np.load(file_path)

    print(f"Loaded: {os.path.basename(file_path)}")
    print(f"Shape: {data.shape}")
    print(f"Data type: {data.dtype}")

    return data


def get_train_files():
    """Get all training telemetry files."""
    return sorted(
        os.path.join(TRAIN_DIR, file)
        for file in os.listdir(TRAIN_DIR)
        if file.endswith(".npy")
    )


def get_test_files():
    """Get all testing telemetry files."""
    return sorted(
        os.path.join(TEST_DIR, file)
        for file in os.listdir(TEST_DIR)
        if file.endswith(".npy")
    )


if __name__ == "__main__":

    print("=== OrbitGuard Dataset Check ===")

    # Get training and testing files
    train_files = get_train_files()
    test_files = get_test_files()

    print(f"\nTraining files: {len(train_files)}")
    print(f"Testing files: {len(test_files)}")

    # Check first training file
    if train_files:
        print("\n--- Training Dataset ---")
        train_data = load_telemetry(train_files[0])

    # Check first testing file
    if test_files:
        print("\n--- Testing Dataset ---")
        test_data = load_telemetry(test_files[0])

    print("\n=== Dataset check completed successfully ===")
