# pointshub (Unofficial PointsHub API Client)

[🇷🇺 Русский](#русская-версия) | [🇺🇸 English](#english-version)

---

## English Version

Asynchronous Python client for [PointsHub API](https://api.buysteampoints.com/docs).  
❗ I do not collaborate and am not affiliated with [PointsHub](https://t.me/pointshub_bot). This client is written solely for convenience when working with the API.

### 📌 Quick Start

```python
import asyncio
from pointshub_api import PointsHubClient

async def main():
    async with PointsHubClient(api_key="your_api_key") as client:
        # Get current price
        price = await client.steam.get_price()
        print(price)

        # Buy Steam Points
        order = await client.steam.buy(puan=100, steam_link="https://steamcommunity.com/id/yourprofile")
        print(order)

        # Check balance
        balance = await client.steam.get_balance()
        print(balance)

asyncio.run(main())
```

### 📂 Main Features

#### 🎮 Steam Operations (`client.steam`)
- `get_price()` - Get current Steam Points price per point
- `buy(puan, steam_link)` - Buy Steam Points for a Steam account
- `get_balance()` - Get current account balance

### 📘 Usage Examples

#### Basic Usage
```python
import asyncio
from pointshub_api import PointsHubClient, APIError

async def main():
    try:
        async with PointsHubClient(api_key="your_api_key") as client:
            # Get price (no API key required)
            price = await client.steam.get_price()
            print(f"Current price: {price}")
            
            # Buy Steam Points
            order = await client.steam.buy(
                puan=100,
                steam_link="https://steamcommunity.com/id/yourprofile"
            )
            print(f"Order created: {order}")
            
            # Check balance
            balance = await client.steam.get_balance()
            print(f"Balance: {balance}")

    except APIError as e:
        print(f"API error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

asyncio.run(main())
```

#### Error Handling
```python
from pointshub_api import (
    PointsHubClient, 
    APIError, 
    APIAuthenticationError, 
    APIConnectionError,
    APITimeoutError,
    APIServerError,
    APIClientError
)

async def robust_example():
    try:
        async with PointsHubClient(api_key="your_api_key") as client:
            balance = await client.steam.get_balance()
            print(f"Balance: {balance}")
            
    except APIAuthenticationError:
        print("Authentication failed - check your API key")
    except APIConnectionError:
        print("Connection error - check internet")
    except APITimeoutError:
        print("Request timed out - try again")
    except APIServerError:
        print("Server error - PointsHub API is having issues")
    except APIClientError:
        print("Client error - check your request")
    except APIError as e:
        print(f"General API error: {e}")
```

### ⚠️ Disclaimer

- This is an **unofficial library**. This client is not an official PointsHub product.
- I **do not collaborate** with PointsHub and have no relation to their service or company.
- The author **is not responsible** for any problems, losses, or damages arising from the use of this library.
- The library may stop working at any time due to changes in the PointsHub API.
- This library is provided "AS IS", without any warranties, express or implied.
- Use at your own risk.

### 📜 License

[MIT](LICENSE)

---

## Русская версия

Асинхронный Python-клиент для [PointsHub API](https://api.buysteampoints.com/docs).  
❗ Я не сотрудничаю и никак не связан с [PointsHub](https://t.me/pointshub_bot). Этот клиент написан исключительно для удобства работы с API.

## 📌 Быстрый старт

```python
import asyncio
from pointshub_api import PointsHubClient

async def main():
    async with PointsHubClient(api_key="your_api_key") as client:
        # Получение текущей цены
        price = await client.steam.get_price()
        print(price)

        # Покупка Steam Points
        order = await client.steam.buy(puan=100, steam_link="https://steamcommunity.com/id/yourprofile")
        print(order)

        # Проверка баланса
        balance = await client.steam.get_balance()
        print(balance)

asyncio.run(main())
```

---

## 📂 Основные возможности

#### 🎮 Steam операции (`client.steam`)
- `get_price()` - Получение текущей цены за пункт Steam Points
- `buy(puan, steam_link)` - Покупка Steam Points для аккаунта Steam
- `get_balance()` - Получение текущего баланса аккаунта

---

## 📘 Примеры использования

### Основное использование
```python
import asyncio
from pointshub_api import PointsHubClient, APIError

async def main():
    try:
        async with PointsHubClient(api_key="your_api_key") as client:
            # Получение цены (API ключ не требуется)
            price = await client.steam.get_price()
            print(f"Текущая цена: {price}")
            
            # Покупка Steam Points
            order = await client.steam.buy(
                puan=100,
                steam_link="https://steamcommunity.com/id/yourprofile"
            )
            print(f"Заказ создан: {order}")
            
            # Проверка баланса
            balance = await client.steam.get_balance()
            print(f"Баланс: {balance}")

    except APIError as e:
        print(f"Ошибка API: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

asyncio.run(main())
```

### Обработка ошибок
```python
from pointshub_api import (
    PointsHubClient, 
    APIError, 
    APIAuthenticationError, 
    APIConnectionError,
    APITimeoutError,
    APIServerError,
    APIClientError
)

async def robust_example():
    try:
        async with PointsHubClient(api_key="your_api_key") as client:
            balance = await client.steam.get_balance()
            print(f"Баланс: {balance}")
            
    except APIAuthenticationError:
        print("Ошибка авторизации - проверьте ваш API ключ")
    except APIConnectionError:
        print("Ошибка соединения - проверьте интернет")
    except APITimeoutError:
        print("Время ожидания истекло - попробуйте еще раз")
    except APIServerError:
        print("Ошибка сервера - проблемы с PointsHub API")
    except APIClientError:
        print("Ошибка клиента - проверьте ваш запрос")
    except APIError as e:
        print(f"Общая ошибка API: {e}")
```

---

## ⚠️ Отказ от ответственности (Disclaimer)

- Это **неофициальная библиотека**. Данный клиент не является официальным продуктом PointsHub.
- Я **не сотрудничаю** с PointsHub и не имею отношения к их сервису или компании.
- Автор **не несет ответственности** за любые проблемы, убытки или ущерб, возникшие в результате использования данной библиотеки.
- Библиотека может перестать работать в любой момент из-за изменений в API PointsHub.
- Данная библиотека предоставляется "КАК ЕСТЬ", без каких-либо гарантий, явных или подразумеваемых.
- Используйте на свой страх и риск.

---

## 📜 Лицензия

[MIT](LICENSE)
