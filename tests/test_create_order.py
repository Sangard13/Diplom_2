import allure
import pytest
from config import Config
from helpers.api_helper import ApiHelper


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией")
    @allure.description("Тест на успешное создание заказа авторизованным пользователем")
    def test_create_order_with_auth_success(self, api_helper, create_and_delete_user):
        with allure.step("Создать пользователя и получить токен"):
            email = api_helper.generate_random_email()
            create_response = create_and_delete_user(email=email)
            assert create_response.status_code == 200, "Пользователь должен быть создан успешно"
            access_token = create_response.json().get('accessToken')

        with allure.step("Создать заказ с ингредиентами"):
            ingredients = [Config.BUN_INGREDIENT, Config.MAIN_INGREDIENT, Config.SAUCE_INGREDIENT]
            response = api_helper.create_order(ingredients=ingredients, access_token=access_token)

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверить тело ответа"):
            response_body = response.json()
            assert "success" in response_body, "В ответе отсутствует поле success"
            assert response_body["success"] is True, f"success должно быть True, получено {response_body['success']}"
            assert "order" in response_body, "В ответе отсутствует поле order"
            assert "number" in response_body["order"], "В ответе order отсутствует number"

    @allure.title("Создание заказа без авторизации")
    @allure.description("Тест на создание заказа без токена авторизации")
    def test_create_order_without_auth_fail(self, api_helper):
        with allure.step("Создать заказ без токена авторизации"):
            ingredients = [Config.BUN_INGREDIENT, Config.MAIN_INGREDIENT]
            response = api_helper.create_order(ingredients=ingredients)

        with allure.step("Проверить статус код"):
            assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"

        with allure.step("Проверить тело ответа"):
            response_body = response.json()
            assert "success" in response_body, "В ответе отсутствует поле success"
            assert response_body["success"] is False, f"success должно быть False, получено {response_body['success']}"
            assert "message" in response_body, "В ответе отсутствует поле message"

    @allure.title("Создание заказа с ингредиентами")
    @allure.description("Тест на создание заказа с корректными ингредиентами")
    def test_create_order_with_ingredients_success(self, api_helper, create_and_delete_user):
        with allure.step("Создать пользователя и получить токен"):
            email = api_helper.generate_random_email()
            create_response = create_and_delete_user(email=email)
            access_token = create_response.json().get('accessToken')

        with allure.step("Создать заказ с несколькими ингредиентами"):
            ingredients = [
                Config.BUN_INGREDIENT,
                Config.MAIN_INGREDIENT,
                Config.SAUCE_INGREDIENT,
                Config.BUN_INGREDIENT  # Вторая булка
            ]
            response = api_helper.create_order(ingredients=ingredients, access_token=access_token)

        with allure.step("Проверить успешное создание"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
            assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    @allure.description("Тест на создание заказа без указания ингредиентов")
    def test_create_order_without_ingredients_fail(self, api_helper, create_and_delete_user):
        with allure.step("Создать пользователя и получить токен"):
            email = api_helper.generate_random_email()
            create_response = create_and_delete_user(email=email)
            access_token = create_response.json().get('accessToken')

        with allure.step("Создать заказ без ингредиентов"):
            response = api_helper.create_order(ingredients=None, access_token=access_token)

        with allure.step("Проверить статус код"):
            assert response.status_code == 400, f"Ожидался код 400, получен {response.status_code}"

        with allure.step("Проверить тело ответа"):
            response_body = response.json()
            assert "success" in response_body, "В ответе отсутствует поле success"
            assert response_body["success"] is False, f"success должно быть False, получено {response_body['success']}"
            assert "message" in response_body, "В ответе отсутствует поле message"

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.description("Тест на создание заказа с некорректными ID ингредиентов")
    def test_create_order_with_invalid_ingredient_hash_fail(self, api_helper, create_and_delete_user):
        with allure.step("Создать пользователя и получить токен"):
            email = api_helper.generate_random_email()
            create_response = create_and_delete_user(email=email)
            access_token = create_response.json().get('accessToken')

        with allure.step("Создать заказ с неверным хешем ингредиентов"):
            invalid_ingredients = ["invalid_hash_1", "invalid_hash_2"]
            response = api_helper.create_order(ingredients=invalid_ingredients, access_token=access_token)

        with allure.step("Проверить статус код"):
            # API может вернуть 400 или 500 в зависимости от реализации
            assert response.status_code in [400, 500, 404], \
                f"Ожидался код 400, 404 или 500, получен {response.status_code}"