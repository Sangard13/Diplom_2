import requests


class StellarBurgersAPI:
    def __init__(self, base_url="https://stellarburgers.education-services.ru"):
        self.base_url = base_url
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
        url = f"{self.base_url}/api/auth/register"

        payload = {}
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        if name is not None:
            payload["name"] = name

        return requests.post(url, json=payload)

    def login_user(self, email, password):
        """Авторизация пользователя"""
        url = f"{self.base_url}/api/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        return requests.post(url, json=payload)

    def get_user_info(self):
        """Получение информации о пользователе"""
        url = f"{self.base_url}/api/auth/user"
        return requests.get(url, headers=self._get_headers())

    def update_user_info(self, email=None, password=None, name=None):
        """Обновление информации о пользователе"""
        url = f"{self.base_url}/api/auth/user"
        payload = {}
        if email:
            payload["email"] = email
        if password:
            payload["password"] = password
        if name:
            payload["name"] = name

        return requests.patch(url, json=payload, headers=self._get_headers())

    def delete_user(self):
        """Удаление пользователя"""
        url = f"{self.base_url}/api/auth/user"
        return requests.delete(url, headers=self._get_headers())

    def get_ingredients(self):
        """Получение списка ингредиентов"""
        url = f"{self.base_url}/api/ingredients"
        return requests.get(url)

    def create_order(self, ingredients):
        """Создание заказа"""
        url = f"{self.base_url}/api/orders"
        payload = {
            "ingredients": ingredients
        }
        return requests.post(url, json=payload, headers=self._get_headers())

    def get_user_orders(self):
        """Получение заказов пользователя"""
        url = f"{self.base_url}/api/orders"
        return requests.get(url, headers=self._get_headers())

    def logout_user(self):
        """Выход из системы"""
        url = f"{self.base_url}/api/auth/logout"
        payload = {
            "token": self.token.replace("Bearer ", "") if self.token and "Bearer " in self.token else self.token
        }
        return requests.post(url, json=payload)
