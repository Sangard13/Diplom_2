import allure
import pytest


@allure.feature("Создание пользователя")
@allure.story("Эндпоинт: POST /api/auth/register")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_unique_user_success(self, api_client, new_user_data):
        """Тест успешного создания уникального пользователя"""
        response = api_client.register_user(**new_user_data)

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["success"] is True

        # Очистка - удаление созданного пользователя
        api_client.token = response_data["accessToken"]
        api_client.delete_user()
        api_client.token = None

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user_fails(self, registered_user):
        """Тест неудачной попытки создания уже существующего пользователя"""
        client = registered_user["client"]
        user_data = registered_user["user_data"]

        response = client.register_user(**user_data)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] is False

    @pytest.mark.parametrize("missing_field", [
        "email",
        "password",
        "name",
    ])
    @allure.title("Создание пользователя без обязательного поля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_without_required_field_fails(self, api_client, new_user_data, missing_field):
        """Тест создания пользователя без обязательных полей"""
        allure.dynamic.title(f"Создание пользователя без поля {missing_field}")

        invalid_user_data = new_user_data.copy()
        invalid_user_data.pop(missing_field)

        response = api_client.register_user(**invalid_user_data)

        assert response.status_code == 403
        response_data = response.json()
        assert response_data["success"] is False