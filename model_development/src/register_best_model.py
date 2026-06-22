import argparse
import os
import sys

from clearml import Task
from clearml.model import Model

sys.path.insert(0, os.getcwd())

from src.config import clearml_settings


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--metric",
        type=str,
        default="f1",
        help="Possible metric for choice best model",
        choices=["f1", "accuracy"],
    )
    return parser.parse_args()


def main():
    args = parse_args()

    best_task = find_trained_model(args.metric)
    register_model(best_task)


def find_trained_model(metric: str):
    tasks = Task.get_tasks(
        project_name=clearml_settings.project_name,
        task_name=clearml_settings.train_task_name,
        task_filter={"status": ["completed"]},
    )

    if not tasks:
        raise ValueError(
            "No completed training tasks found. Please run the training stage."
        )

    best_task = None
    best_metric = -1.0

    for task in tasks:
        scalars = task.get_last_scalar_metrics()
        try:
            metric_value = scalars["metrics"][metric]["last"]
        except Exception:
            print(f"Metric {metric} for task {task.id} not found. Skipping...")
            continue

        if metric_value > best_metric:
            best_metric = metric_value
            best_task = task

    if best_task is None:
        raise ValueError(f"No valid tasks with metric '{metric}' found.")

    print(f"\nBest: {best_task.id=}, {metric}:{best_metric}")
    return best_task


def register_model(best_task: Task):
    task_models = best_task.get_models()
    output_models = task_models.get("output", [])

    if not output_models:
        raise ValueError(f"Task {best_task.id} does not have OutputModel.")

    output_model = output_models[0]
    model = Model(model_id=output_model.id)

    model_params = best_task.get_parameters_as_dict()
    hyperparameters = model_params.get("hyperparameters", {})

    scalars = best_task.get_last_scalar_metrics()
    f1_score = scalars.get("metrics", {}).get("f1", {}).get("last", None)
    accuracy = scalars.get("metrics", {}).get("accuracy", {}).get("last", None)

    model.tags = [
        f"f1={f1_score:.3f}",
        f"accuracy={accuracy:.3f}",
        f"n_estimators={hyperparameters.get('n_estimators', 'unknown')}",
        f"max_depth={hyperparameters.get('max_depth', 'unknown')}",
        "news_classification",
        "sklearn",
    ]
    model.name = clearml_settings.register_model_name
    model.publish()

    print(
        f"\nModel with id={output_model.id} registered by name {clearml_settings.register_model_name}."
    )


if __name__ == "__main__":
    main()
