import allure
import pytest
from helpers.api_client import StellarBurgersAPI
from data.test_data import TestData


@allure.feature("Логин пользователя")
@allure.story("Эндпоинт: POST /api/auth/login")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_existing_user(self, registered_user):
        """Тест входа под существующим пользователем"""
        email = registered_user["email"]
        password = registered_user["password"]

        # Создаем нового клиента для теста входа
        new_client = StellarBurgersAPI()

        with allure.step("Отправка запроса на вход"):
            response = new_client.login_user(email, password)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert "refreshToken" in response_data, "В ответе должен быть refreshToken"
            assert response_data["user"]["email"] == email, "Email не совпадает"

    @allure.title("Вход с неверным email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_wrong_email(self, api_client):
        """Тест входа с неверным email"""
        with allure.step("Отправка запроса с неверным email"):
            response = api_client.login_user(
                TestData.WRONG_EMAIL,
                TestData.BASE_PASSWORD
            )

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert response_data["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_wrong_password(self, registered_user):
        """Тест входа с неверным паролем"""
        email = registered_user["email"]

        # Создаем нового клиента
        client = StellarBurgersAPI()

        with allure.step("Отправка запроса с неверным паролем"):
            response = client.login_user(email, TestData.WRONG_PASSWORD)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert response_data["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.title("Вход с пустыми данными")
    @allure.severity(allure.severity_level.NORMAL)
    def test_login_with_empty_data(self, api_client):
        """Тест входа с пустыми данными"""
        with allure.step("Отправка запроса с пустыми данными"):
            response = api_client.login_user("", "")

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"