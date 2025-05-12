import requests
import socks
import socket


# Настройка прокси SOCKS5
def _set_socks5_proxy(proxy_host: str, proxy_port: int, username: str = None, password : str =None):
    # Формирование строки прокси с аутентификацией, если указаны логин и пароль
    if username and password:
        proxy_url = f'socks5://{username}:{password}@{proxy_host}:{proxy_port}'
    else:
        proxy_url = f'socks5://{proxy_host}:{proxy_port}'

    socks.set_default_proxy(socks.SOCKS5, proxy_host, proxy_port, True, username, password)
    socket.socket = socks.socksocket

def check_proxy(proxy_host: str, proxy_port: int, username: str =None, password: str = None) -> str or bool:
    original_socket = None
    try:
        original_socket = socket.socket # запоминаем какой сокет был до
        test_url = "http://httpbin.org/ip" # URl с которого будем брать информацию о нашем IP
        _set_socks5_proxy(proxy_host, proxy_port, username, password) # подключаем прокси

        # Отправка запроса с использованием прокси
        response = requests.get(test_url, timeout = 5)

        socket.socket = original_socket # устанавливаем оригинальный сокет
        # Проверка статуса ответа
        if response.status_code == 200:
            response_json = response.json()  # Парсим ответ в формате JSON
            ip_address = response_json.get("origin")  # Извлекаем значение "origin"
            return ip_address
        else:
            return False
    except requests.exceptions.ConnectionError: # если не смогли подключиться к прокси или если с сайтом проверки прокси ошибка
        socket.socket = original_socket
        return False

    except Exception as e:
        socket.socket = original_socket
        return False

# Пример использования
# proxy_host = "45.144.169.213"  # Замените на IP или доменное имя вашего прокси
# proxy_port = 8000          # Укажите порт вашего прокси
# username = "BVJNQe"             # Укажите логин (если есть)
# password = "qXe5aX"             # Укажите пароль (если есть)
#
# print(check_proxy(proxy_host, proxy_port, username, password))