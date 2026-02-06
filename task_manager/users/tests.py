from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class UsersTest(TestCase):
    fixtures = ["users.json"]

    def setUp(self):
        self.list_url = reverse("users_list")
        self.create_url = reverse("users_create")
        self.login_url = reverse("login")
        self.user1 = User.objects.get(username="rrr")
        self.user2 = User.objects.get(pk="2")
        self.user3 = User.objects.get(first_name="пупсик")
        self.update_url1 = reverse("users_update", kwargs={'pk': self.user1.id})
        self.update_url2 = reverse("users_update", kwargs={'pk': self.user2.id})

    def test_fixtures(self):
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, "rrr")

    
    def test_users_list(self):
        #отображение списка пользователей
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Пользователи')

        #по общему количеству
        self.assertIn("users", response.context)
        users = response.context["users"]
        self.assertTrue(len(users) == 3)
    
    def test_user_bad_create(self):
        response = self.client.post(self.create_url, data={"first_name": "Bobik", "last_name": 'S', 'username': 'bob-S', 'password1':'123', 'password2':'1234'})
        self.assertContains(response, 'Введенные пароли не совпадают.')

    def test_user_good_create(self):
        #отображение страницы регистрации
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Регистрация')

        #успешная регистрация
        response = self.client.post(self.create_url, follow=True, data={"first_name": "Bobik", "last_name": 'S', 'username': 'bob-S', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'Пользователь успешно зарегистрирован')

        #проверка в списке пользователей
        response = self.client.get(self.list_url)
        self.assertContains(response, "Bobik")

        #по общему количеству
        users = response.context["users"]
        self.assertTrue(len(users) == 4)
    
    def make_login(self, user):
        #логин под пользователем №1 (пароли у всех одинаковые)
        response = self.client.post(self.login_url, follow=True, data={'username': user.username, 'password':'1234'})
        self.assertContains(response, 'Вы залогинены')
    
    def test_bad_permission_middleware(self):
        #отправка запроса на изменение пользователя, не будучи залогиненым
        response = self.client.post(self.update_url1, follow=True, data={"first_name": "Bobik", "last_name": 'Sokkkkk', 'username': 'bob-S', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #логин под пользователем №1
        self.make_login(self.user1)

        #попытка изменить пользователя №3
        delete_url = reverse("users_delete", kwargs={'pk': self.user3.id})
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя.')
    
    def test_user_bad_update(self):
        #логин под пользователем №2
        self.make_login(self.user2)

        #обновление с плохим паролем
        response = self.client.post(self.update_url2, follow=True, data={"first_name": self.user2.first_name, "last_name": self.user2.last_name, 'username': 'egoska', 'password1':'12', 'password2':'12'})
        self.assertContains(response, 'Введённый пароль слишком короткий. Он должен состоять из как минимум 3 символа.')
    

    def test_user_update(self):
        #логин под пользователем №2
        self.make_login(self.user2)

        #отображение страницы формы
        response = self.client.get(self.update_url2)
        self.assertEqual(response.status_code, 200)

        #запрос post на обновление
        response = self.client.post(self.update_url2, follow=True, data={"first_name": self.user2.first_name, "last_name": self.user2.last_name, 'username': 'egoska', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'Пользователь успешно изменен')
        self.assertContains(response, 'egoska')
    



    def test_user_good_delete(self):
    
        self.make_login(self.user2)

        delete_url = reverse("users_delete", kwargs={'pk': self.user2.id})

        #отображение страницы удаления
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        #post запрос на удаление
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, 'Пользователь успешно удален')

        #по общему количеству
        response = self.client.get(self.list_url)
        users = response.context["users"]
        self.assertTrue(len(users) == 2)