import os
import requests
import subprocess
import sys
from dotenv import load_dotenv

# Проверяем и устанавливаем python-dotenv при необходимости
try:
    import dotenv
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv"])
    import dotenv  # Повторный импорт после установки

# Проверяем, выполняется ли скрипт в Google Colab
try:
    from google.colab import drive
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# Подключаем Google Drive (если в Colab)
if IN_COLAB:
    drive.mount('/content/drive')
    env_path = '/content/drive/MyDrive/Colab/.env'  # Убедитесь, что путь правильный
else:
    env_path = '.env'  # Используем локальный .env файл

# Загружаем переменные из .env файла
load_dotenv(env_path)

# Проверяем, загрузилась ли переменная
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена в .env файле.")

# ID канала (замените на реальный ID)
CHANNEL_ID = -1001234567890

# Получить user_id по username
def get_user_id(username):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat'
    params = {
        'chat_id': username
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        user_id = data.get('result', {}).get('id')
        return user_id
    return None

# Проверка подписки на канал
def check_subscription(user_id):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember'
    params = {
        'chat_id': CHANNEL_ID,  # Используем ID канала
        'user_id': user_id
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        status = data.get('result', {}).get('status')
        if status in ['member', 'administrator', 'creator']:
            return True
    return False

# Основная логика скрипта
def main():
    username = input('Введите ваш Telegram username (например, @username): ')
    
    # Получаем user_id
    user_id = get_user_id(username)
    if not user_id:
        print('❌\033[1;31mНе удалось получить ваш user_id. Убедитесь, что username корректен.\033[0m')
        return
    
    # Проверяем подписку
    if not check_subscription(user_id):
        print('❌\033[1;31mВы не подписаны на канал.\033[0m')
        return
    
    url = 'https://hdmn.cloud/ru/demo/'
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            if 'Ваша электронная почта' in response.text:
                email = input('Введите электронную почту для получения тестового периода: ')
                response = requests.post('https://hdmn.cloud/ru/demo/success/', data={
                    "demo_mail": f"{email}"
                })

                if 'Ваш код выслан на почту' in response.text:
                    print('✅\033[1;32mВаш код уже в пути!\033[0m Проверьте свой почтовый ящик.')
                else:
                    print('❌\033[1;31mУказанная почта не подходит для получения тестового периода.\033[0m')
            else:
                print('⚠️\033[1;31mНа странице не найдено нужного текста. Проверьте доступность страницы.\033[0m')
        else:
            print(f"⚠️\033[1;31mОшибка при запросе к странице.\033[0m Код ответа: {response.status_code}")
        
    except requests.RequestException as e:
        print(f"\033[1;31mОшибка при запросе к сайту:\033[0m {e}")

if __name__ == '__main__':
    main()
