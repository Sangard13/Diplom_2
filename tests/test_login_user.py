import pytest
from helpers.api_helper import ApiHelper
from config import Config


class TestLoginUser:

    def test_login_existing_user_success(self, api_helper, existing_user_data):
        """Вход под существующим пользователем"""
        # Выполнить вход с правильными учетными данными
        response = api_helper.login_user(
            email=existing_user_data['email'],
            password=existing_user_data['password']
        )

        print(f"\nТест: Вход существующего пользователя")
        print(f"Email: {existing_user_data['email']}")
        print(f"Статус код: {response.status_code}")
        print(f"Ответ: {response.text[:200]}...")

        # Проверить статус код
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}. Ответ: {response.text}"

        # Проверить тело ответа
        response_body = response.json()
        assert "success" in response_body, f"В ответе отсутствует поле success. Ответ: {response_body}"
        assert response_body["success"] is True, f"success должно быть True, получено {response_body['success']}"
        assert "user" in response_body, "В ответе отсутствует поле user"
        assert "email" in response_body["user"], "В ответе user отсутствует email"
        assert response_body["user"]["email"] == existing_user_data['email'], f"Email не совпадает"
        assert "name" in response_body["user"], "В ответе user отсутствует name"
        assert response_body["user"]["name"] == existing_user_data['name'], f"Name не совпадает"
        assert "accessToken" in response_body, "В ответе отсутствует accessToken"
        assert "refreshToken" in response_body, "В ответе отсутствует refreshToken"

        print(f"✅ Успешный вход пользователя {response_body['user']['name']}")

    @pytest.mark.parametrize("test_case", [
        ("wrong@email.com", "123456789", "неверным email"),
        ("qaerfsf13@hmaul.com", "WrongPassword!", "неверным паролем"),
        ("wrong@email.com", "WrongPassword!", "неверным email и паролем")
    ])
    def test_login_with_wrong_credentials_fail(self, api_helper, test_case):
        """Вход с неверным логином и паролем"""
        email, password, description = test_case

        print(f"\nТест: Вход с {description}")
        print(f"Email: {email}")
        print(f"Пароль: {password}")

        response = api_helper.login_user(email=email, password=password)

        print(f"Статус код: {response.status_code}")
        print(f"Ответ: {response.text}")

        # Проверить статус код
        assert response.status_code == 401, f"Ожидался код 401, получен {response.status_code}"

        # Проверить тело ответа
        response_body = response.json()
        assert "success" in response_body, "В ответе отсутствует поле success"
        assert response_body["success"] is False, f"success должно быть False, получено {response_body['success']}"
        assert "message" in response_body, "В ответе отсутствует поле message"

        print(f"✅ Корректная обработка неверных данных: {response_body['message']}")