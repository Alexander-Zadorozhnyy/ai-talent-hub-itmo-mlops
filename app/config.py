from pydantic_settings import BaseSettings


class WebSettings(BaseSettings):
    api_url: str = "http://localhost:8083/serve/news-classifier"
    timeout: int = 10

    app_port: int = 7860


web_settings = WebSettings()
