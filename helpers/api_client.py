import requests
from typing import Dict, List


class StellarBurgersAPI:
    BASE_URL = "https://stellarburgers.education-services.ru/api"

    def __init__(self):
        self.session = requests.Session()
        self.token = None

    def set_token(self, token: str):
        """Установка токена авторизации"""
        self.token = token

    def _get_headers(self, auth: bool = False) -> Dict:
        """Получение заголовков для запроса"""
        headers = {
            'Content-Type': 'application/json'
        }
        if auth and self.token:
            # В документации указано, что токен передается без префикса Bearer
            headers['Authorization'] = self.token
        return headers

    def register_user(self, email: str, password: str, name: str) -> requests.Response:
        """Регистрация пользователя"""
        url = f"{self.BASE_URL}/auth/register"
        payload = {
            "email": email,
            "password": password,
            "name": name
        }
        response = self.session.post(url, json=payload, headers=self._get_headers())

        # Сохраняем токен, если регистрация успешна
        if response.status_code == 200:
            data = response.json()
            if 'accessToken' in data:
                self.token = data['accessToken']

        return response

    def login_user(self, email: str, password: str) -> requests.Response:
        """Авторизация пользователя"""
        url = f"{self.BASE_URL}/auth/login"
        payload = {
            "email": email,
            "password": password
        }
        response = self.session.post(url, json=payload, headers=self._get_headers())

        # Сохраняем токен, если авторизация успешна
        if response.status_code == 200:
            data = response.json()
            if 'accessToken' in data:
                self.token = data['accessToken']

        return response

    def delete_user(self) -> requests.Response:
        """Удаление пользователя (требуется авторизация)"""
        if not self.token:
            raise ValueError("Требуется авторизация для удаления пользователя")

        url = f"{self.BASE_URL}/auth/user"
        response = self.session.delete(url, headers=self._get_headers(auth=True))
        return response

    def create_order(self, ingredients: List[str], auth: bool = True) -> requests.Response:
        """Создание заказа"""
        url = f"{self.BASE_URL}/orders"
        payload = {
            "ingredients": ingredients
        }

        if auth:
            response = self.session.post(url, json=payload, headers=self._get_headers(auth=True))
        else:
            response = self.session.post(url, json=payload, headers=self._get_headers())

        return response

    def get_ingredients(self) -> requests.Response:
        """Получение списка ингредиентов"""
        url = f"{self.BASE_URL}/ingredients"
        response = self.session.get(url, headers=self._get_headers())
        return response

    def get_user_info(self) -> requests.Response:
        """Получение информации о пользователе"""
        url = f"{self.BASE_URL}/auth/user"
        response = self.session.get(url, headers=self._get_headers(auth=True))
        return response