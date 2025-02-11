import requests
from IPython import get_ipython

def main():
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
                    print('✅ Ваш код уже в пути! Проверьте свой почтовый ящик.')
                    
                    # Условие успешного завершения задачи
                    restart_kernel()
                else:
                    print('⚠️ Указанная почта не подходит для получения тестового периода.')
            else:
                print('⚠️ На странице не найдено нужного текста. Проверьте доступность страницы.')
        else:
            print(f"❌ Ошибка при запросе к странице. Код ответа: {response.status_code}")
            
    except requests.RequestException as e:
        print(f"❌ Ошибка при запросе к сайту: {e}")

def restart_kernel():
    ip = get_ipython()
    if ip is not None:
        ip.run_line_magic("reset", "-f")
        print("Ядро перезапущено.")

if __name__ == "__main__":
    main()
