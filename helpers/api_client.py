import requests
from .constants import URLs


class StellarBurgersAPI:
    def __init__(self):
        self.token = None

    def _get_headers(self):
        """Получение заголовков для запросов"""
        headers = {
            "Content-Type": "application/json"
        }
        if self.token:
            headers["Authorization"] = self.token
        return headers

    def register_user(self, email=None, password=None, name=None):
        """Регистрация пользователя - принимает optional параметры"""
        payload = {}
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        if name is not None:
            payload["name"] = name

        return requests.post(URLs.REGISTER, json=payload)

    def login_user(self, email, password):
        """Авторизация пользователя"""
        payload = {
            "email": email,
            "password": password
        }
        response = requests.post(URLs.LOGIN, json=payload)
        if response.status_code == 200:
            self.token = response.json().get("accessToken")
        return response

    def get_user_info(self):
        """Получение информации о пользователе"""
        return requests.get(URLs.USER, headers=self._get_headers())

    def update_user_info(self, email=None, password=None, name=None):
        """Обновление информации о пользователе"""
        payload = {}
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        if name:
            payload["name"] = name

        return requests.patch(URLs.USER, json=payload, headers=self._get_headers())

    def delete_user(self):
        """Удаление пользователя"""
        return requests.delete(URLs.USER, headers=self._get_headers())

    def get_ingredients(self):
        """Получение списка ингредиентов"""
        return requests.get(URLs.INGREDIENTS)

    def create_order(self, ingredients):
        """Создание заказа"""
        payload = {
            "ingredients": ingredients
        }
        return requests.post(URLs.ORDERS, json=payload, headers=self._get_headers())

    def get_user_orders(self):
        """Получение заказов пользователя"""
        return requests.get(URLs.ORDERS, headers=self._get_headers())

    def logout_user(self):
        """Выход из системы"""
        payload = {
            "token": self.token.replace("Bearer ", "") if self.token and "Bearer " in self.token else self.token
        }
        return requests.post(URLs.LOGOUT, json=payload)
