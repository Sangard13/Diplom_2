import requests
import random
import string
from config import Config


class ApiHelper:

    @staticmethod
    def generate_random_email():
        """Генерация случайного email"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        return f"{Config.TEST_EMAIL_PREFIX}{random_string}@test.com"

    @staticmethod
    def create_user(email=None, password=None, name=None):
        """Создание пользователя"""
        if email is None:
            email = ApiHelper.generate_random_email()
        if password is None:
            password = Config.TEST_PASSWORD
        if name is None:
            name = Config.TEST_NAME

        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        response = requests.post(Config.CREATE_USER_URL, json=payload)
        return response

    @staticmethod
    def login_user(email, password):
        """Авторизация пользователя"""
        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(Config.LOGIN_URL, json=payload)
        return response

    @staticmethod
    def delete_user(access_token):
        """Удаление пользователя (для очистки)"""
        headers = {"Authorization": access_token}
        response = requests.delete(Config.CREATE_USER_URL, headers=headers)
        return response

    @staticmethod
    def create_order(ingredients=None, access_token=None):
        """Создание заказа"""
        headers = {}
        if access_token:
            headers["Authorization"] = access_token

        payload = {}
        if ingredients is not None:
            payload["ingredients"] = ingredients

        response = requests.post(Config.CREATE_ORDER_URL, headers=headers, json=payload)
        return response