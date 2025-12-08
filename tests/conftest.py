import pytest
import allure
import random
import string
from helpers.api_client import StellarBurgersAPI


def generate_random_email():
    """Генерация случайного email"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_string}@example.com"


def generate_random_name():
    """Генерация случайного имени"""
    random_string = ''.join(random.choices(string.ascii_letters, k=8))
    return f"Test User {random_string}"


class TestData:
    BASE_PASSWORD = "Password123"
    WRONG_EMAIL = "wrong@example.com"
    WRONG_PASSWORD = "WrongPassword"

    @staticmethod
    def get_valid_user_data():
        """Получение валидных данных пользователя"""
        return {
            "email": generate_random_email(),
            "password": "Password123",
            "name": generate_random_name()
        }


@pytest.fixture
def api_client():
    """Фикстура для создания API клиента"""
    return StellarBurgersAPI()


@pytest.fixture
def registered_user(api_client):
    """Фикстура для создания зарегистрированного пользователя"""
    user_data = TestData.get_valid_user_data()
    response = api_client.register_user(**user_data)
    assert response.status_code == 200, f"Не удалось зарегистрировать пользователя: {response.text}"

    yield {
        "client": api_client,
        "email": user_data["email"],
        "password": user_data["password"],
        "name": user_data["name"],
        "response": response
    }

    # Удаление пользователя после теста
    try:
        if api_client.token:
            delete_response = api_client.delete_user()
            print(f"Пользователь удален: {delete_response.status_code}")
    except Exception as e:
        print(f"Ошибка при удалении пользователя: {e}")


@pytest.fixture
def get_ingredients(api_client):
    """Фикстура для получения списка ингредиентов"""
    response = api_client.get_ingredients()
    assert response.status_code == 200, "Не удалось получить список ингредиентов"
    data = response.json()
    return data["data"]


@pytest.fixture
def valid_ingredients(get_ingredients):
    """Фикстура для получения валидных ингредиентов"""
    ingredients = []

    # Берем первые 3 ингредиента разных типов
    buns = []
    sauces = []
    mains = []

    for ingredient in get_ingredients:
        if ingredient["type"] == "bun":
            buns.append(ingredient["_id"])
        elif ingredient["type"] == "sauce":
            sauces.append(ingredient["_id"])
        elif ingredient["type"] == "main":
            mains.append(ingredient["_id"])

    # Добавляем по одному из каждой категории, если есть
    if buns:
        ingredients.append(buns[0])
    if sauces:
        ingredients.append(sauces[0])
    if mains:
        ingredients.append(mains[0])

    return ingredients


@pytest.fixture
def invalid_ingredient_hash():
    """Фикстура для невалидного хеша ингредиента"""
    return ["invalid_hash_12345"]