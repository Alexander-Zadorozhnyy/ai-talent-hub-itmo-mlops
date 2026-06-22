import os
import sys

from clearml import Dataset
from datasets import load_dataset
from sklearn.model_selection import train_test_split

sys.path.insert(0, os.getcwd())

from src.config import clearml_settings, dataset_settings
from src.utils.csv_worker import CSVWorker

RANDOM_STATE = 42
TEST_SIZE = 0.3


def download_dataset():
    print(
        f"Downloading and preprocessing data for {dataset_settings.dataset_name} dataset..."
    )
    ds = load_dataset("heegyu/news-category-dataset")

    os.makedirs(dataset_settings.tmp_dataset_dir, exist_ok=True)

    all_data = [(s["headline"], s["category"]) for s in ds["train"]]

    train_data, test_data = train_test_split(
        all_data, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )

    train_path = os.path.join(dataset_settings.tmp_dataset_dir, "train.csv")
    test_path = os.path.join(dataset_settings.tmp_dataset_dir, "test.csv")

    for path, samples in [(train_path, train_data), (test_path, test_data)]:
        CSVWorker.write(path, samples)

    print(
        f"Preprocess train data: {len(train_data)} elements and write it to: {train_path}"
    )
    print(
        f"Preprocess test data: {len(test_data)} elements and write it to: {test_path}"
    )


def create_dataset():
    print("\nCreating ClearML Dataset...")

    dataset = Dataset.create(
        dataset_name=dataset_settings.dataset_name,
        dataset_project=clearml_settings.project_name,
        dataset_version="1.0",
    )

    # Add files
    dataset.add_files(path=os.path.join(dataset_settings.tmp_dataset_dir, "train.csv"))
    dataset.add_files(path=os.path.join(dataset_settings.tmp_dataset_dir, "test.csv"))

    dataset.add_tags(["news", "classification"])

    # Upload files and fix them
    dataset.upload()
    dataset.finalize()

    print(f"Dataset created with ID:      {dataset.id}")
    print(f"Dataset Version: {dataset.version}")


if __name__ == "__main__":
    download_dataset()
    create_dataset()
    # c65f27626d4a41288b2bfb719dc8b0f3
