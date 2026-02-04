from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class UsersTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.home_url = reverse("home")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")

    def test_home(self):
        #гравная страница
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вани')
    
    def test_bad_login(self):
        #неправильный логин
        response = self.client.post(self.login_url, follow=True, data={'username': 'rrrh', 'password':'1234'})
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')

    def test_good_login(self):
        #отображение страницы входа
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Вход')

        #post запрос на вход с правильным логином
        response = self.client.post(self.login_url, follow=True, data={'username': 'rrr', 'password':'1234'})
        self.assertContains(response, 'Вы залогинены')
    
    def test_logout(self):
        #post запрос на выход
        response = self.client.post(self.logout_url, follow=True)
        self.assertContains(response, 'Вы разлогинены')