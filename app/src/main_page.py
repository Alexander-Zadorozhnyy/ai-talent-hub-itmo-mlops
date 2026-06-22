from typing import Callable

import gradio as gr

from src.topics import TOPICS_MAP
from config import web_settings as settings


def get_page(classify_news_func: Callable):
    with gr.Blocks(
        title="Классификатор новостей",
        theme=gr.themes.Soft(),
        css="""
            .gradio-container {
                max-width: 900px;
                margin: auto;
            }
            .input-text textarea {
                font-size: 16px !important;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            .output-label {
                font-size: 20px !important;
                font-weight: bold;
            }
            .latency-text {
                font-size: 18px !important;
                font-weight: 600;
                color: #2C3E50;
            }
            .main-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
                border-radius: 15px;
                color: white;
                margin-bottom: 20px;
            }
            .stats-box {
                background: #f8f9fa;
                padding: 10px 15px;
                border-radius: 10px;
                border: 1px solid #e9ecef;
            }
            .category-badge {
                display: inline-block;
                padding: 3px 10px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
                margin: 2px;
            }
        """,
    ) as demo:
        gr.HTML("""
        <div class="main-header">
            <h1 style="margin: 0; font-size: 32px;">📰 Классификатор тем новостей</h1>
            <p style="margin: 5px 0 0 0; opacity: 0.9; font-size: 16px;">
                Модель определяет тему новости из 42 категорий
            </p>
        </div>
        """)

        with gr.Row():
            with gr.Column():
                gr.HTML("""
                <div style="display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 15px;">
                    <span class="category-badge" style="background:#2E86C1;color:white;">U.S. NEWS</span>
                    <span class="category-badge" style="background:#27AE60;color:white;">GOOD NEWS</span>
                    <span class="category-badge" style="background:#E74C3C;color:white;">DIVORCE</span>
                    <span class="category-badge" style="background:#1ABC9C;color:white;">WELLNESS</span>
                    <span class="category-badge" style="background:#F39C12;color:white;">WEIRD NEWS</span>
                    <span class="category-badge" style="background:#3498DB;color:white;">TECH</span>
                    <span class="category-badge" style="background:#8E44AD;color:white;">SCIENCE</span>
                    <span class="category-badge" style="background:#E91E63;color:white;">ENTERTAINMENT</span>
                    <span class="category-badge" style="background:#2C3E50;color:white;">POLITICS</span>
                    <span class="category-badge" style="background:#607D8B;color:white;">BUSINESS</span>
                    <span class="category-badge" style="background:#FF6B6B;color:white;">+32 других</span>
                </div>
                """)

        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(
                    label="📝 Введите текст новости",
                    placeholder="Например: 'The new iPhone was released today with amazing features...'",
                    lines=4,
                    elem_classes="input-text",
                )

                with gr.Row():
                    predict_btn = gr.Button("🔮 Predict", variant="primary", size="lg")
                    clear_btn = gr.Button("🗑️ Очистить", variant="secondary", size="lg")

        with gr.Row():
            with gr.Column(scale=2):
                label_output = gr.Label(
                    label="🏷️ Классификация",
                    value="Ожидание ввода...",
                    elem_classes="output-label",
                )

            with gr.Column(scale=1):
                latency_output = gr.Textbox(
                    label="⏱️ Время ответа",
                    value="0 ms",
                    interactive=False,
                    elem_classes="latency-text",
                )

        html_output = gr.HTML(
            value="""
            <div style='padding: 20px; text-align: center; background: #f8f9fa; border-radius: 10px;'>
                <p style='color: #6c757d; font-size: 16px;'>Введите текст и нажмите "Predict"</p>
            </div>
            """
        )

        with gr.Accordion("📊 Информация о модели", open=False):
            gr.Markdown(f"""
            **Модель**: Классификатор новостей (42 категории)
            
            **Эндпоинт**: {settings.api_url}
            
            **Обработка**:
            - Модель принимает текст и возвращает предсказанную категорию
            - Всего поддерживается 42 категории новостей
            - Если тема неизвестна, будет отображено предупреждение
            """)

            # Дополнительная информация о категориях
            gr.Markdown("### 📋 Полный список категорий:")

            # Создаем таблицу с категориями
            categories_html = "<div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px;'>"
            for category, info in sorted(TOPICS_MAP.items()):
                categories_html += f"""
                <div style='background: {info["color"]}22; padding: 5px 10px; border-radius: 8px; 
                            border-left: 3px solid {info["color"]};'>
                    {info["emoji"]} {category}
                </div>
                """
            categories_html += "</div>"
            gr.HTML(categories_html)

            gr.Markdown("""
            ---
            **⚠️ Примечание**: Если модель вернет категорию, отсутствующую в списке выше, 
            интерфейс отобразит предупреждение о неизвестной теме.
            """)

        predict_btn.click(
            fn=classify_news_func,
            inputs=text_input,
            outputs=[label_output, latency_output, html_output],
        )

        text_input.submit(
            fn=classify_news_func,
            inputs=text_input,
            outputs=[label_output, latency_output, html_output],
        )

        clear_btn.click(
            fn=lambda: (
                "",
                "Ожидание ввода...",
                "0 ms",
                "<div style='padding:20px;text-align:center;background:#f8f9fa;border-radius:10px;'>"
                "<p style='color:#6c757d;font-size:16px;'>Введите текст и нажмите 'Predict'</p></div>",
            ),
            outputs=[text_input, label_output, latency_output, html_output],
        )

    return demo
