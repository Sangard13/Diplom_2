import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers.api_client import StellarBurgersAPI
from helpers.data_generator import UserDataGenerator


# Фикстуры для тестов создания пользователя и логина
@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return StellarBurgersAPI()


@pytest.fixture
def new_user_data():
    """Фикстура генерирует данные нового пользователя"""
    return UserDataGenerator.generate_valid_user_data()


@pytest.fixture
def registered_user(api_client, new_user_data):
    """
    Фикстура создает зарегистрированного пользователя для тестов.
    Автоматически удаляет пользователя после теста.
    """
    response = api_client.register_user(**new_user_data)

    if response.status_code != 200:
        pytest.skip("Не удалось зарегистрировать пользователя для теста")

    response_data = response.json()
    token = response_data.get("accessToken")
    api_client.token = token

    # Данные пользователя
    user_info = {
        "client": api_client,
        "email": new_user_data["email"],
        "password": new_user_data["password"],
        "name": new_user_data["name"],
        "user_data": new_user_data,
        "token": token,
        "response": response
    }

    yield user_info

    # Удаление пользователя после теста
    if token:
        api_client.token = token
        api_client.delete_user()
    api_client.token = None


# Фикстуры для тестов создания заказа
@pytest.fixture
def get_ingredients(api_client):
    """Фикстура для получения списка ингредиентов"""
    response = api_client.get_ingredients()

    if response.status_code != 200:
        pytest.skip("Не удалось получить список ингредиентов")

    data = response.json()
    if not data.get("success", False):
        pytest.skip("API вернуло неуспешный ответ для ингредиентов")

    return data.get("data", [])


@pytest.fixture
def valid_ingredients(get_ingredients):
    """Фикстура для получения валидных ингредиентов для заказа"""
    if not get_ingredients:
        pytest.skip("Нет доступных ингредиентов")

    ingredients = []

    # Ингредиенты разных типов для теста заказа
    buns = [ing for ing in get_ingredients if ing.get("type") == "bun"]
    sauces = [ing for ing in get_ingredients if ing.get("type") == "sauce"]
    mains = [ing for ing in get_ingredients if ing.get("type") == "main"]

    # Добавляем по одному ингредиенту каждого типа
    if buns:
        ingredients.append(buns[0].get("_id"))
    if sauces:
        ingredients.append(sauces[0].get("_id"))
    if mains:
        ingredients.append(mains[0].get("_id"))

    return ingredients


@pytest.fixture
def invalid_ingredient_hash():
    """Фикстура для неверного хеша ингредиента"""
    return ["invalid_hash_12345"]


@pytest.fixture
def empty_ingredients():
    """Фикстура возвращает пустой список ингредиентов"""
    return []