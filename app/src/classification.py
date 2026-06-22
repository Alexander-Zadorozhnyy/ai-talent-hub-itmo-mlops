import json
import time

import requests

from config import web_settings as settings
from src.topics import TOPICS_MAP, get_topic_info


def classify_news(text):
    """
    Отправляет запрос к API модели и возвращает результат с визуальным оформлением
    """
    if not text or text.strip() == "":
        return (
            "⚠️ Введите текст новости",
            "0 ms",
            """
            <div style='padding: 20px; text-align: center; background: #f8f9fa; border-radius: 10px;'>
                <p style='color: #6c757d; font-size: 16px;'>Пожалуйста, введите текст новости для классификации</p>
            </div>
            """,
        )

    start_time = time.time()

    try:
        payload = {"text": text}
        headers = {"Content-Type": "application/json"}

        response = requests.post(
            settings.api_url, json=payload, headers=headers, timeout=settings.timeout
        )

        latency = (time.time() - start_time) * 1000  # в миллисекундах

        if response.status_code == 200:
            result = response.json()

            # Извлечение предсказанной темы
            predicted_label = result.get("label", "UNKNOWN")

            topic_info = get_topic_info(predicted_label)
            emoji = topic_info["emoji"]
            color = topic_info["color"]

            is_unknown = predicted_label not in TOPICS_MAP

            # Создание визуального блока
            if is_unknown:
                html_output = f"""
                <div style='padding: 20px; background: #fff3cd; border-radius: 15px; border-left: 5px solid #ffc107; margin: 10px 0;'>
                    <div style='display: flex; align-items: center; gap: 15px;'>
                        <div style='font-size: 48px;'>⚠️</div>
                        <div style='flex: 1;'>
                            <h2 style='margin: 0; color: #856404; font-size: 20px;'>
                                НЕИЗВЕСТНАЯ ТЕМА
                            </h2>
                            <p style='margin: 5px 0 0 0; color: #856404; font-size: 14px;'>
                                Модель предсказала: "{predicted_label}"
                            </p>
                            <p style='margin: 5px 0 0 0; color: #856404; font-size: 13px;'>
                                ⚠️ Эта тема отсутствует в списке известных категорий
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span style='background: #ffc107; color: #856404; padding: 5px 15px; 
                                       border-radius: 20px; font-size: 14px; font-weight: bold;'>
                                {latency:.1f} ms
                            </span>
                        </div>
                    </div>
                </div>
                """
                label_text = f"⚠️ {predicted_label} (неизвестная тема)"
            else:
                html_output = f"""
                <div style='padding: 20px; background: linear-gradient(135deg, {color}22, {color}44); 
                            border-radius: 15px; border-left: 5px solid {color}; margin: 10px 0;'>
                    <div style='display: flex; align-items: center; gap: 15px;'>
                        <div style='font-size: 48px;'>{emoji}</div>
                        <div style='flex: 1;'>
                            <h2 style='margin: 0; color: {color}; font-size: 24px;'>
                                {predicted_label}
                            </h2>
                            <p style='margin: 5px 0 0 0; color: #555; font-size: 14px;'>
                                Тема новости успешно определена
                            </p>
                        </div>
                        <div style='text-align: right;'>
                            <span style='background: {color}; color: white; padding: 5px 15px; 
                                       border-radius: 20px; font-size: 14px; font-weight: bold;'>
                                {latency:.1f} ms
                            </span>
                        </div>
                    </div>
                </div>
                """
                label_text = f"{emoji} {predicted_label}"

            return (label_text, f"{latency:.1f} ms", html_output)
        else:
            error_msg = f"Ошибка сервера: {response.status_code}"
            html_output = f"""
            <div style='padding: 20px; background: #fee; border-radius: 10px; border-left: 5px solid #e74c3c;'>
                <p style='color: #c0392b; margin: 0;'><strong>❌ Ошибка:</strong> {error_msg}</p>
                <p style='color: #666; font-size: 14px; margin: 5px 0 0 0;'>
                    Ответ сервера: {response.text[:100] if response.text else "Нет тела ответа"}
                </p>
                <p style='color: #666; font-size: 14px; margin: 5px 0 0 0;'>
                    Проверьте, что модель запущена и доступна
                </p>
            </div>
            """
            return (f"❌ {error_msg}", f"{latency:.1f} ms", html_output)

    except requests.exceptions.ConnectionError:
        latency = (time.time() - start_time) * 1000
        html_output = f"""
        <div style='padding: 20px; background: #fee; border-radius: 10px; border-left: 5px solid #e74c3c;'>
            <p style='color: #c0392b; margin: 0;'><strong>❌ Ошибка подключения:</strong></p>
            <p style='color: #666; font-size: 14px; margin: 5px 0 0 0;'>
                Не удалось подключиться к серверу по адресу <code>{settings.api_url}</code><br>
                Убедитесь, что модель запущена и сервер работает
            </p>
            <p style='color: #666; font-size: 13px; margin: 10px 0 0 0;'>
                💡 Попробуйте проверить:<br>
                1. Запущен ли сервер с моделью<br>
                2. Правильный ли порт (8082)<br>
                3. Доступен ли эндпоинт {settings.api_url}
            </p>
        </div>
        """
        return ("❌ Endpoint недоступен", f"{latency:.1f} ms", html_output)
    except requests.exceptions.Timeout:
        latency = (time.time() - start_time) * 1000
        html_output = f"""
        <div style='padding: 20px; background: #fff3cd; border-radius: 10px; border-left: 5px solid #ffc107;'>
            <p style='color: #856404; margin: 0;'><strong>⏱️ Таймаут:</strong></p>
            <p style='color: #666; font-size: 14px; margin: 5px 0 0 0;'>
                Сервер не ответил за {settings.timeout} секунд
            </p>
            <p style='color: #666; font-size: 13px; margin: 5px 0 0 0;'>
                Попробуйте позже или проверьте загрузку сервера
            </p>
        </div>
        """
        return ("⏱️ Таймаут запроса", f"{latency:.1f} ms", html_output)
    except json.JSONDecodeError as e:
        latency = (time.time() - start_time) * 1000
        html_output = f"""
        <div style='padding: 20px; background: #fee; border-radius: 10px; border-left: 5px solid #e74c3c;'>
            <p style='color: #c0392b; margin: 0;'><strong>❌ Ошибка JSON:</strong></p>
            <p style='color: #666; font-size: 14px; margin: 5px 0 0 0;'>
                Не удалось обработать ответ сервера
            </p>
            <p style='color: #666; font-size: 13px; margin: 5px 0 0 0;'>
                {str(e)}
            </p>
        </div>
        """
        return ("❌ Ошибка парсинга ответа", f"{latency:.1f} ms", html_output)
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        html_output = f"""
        <div style='padding: 20px; background: #fee; border-radius: 10px; border-left: 5px solid #e74c3c;'>
            <p style='color: #c0392b; margin: 0;'><strong>❌ Непредвиденная ошибка:</strong></p>
            <p style='color: #666; font-size: 14px; margin: 5px 0 0 0;'>{str(e)}</p>
        </div>
        """
        return (f"❌ Ошибка: {str(e)[:50]}", f"{latency:.1f} ms", html_output)
