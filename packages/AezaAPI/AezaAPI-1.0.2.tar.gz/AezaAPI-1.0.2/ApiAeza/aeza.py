import requests
import json


class AuthAeza():
    def __init__(self, key: str) -> None:
        self.key = key

    def token(self):
        """Инициализация токена."""
        return self.key

    def get_balance(self) -> float:
        """Получение баланса."""
        responce = requests.get('https://core.aeza.net/api/desktop?',
                                headers={
                                    'authorization': f'Bearer {self.key}'
                                }
                                )
        balance: float = json.loads(
            responce.text)['data']['balance']['value']
        return balance

    def invoice_card(self, amount: int) -> str:
        """Пополнение счёта картой."""
        if amount < 100:
            return 'Минимальная сумма пополнения 100 ₽'
        responce = requests.post('https://core.aeza.net/api/payment/invoices?',
                                 headers={
                                     'authorization': f'Bearer {self.key}'
                                 },
                                 json={
                                     "method": "unitpay:card", "amount": amount
                                 }
                                 )
        link: str = json.loads(responce.text)[
            'data']['transaction']['invoice']['link']
        return link

    def invoice_qiwi(self, amount: int) -> str:
        """Пополнение счёта через Qiwi."""
        if amount < 100:
            return 'Минимальная сумма пополнения 100 ₽'
        responce = requests.post('https://core.aeza.net/api/payment/invoices?',
                                 headers={
                                     'authorization': f'Bearer {self.key}'
                                 },
                                 json={
                                     "method": "lava:qiwi", "amount": amount
                                 }
                                 )
        link: str = json.loads(responce.text)[
            'data']['transaction']['invoice']['link']
        return link

    def status_server(self) -> dict:
        """Проверка статуса серверов."""
        server: dict = {}
        num: int = 0
        responce = requests.get(
            'https://aeza-monitor.cofob.dev/api/status-page/heartbeat/locations').text
        status: float = json.loads(responce)['uptimeList']
        for i in status:
            percent = status[i]
            server[num] = "{:.2f}".format(float(percent))
            num += 1
        return server

    def add_api_key(self, name_key: str) -> str:
        """Создание API-ключа."""
        responce = requests.post('https://core.aeza.net/api/apikeys?',
                                 headers={
                                     'authorization': f'Bearer {self.key}'
                                 },
                                 json={
                                     'name': name_key
                                 }
                                 )
        apikey: str = json.loads(responce.text)['data']['items'][0]['token']
        return apikey

    def get_api_key(self) -> dict:
        """Получение списка API-ключей"""
        apikey: dict = {}
        responce = requests.get('https://core.aeza.net/api/apikeys?',
                                headers={
                                    'authorization': f'Bearer {self.key}'
                                }
                                )
        apikeys: dict = json.loads(responce.text)['data']['items']
        for i in apikeys:
            apikey[i['name']] = i['token']
        return apikey

    def add_ssh_key(self, name, ssh_key) -> str:
        """Добавление SSH-ключа"""
        responce = requests.post('https://core.aeza.net/api/sshkeys?',
                                 headers={
                                     'authorization': f'Bearer {self.key}'
                                 },
                                 json={
                                     'name': name, 'pubKey': ssh_key
                                 }
                                 )
        status = json.loads(responce.text)
        try:
            return status['error']['message']
        except:
            return 'Ключ успешно добавлен'

    def get_ssh_key(self):
        """Получение списка SSH-ключей."""
        sshkey: dict = {}
        responce = requests.get('https://core.aeza.net/api/sshkeys?',
                                headers={
                                    'authorization': f'Bearer {self.key}'
                                }
                                )
        sshkeys: dict = json.loads(responce.text)['data']['items']
        for i in sshkeys:
            sshkey[i['name']] = i['pubKey']
        return sshkey

    def get_my_server(self):
        """Получение информации приобретённых серверов."""
        all_server = {}
        responce = requests.get(
            'https://core.aeza.net/api/services?offset=NaN&count=undefined&sort=',
            headers={
                'authorization': f'Bearer {self.key}'
            }
        )
        servers: dict = json.loads(responce.text)['data']['items']
        for i in servers:
            try:
                all_server[i['name']] = {'status': i['status'],
                                        'ip': i['ip'],
                                        'username': i['parameters']['username'],
                                        'password': i['secureParameters']['data']['password'],
                                        'type': i['product']['type'],
                                        'id': i['id']
                                        }
            except:
                ...
        return all_server

    def get_product(self) -> dict:
        """Получение списка продуктов."""
        product: dict = {}
        responce = requests.get(
            'https://core.aeza.net/api/services/products',
            headers={
                'Authorization': f'Bearer {self.key}'
            }
        )
        products = json.loads(responce.text)
        for i in products['data']['items']:
            product[i['name']] = [
                {'configuration': i['configuration']},
                {'price': i['rawPrices']}
            ]
        return product

    def get_total_product(self) -> int:
        """Получение количества продуктов."""
        responce = requests.get(
            'https://core.aeza.net/api/services/products',
            headers={
                'Authorization': f'Bearer {self.key}'})
        total = json.loads(responce.text)
        return total['data']['total']

    def ordering_service(self, count: int,
                         term: str,
                         name: str,
                         id: int,
                         parameters: int,
                         autoProlong: bool) -> bool:
        """Функция оформления сервера.

        Аргументы:
        count -- количество серверов (целое число)
        term -- срок аренды сервера (строка)
        name -- название сервера (строка)
        id -- идентификатор продукта (целое число)
        parameters -- параметры сервера (целое число)
        autoProlong -- автоматическое продление аренды (булево значение)

        Возвращает:
        Возвращает строку 'Сервер оформлен', если сервер успешно оформлен,
        или сообщение об ошибке в виде строки, если произошла ошибка.
        """
        data = {
            'count': count,
            'term': term,
            'name': name,
            'productId': id,
            'parameters': {
                'os': parameters
            },
            'autoProlong': autoProlong,
            'method': 'balance'
        }
        responce = requests.post(
            'https://core.aeza.net/api/services/orders',
            headers={
                'Authorization': f'Bearer {self.key}'},
            json=data
        )
        status = json.loads(responce.text)
        try:
            return status['error']['message']
        except:
            return 'Сервер оформлен'
