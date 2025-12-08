import allure
import pytest
from data.test_data import TestData


@allure.feature("Создание пользователя")
@allure.story("Эндпоинт: POST /api/auth/register")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_unique_user(self, api_client):
        """Тест создания уникального пользователя"""
        user_data = TestData.get_valid_user_data()

        with allure.step("Отправка запроса на создание пользователя"):
            response = api_client.register_user(**user_data)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is True, "Поле success должно быть True"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert "refreshToken" in response_data, "В ответе должен быть refreshToken"
            assert response_data["user"]["email"] == user_data["email"], "Email не совпадает"
            assert response_data["user"]["name"] == user_data["name"], "Name не совпадает"

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user(self, registered_user):
        """Тест создания уже существующего пользователя"""
        client = registered_user["client"]
        email = registered_user["email"]
        password = registered_user["password"]
        name = registered_user["name"]

        with allure.step("Повторная регистрация того же пользователя"):
            response = client.register_user(email, password, name)

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

        with allure.step("Проверка тела ответа"):
            response_data = response.json()
            assert response_data["success"] is False, "Поле success должно быть False"
            assert response_data["message"] == "User already exists", "Неверное сообщение об ошибке"

    @allure.title("Создание пользователя без email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_without_email(self, api_client):
        """Тест создания пользователя без обязательного поля email"""
        user_data = {
            "password": "Password123",
            "name": "Test User"
        }

        with allure.step("Отправка запроса без email"):
            response = api_client.session.post(
                f"{api_client.BASE_URL}/auth/register",
                json=user_data,
                headers=api_client._get_headers()
            )

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

    @allure.title("Создание пользователя без пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_without_password(self, api_client):
        """Тест создания пользователя без обязательного поля password"""
        user_data = {
            "email": TestData.get_valid_user_data()["email"],
            "name": "Test User"
        }

        with allure.step("Отправка запроса без пароля"):
            response = api_client.session.post(
                f"{api_client.BASE_URL}/auth/register",
                json=user_data,
                headers=api_client._get_headers()
            )

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"

    @allure.title("Создание пользователя без имени")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_without_name(self, api_client):
        """Тест создания пользователя без обязательного поля name"""
        user_data = {
            "email": TestData.get_valid_user_data()["email"],
            "password": "Password123"
        }

        with allure.step("Отправка запроса без имени"):
            response = api_client.session.post(
                f"{api_client.BASE_URL}/auth/register",
                json=user_data,
                headers=api_client._get_headers()
            )

        with allure.step("Проверка статус-кода ответа"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"