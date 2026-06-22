from src.classification import classify_news
from src.main_page import get_page
from config import web_settings as settings


if __name__ == "__main__":
    app = get_page(classify_news_func=classify_news)
    app.launch(
        server_name="0.0.0.0", server_port=settings.app_port, share=False, debug=False
    )
