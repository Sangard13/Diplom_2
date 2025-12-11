import random
import string


class UserDataGenerator:

    @staticmethod
    def generate_random_string(length=10, chars=None):
        """Генерация случайной строки"""
        if chars is None:
            chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=length))

    @staticmethod
    def generate_random_email():
        """Генерация случайного email"""
        random_string = UserDataGenerator.generate_random_string(10)
        return f"test_{random_string}@example.com"

    @staticmethod
    def generate_random_name():
        """Генерация случайного имени"""
        random_string = UserDataGenerator.generate_random_string(
            8, string.ascii_letters
        )
        return f"Test User {random_string}"

    @staticmethod
    def generate_valid_user_data():
        """Получение валидных данных пользователя"""
        return {
            "email": UserDataGenerator.generate_random_email(),
            "password": "Password123",
            "name": UserDataGenerator.generate_random_name()
        }

    @staticmethod
    def generate_invalid_email():
        """Генерация невалидного email"""
        return "invalid_email_format"

    @staticmethod
    def generate_short_password():
        """Генерация короткого пароля"""
        return "short"