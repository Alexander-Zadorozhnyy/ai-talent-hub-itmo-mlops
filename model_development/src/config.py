from pydantic_settings import BaseSettings


class ClearMLSettings(BaseSettings):
    project_name: str = "mlops"
    queue_name: str = "tasks"

    train_task_name: str = "model-training"
    register_model_name: str = "best_news_classifier"

    file_server: str = "http://<IP_ADDRESS>:8081"


class DatasetSettings(BaseSettings):
    dataset_name: str = "news_classification"
    tmp_dataset_dir: str = "./tmp"


clearml_settings = ClearMLSettings()
dataset_settings = DatasetSettings()
