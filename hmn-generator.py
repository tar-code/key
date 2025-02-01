import requests

def handle_success(response):
    """Обработка успешного ответа."""
    success_message = """
    ✅ Ваш код уже в пути! Проверьте свой почтовый ящик.
    Подробнее об использовании кода: https://example.com/instructions
    """
    print(success_message)

def handle_error(error_type, error_message=None):
    """Обработка ошибок."""
    if error_type == "invalid_email":
        error_message = """
        ⚠️ Указанная почта не подходит для получения тестового периода.
        Инструкция по вводу корректной почты: https://example.com/email-instruction
        """
    elif error_type == "page_not_found":
        error_message = """
        ⚠️ На странице не найдено нужного текста.
        Проверьте доступность страницы: https://hdmn.cloud/ru/demo/
        """
    elif error_type == "request_error":
        error_message = f"""
        ❌ Ошибка при запросе к странице. Код ответа: {error_message}
        Инструкции по устранению проблемы: https://example.com/error-instructions
        """
    elif error_type == "site_request_error":
        error_message = f"""
        ❌ Ошибка при запросе к сайту: {error_message}
        Проверьте подключение к интернету или попробуйте позже.
        """
    print(f"\033[1;31m{error_message}\033[0m")

url = 'https://hdmn.cloud/ru/demo/'

# Попытка получить страницу и проверить статус ответа
try:
    response = requests.get(url)
    
    # Проверка на успешный ответ от сервера
    if response.status_code == 200:
        # Если текст на странице содержит "Ваша электронная почта", продолжаем
        if 'Ваша электронная почта' in response.text:
            email = input('Введите электронную почту для получения тестового периода: ')

            response = requests.post('https://hdmn.cloud/ru/demo/success/', data={
                "demo_mail": f"{email}"
            })

            if 'Ваш код выслан на почту' in response.text:
                handle_success(response)
            else:
                handle_error("invalid_email")
        else:
            handle_error("page_not_found")
    else:
        handle_error("request_error", response.status_code)
        
except requests.RequestException as e:
    handle_error("site_request_error", e)
