from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersTest(TestCase):
    fixtures = ["users.json"]

    def test_home(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_fixtures(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, "rrr")
    
    def test_bad_login(self):
        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': 'rrrh', 'password':'1234'})
        self.assertContains(response, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')

    def test_good_login(self):
        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': 'rrr', 'password':'1234'})
        self.assertContains(response, 'Вы залогинены')

    
    def test_users_list(self):
        response = self.client.get(reverse("users_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("users", response.context)
        users = response.context["users"]

        self.assertTrue(len(users) == 3)

    def test_user_create(self):
        create_url = reverse("users_create")
        list_url = reverse("users_list")
        response = self.client.post(create_url, follow=True, data={"first_name": "Bobik", "last_name": 'S', 'username': 'bob-S', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'Пользователь успешно зарегистрирован')
        response = self.client.get(list_url)
        self.assertContains(response, "Bobik")
        users = response.context["users"]
        self.assertTrue(len(users) == 4)
        
    
    def test_bad_permission_middleware(self):
        user = User.objects.filter(first_name="Егор")
        update_url = reverse("users_update", kwargs={'pk': user[0].id})
        response = self.client.post(update_url, follow=True, data={"first_name": "Bobik", "last_name": 'Sokkkkk', 'username': 'bob-S', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': 'rrr', 'password':'1234'})
        self.assertContains(response, 'Вы залогинены')

        user = User.objects.filter(first_name="пупсик")
        update_url = reverse("users_update", kwargs={'pk': user[0].id})
        response = self.client.post(update_url, follow=True, data={"first_name": "Bobik", "last_name": 'Sokkkkk', 'username': 'bob-S', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя.')




