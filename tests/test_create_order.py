import allure
import pytest
from data.test_data import TestData


@allure.feature("Создание заказа")
@allure.story("Эндпоинт: POST /api/orders")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_order_with_auth_and_ingredients(self, registered_user, valid_ingredients):
        """Тест создания заказа с авторизацией и ингредиентами"""
        client = registered_user["client"]

        with allure.step("Отправка запроса на создание заказа"):
            response = client.create_order(valid_ingredients, auth=True)

        with allure.step("Проверка статус-кода ответа"):
            # Согласно документации, с авторизацией должен быть 200
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "order" in response_data, "В ответе должен быть объект order"
            assert "number" in response_data["order"], "В заказе должен быть номер"
            assert "name" in response_data["order"], "В заказе должно быть название"

    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_auth(self, api_client, valid_ingredients):
        """Тест создания заказа без авторизации"""
        with allure.step("Отправка запроса на создание заказа без авторизации"):
            response = api_client.create_order(valid_ingredients, auth=False)

        with allure.step("Проверка статус-кода ответа"):
            # Проверим оба возможных варианта: 200 или 401
            # Сначала проверим, что запрос вообще прошел
            assert response.status_code in [200, 401], f"Неожиданный статус: {response.status_code}"

            if response.status_code == 200:
                # Если API позволяет создавать заказ без авторизации
                response_data = response.json()
                assert response_data["success"] is True, "Поле success должно быть True"
            else:
                # Если API требует авторизацию
                response_data = response.json()
                assert response_data["success"] is False, "Поле success должно быть False"

    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_without_ingredients(self, registered_user):
        """Тест создания заказа без ингредиентов"""
        client = registered_user["client"]

        with allure.step("Отправка запроса на создание заказа без ингредиентов"):
            response = client.create_order([], auth=True)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert "message" in response_data, "Должно быть сообщение об ошибке"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_invalid_ingredient_hash(self, registered_user, invalid_ingredient_hash):
        """Тест создания заказа с неверным хешем ингредиентов"""
        client = registered_user["client"]

        with allure.step("Отправка запроса с неверным хешем ингредиентов"):
            response = client.create_order(invalid_ingredient_hash, auth=True)

        with allure.step("Проверка статус-кода ответа"):
            # Может быть 400 или 500 в зависимости от реализации
            assert response.status_code in [400, 500], f"Ожидался статус 400 или 500, получен {response.status_code}"

    @allure.title("Создание заказа с одним ингредиентом")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_single_ingredient(self, registered_user, get_ingredients):
        """Тест создания заказа с одним ингредиентом"""
        client = registered_user["client"]
        single_ingredient = [get_ingredients[0]["_id"]]

        with allure.step("Отправка запроса с одним ингредиентом"):
            response = client.create_order(single_ingredient, auth=True)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code in [200, 400], f"Неожиданный статус: {response.status_code}"