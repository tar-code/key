import os
import requests
import subprocess
import sys

# ✅ Установка python-dotenv, если он не найден
try:
    import dotenv
    from dotenv import load_dotenv
except ImportError:
    print("⚠️ Устанавливаю python-dotenv...")
    subprocess.run([sys.executable, "-m", "pip", "install", "python-dotenv"])
    import dotenv
    from dotenv import load_dotenv

# ✅ Проверяем, выполняется ли скрипт в Google Colab
try:
    from google.colab import drive
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

# ✅ Указываем путь к .env (если в Colab, пробуем Google Drive)
env_path = None

if IN_COLAB:
    try:
        drive.mount('/content/drive')
        env_path = '/content/drive/MyDrive/Colab/.env'  # 🟢 Проверь, что этот путь правильный!
        if not os.path.exists(env_path):
            raise FileNotFoundError("❌ Файл .env не найден в Google Drive!")
    except Exception as e:
        print(f"⚠️ Ошибка при монтировании Google Drive: {e}")
        env_path = None

# Если Google Drive не работает, просим ввести путь вручную
if env_path is None:
    env_path = input("Введите путь к вашему .env файлу (например, /content/.env): ")

# ✅ Загружаем переменные из .env
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    raise ValueError(f"❌ Файл .env не найден! Указанный путь: {env_path}")

# ✅ Проверяем, загружен ли TELEGRAM_BOT_TOKEN
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Переменная TELEGRAM_BOT_TOKEN не найдена в .env файле!")

# ✅ ID канала (замени на реальный)
CHANNEL_ID = -1001234567890  

# ✅ Получить user_id по username
def get_user_id(username):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat'
    params = {'chat_id': username}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        user_id = data.get('result', {}).get('id')
        return user_id
    return None

# ✅ Проверка подписки на канал
def check_subscription(user_id):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChatMember'
    params = {'chat_id': CHANNEL_ID, 'user_id': user_id}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        status = data.get('result', {}).get('status')
        return status in ['member', 'administrator', 'creator']
    return False

# ✅ Основная логика скрипта
def main():
    username = input('Введите ваш Telegram username (например, @username): ')

    # Получаем user_id
    user_id = get_user_id(username)
    if not user_id:
        print('❌ Не удалось получить ваш user_id. Проверьте username.')
        return

    # Проверяем подписку
    if not check_subscription(user_id):
        print('❌ Вы не подписаны на канал.')
        return

    url = 'https://hdmn.cloud/ru/demo/'

    try:
        response = requests.get(url)

        if response.status_code == 200:
            if 'Ваша электронная почта' in response.text:
                email = input('Введите электронную почту для теста: ')
                response = requests.post('https://hdmn.cloud/ru/demo/success/', data={"demo_mail": email})

                if 'Ваш код выслан на почту' in response.text:
                    print('✅ Ваш код уже в пути! Проверьте почтовый ящик.')
                else:
                    print('❌ Почта не подходит для теста.')
            else:
                print('⚠️ На странице не найден нужный текст. Проверьте доступность сайта.')
        else:
            print(f"⚠️ Ошибка при запросе к странице. Код ответа: {response.status_code}")

    except requests.RequestException as e:
        print(f"❌ Ошибка при запросе к сайту: {e}")

if __name__ == '__main__':
    main()
