import requests

url = 'https://hdmn.cloud/ru/demo/'

# Ссылка на GIF-анимацию
animated_checkmark_url = 'https://drive.google.com/file/d/1ydbK21IHcyr1WM4oqIYB5tPTds7ex1qn/view?usp=sharing'

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
                print(f'\033[1;32m<img src="{animated_checkmark_url}" alt="Animated Checkmark"> Ваш код уже в пути!\033[0m Проверьте свой почтовый ящик.')
            else:
                print('❌ \033[1;31mУказанная почта не подходит для получения тестового периода.\033[0m')
        else:
            print('⚠️ \033[1;31mНа странице не найдено нужного текста. Проверьте доступность страницы.\033[0m')
    else:
        print(f"⚠️ \033[1;31mОшибка при запросе к странице.\033[0m Код ответа: {response.status_code}")
        
except requests.RequestException as e:
    print(f"\033[1;31mОшибка при запросе к сайту:\033[0m {e}")
