import random
import string


def generate_random_email() -> str:
    """Генерация случайного email"""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    return f"test_{random_string}@example.com"


def generate_random_name() -> str:
    """Генерация случайного имени"""
    random_string = ''.join(random.choices(string.ascii_letters, k=8))
    return f"Test User {random_string}"


class TestData:
    # Тестовые пользователи
    BASE_PASSWORD = "Password123"
    BASE_NAME = "Test User"

    # Невалидные данные
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

    @staticmethod
    def get_invalid_user_data_missing_email():
        """Данные пользователя без email"""
        return {
            "password": "Password123",
            "name": generate_random_name()
        }

    @staticmethod
    def get_invalid_user_data_missing_password():
        """Данные пользователя без пароля"""
        return {
            "email": generate_random_email(),
            "name": generate_random_name()
        }

    @staticmethod
    def get_invalid_user_data_missing_name():
        """Данные пользователя без имени"""
        return {
            "email": generate_random_email(),
            "password": "Password123"
        }