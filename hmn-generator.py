import requests
from IPython.display import HTML, display

url = 'https://hdmn.cloud/ru/demo/'

# Ссылки на GIF-анимации
animated_checkmark_url = 'https://i.imgur.com/Uj3xPn5.gif'
animated_cross_url = 'https://i.imgur.com/a7p5Nyb.gif'
animated_warning_url = 'https://i.imgur.com/a7p5Nyb.gif'

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
                # Вывод сообщения с GIF-анимацией вместо обычного символа
                html_message = f'<img src="{animated_checkmark_url}" alt="Animated Checkmark"> Ваш код уже в пути! Проверьте свой почтовый ящик.'
                display(HTML(html_message))
            else:
                # Замена ❌ на GIF-анимацию
                html_message = f'<img src="{animated_cross_url}" alt="Animated Cross"> Указанная почта не подходит для получения тестового периода.'
                display(HTML(html_message))
        else:
            # Замена ⚠️ на GIF-анимацию
            html_message = f'<img src="{animated_warning_url}" alt="Animated Warning"> На странице не найдено нужного текста. Проверьте доступность страницы.'
            display(HTML(html_message))
    else:
        # Замена ⚠️ на GIF-анимацию
        html_message = f'<img src="{animated_warning_url}" alt="Animated Warning"> Ошибка при запросе к странице. Код ответа: {response.status_code}'
        display(HTML(html_message))
        
except requests.RequestException as e:
    # Замена ⚠️ на GIF-анимацию
    html_message = f'<img src="{animated_warning_url}" alt="Animated Warning"> Ошибка при запросе к сайту: {e}'
    display(HTML(html_message))
