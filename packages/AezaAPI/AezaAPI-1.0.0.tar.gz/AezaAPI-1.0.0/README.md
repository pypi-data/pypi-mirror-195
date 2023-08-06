# AezaAPI

### Описание
Библиотека для использования API сервиса Aeza

### Методы

- <b>get_balance</b> - Узнать баланс
- <b>invoice_card</b> - Пополнить баланс картой
- <b>invoice_qiwi</b> - Пополнить баланс через Qiwi
- <b>status_server</b> - Статус серверов
- <b>add_api_key</b> - Создание API-ключа
- <b>get_api_key</b> - Получение списка API-ключей
- <b>add_ssh_key</b> - Добавление SSH-ключа
- <b>get_ssh_key</b> - Получение списка SSH-ключей
- <b>get_my_server</b> - Получение информации приобретённых серверов
- <b>get_product</b> - Получение списка продуктов
- <b>get_total_product</b> - Количество продуктов
- <b>ordering_service</b> - Покупка сервера

### Примеры

```python
from ApiAeza import aeza

TOKEN = aeza.AuthAeza('API-KEY')


def test() -> str:
    """Функция проверит баланс,
       если он меньше 50 рублей,
       то создаcт счёт на сумму 500 рублей
       при этом метод сразу возвращает ссылку для оплаты."""
    if TOKEN.get_balance() < 50:
        return TOKEN.invoice_card(500)
    return 'Всё хорошо'
```

<b>Покупка сервера</b>

```python
from ApiAeza import aeza

TOKEN = aeza.AuthAeza('API-KEY')


def test() -> str:
    """Покупка сервера."""
    return TOKEN.ordering_service(1, # Количество
                                  'mount', # Срок (hour, mount, quarter_year, year, half_year)
                                  'NameServer', # Имя сервера
                                  3, # ID сервера (Можно узнать методом get_product)
                                  25, # os
                                  True) # Автопродление
```

###Начало работы

Для начала работы импортируйте библиотеку, предварительно установив её
```
pip install ApiAeza
```
```python
from ApiAeza import aeza
```
Далее инициализируйте API-ключ
```python
TOKEN = aeza.AuthAeza('API-KEY')
```
Все методы делаются через переменную в которой вы инициализировали токен
```python
TOKEN.get_my_server()
```