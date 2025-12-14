import allure
import pytest


@allure.feature("Логин пользователя")
@allure.story("Эндпоинт: POST /api/auth/login")
class TestLoginUser:

    @allure.title("Вход под существующим пользователем")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_existing_user_success(self, registered_user):
        """Тест успешного входа под существующим пользователем"""
        client = registered_user["client"]
        email = registered_user["email"]
        password = registered_user["password"]

        client.token = None

        response = client.login_user(email, password)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True

    @allure.title("Вход с неверным логином и паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_wrong_credentials_fails(self, api_client):
        """Тест входа с неверным логином и паролем"""
        response = api_client.login_user("wrong@example.com", "WrongPassword123")

        assert response.status_code == 401
        response_data = response.json()
        assert response_data["success"] is False