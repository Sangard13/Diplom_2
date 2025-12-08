import allure
import pytest
from helpers.api_helper import ApiHelper


@allure.feature("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    @allure.description("Тест на успешное создание нового пользователя")
    def test_create_unique_user_success(self, api_helper):
        with allure.step("Создать уникального пользователя"):
            email = api_helper.generate_random_email()
            response = api_helper.create_user(email=email)

        with allure.step("Проверить статус код"):
            assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"

        with allure.step("Проверить тело ответа"):
            response_body = response.json()
            assert "success" in response_body, "В ответе отсутствует поле success"
            assert response_body["success"] is True, f"success должно быть True, получено {response_body['success']}"
            assert "user" in response_body, "В ответе отсутствует поле user"
            assert "email" in response_body["user"], "В ответе user отсутствует email"
            assert response_body["user"]["email"] == email, f"Email не совпадает"
            assert "name" in response_body["user"], "В ответе user отсутствует name"
            assert "accessToken" in response_body, "В ответе отсутствует accessToken"
            assert "refreshToken" in response_body, "В ответе отсутствует refreshToken"

    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.description("Тест на попытку создания уже существующего пользователя")
    def test_create_existing_user_fail(self, api_helper, create_and_delete_user):
        with allure.step("Создать первого пользователя"):
            email = api_helper.generate_random_email()
            create_response = create_and_delete_user(email=email)
            assert create_response.status_code == 200, "Первый пользователь должен быть создан успешно"

        with allure.step("Попытаться создать пользователя с тем же email"):
            response = api_helper.create_user(email=email)

        with allure.step("Проверить статус код"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"

        with allure.step("Проверить тело ответа"):
            response_body = response.json()
            assert "success" in response_body, "В ответе отсутствует поле success"
            assert response_body["success"] is False, f"success должно быть False, получено {response_body['success']}"
            assert "message" in response_body, "В ответе отсутствует поле message"

    @allure.title("Создание пользователя без обязательного поля")
    @allure.description("Тест на создание пользователя без заполнения одного из обязательных полей")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_fail(self, api_helper, missing_field):
        with allure.step(f"Создать пользователя без поля {missing_field}"):
            email = api_helper.generate_random_email() if missing_field != "email" else None
            password = "Password123!" if missing_field != "password" else None
            name = "Test User" if missing_field != "name" else None

            response = api_helper.create_user(email=email, password=password, name=name)

        with allure.step("Проверить статус код"):
            assert response.status_code == 403, f"Ожидался код 403, получен {response.status_code}"

        with allure.step("Проверить тело ответа"):
            response_body = response.json()
            assert "success" in response_body, "В ответе отсутствует поле success"
            assert response_body["success"] is False, f"success должно быть False, получено {response_body['success']}"
            assert "message" in response_body, "В ответе отсутствует поле message"