import argparse
import os
import pickle
import sys
import tempfile

import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    confusion_matrix,
    ConfusionMatrixDisplay,
)
from sklearn.pipeline import Pipeline
from clearml import Dataset, OutputModel, Task

sys.path.insert(0, os.getcwd())

from src.config import clearml_settings, dataset_settings
from src.utils.csv_worker import CSVWorker
from src.utils.git_command import get_git_commit


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max_features", type=int, default=1000, help="Count Vectorizer max features"
    )
    parser.add_argument(
        "--ngram_min", type=int, default=1, help="Count Vectorizer ngram range min"
    )
    parser.add_argument(
        "--ngram_max", type=int, default=2, help="Count Vectorizer ngram range max"
    )
    parser.add_argument(
        "--n_estimators", type=int, default=100, help="RandomForest n_estimators"
    )
    parser.add_argument(
        "--max_depth", type=int, default=30, help="RandomForest max depth"
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run locally without remote execution",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    task = Task.init(
        project_name=clearml_settings.project_name,
        task_name=clearml_settings.train_task_name,
        task_type=Task.TaskTypes.training,
        reuse_last_task_id=False,
    )

    # task.set_script(entry_point="train_model.py")

    # Logging hyperparams for saving and editing in ClearML UI
    hyperparams = {
        "max_features": args.max_features,
        "ngram_min": args.ngram_min,
        "ngram_max": args.ngram_max,
        "n_estimators": args.n_estimators,
        "max_depth": args.max_depth,
    }
    task.connect(hyperparams, name="hyperparameters")

    git_commit = get_git_commit()
    if git_commit:
        task.set_parameter("git/commit", git_commit)
        print(f"Commit ID: {git_commit}")

    # If no --local, only add task in the queue for the agent and exit.
    if not args.local:
        print(f"Add task to queue: {clearml_settings.queue_name}")
        task.execute_remotely(
            queue_name=clearml_settings.queue_name,
            clone=False,
            exit_process=True,
        )

    logger = task.get_logger()

    dataset_id, dataset_version, x_train, y_train, x_test, y_test = get_dataset()

    # Log dataset metadata for reproducibility
    task.set_parameter("dataset/id", dataset_id)
    task.set_parameter("dataset/version", str(dataset_version))

    model = train_model(hyperparams, x_train, y_train)

    accuracy, f1 = validate_model(task, logger, model, x_test, y_test)

    model_id = save_model(task, model, accuracy, f1, hyperparams)

    print(f"\nTraining completed. Model saved with id: {model_id}")
    print(f"  Accuracy:       {accuracy:.3}")
    print(f"  F1:             {f1:.3f}")


def get_dataset():
    print("Loading dataset from ClearML...")
    dataset = Dataset.get(
        dataset_project=clearml_settings.project_name,
        dataset_name=dataset_settings.dataset_name,
        only_completed=True,
        only_published=False,
    )
    dataset_path = dataset.get_local_copy()

    train_path = os.path.join(dataset_path, "train.csv")
    test_path = os.path.join(dataset_path, "test.csv")

    X_train, y_train = CSVWorker.load(train_path)
    X_test, y_test = CSVWorker.load(test_path)
    print(
        f"Dataset loaded. Train set: {len(X_train)} samples, test set: {len(X_test)} samples"
    )

    return dataset.id, dataset.version, X_train, y_train, X_test, y_test


def train_model(hyperparams: dict, X, Y):
    print("Training model with specified hyperparams...")
    pipeline = Pipeline(
        [
            (
                "count",
                CountVectorizer(
                    max_features=hyperparams["max_features"],
                    ngram_range=(hyperparams["ngram_min"], hyperparams["ngram_max"]),
                ),
            ),
            (
                "clf",
                RandomForestClassifier(
                    n_estimators=hyperparams.get("n_estimators", 100),
                    max_depth=hyperparams.get("max_depth", None),
                    random_state=42,
                ),
            ),
        ]
    )
    pipeline.fit(X, Y)

    return pipeline


def validate_model(task, logger, model, x_test, y_test):
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    f1_score_res = f1_score(y_test, y_pred, average="macro")

    print(f"Metrics\nAccuracy: {accuracy:.3f}")
    print(f"F1:       {f1_score_res:.3f}")

    logger.report_scalar("metrics", "accuracy", iteration=0, value=accuracy)
    logger.report_scalar("metrics", "f1", iteration=0, value=f1_score_res)

    log_confusion_matrix(task, y_test, y_pred)

    return accuracy, f1_score_res


def log_confusion_matrix(task: Task, y_true, y_pred):
    labels = list(set(y_true))
    cm = confusion_matrix(y_true, y_pred)

    task.get_logger().report_confusion_matrix(
        title="Confusion Matrix",
        series="test",
        matrix=cm,
        xaxis="Pred",
        yaxis="Actual",
        xlabels=labels,
        ylabels=labels,
        iteration=0,
    )

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    fig, ax = plt.subplots(figsize=(6, 5))
    disp.plot(ax=ax, colorbar=False)
    ax.set_title("Confusion Matrix")
    plt.tight_layout()

    tmp_path = os.path.join(tempfile.gettempdir(), "confusion_matrix.png")
    fig.savefig(tmp_path, dpi=100)
    task.get_logger().report_image(
        title="Confusion Matrix",
        series="test",
        local_path=tmp_path,
        iteration=0,
    )
    plt.close(fig)


def save_model(task, model, accuracy, f1, hyperparams):
    model_path = os.path.join(tempfile.gettempdir(), "model.pkl")
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    # MUST HAVE for 3-rd stage. OutputModel => Models tab => Registry
    output_model = OutputModel(
        task=task,
        framework="scikit-learn",
        name="news-classifier",
    )
    output_model.update_weights(
        weights_filename=model_path,
        target_filename="model.pkl",
        auto_delete_file=False,
        iteration=0,
        upload_uri=clearml_settings.file_server,
    )
    output_model.tags = [
        f"n_estimators={hyperparams['n_estimators']}",
        f"max_depth={hyperparams['max_depth']}",
        f"max_features={hyperparams['max_features']}",
        f"f1={f1:.3f}",
        f"accuracy={accuracy:.3f}",
    ]

    # Save model artifact
    task.upload_artifact(
        name="model",
        artifact_object=model_path,
        metadata={
            "accuracy": round(accuracy, 3),
            "f1": round(f1, 3),  # type: ignore
            "output_model_id": output_model.id,
        },
    )

    return output_model.id


if __name__ == "__main__":
    main()
