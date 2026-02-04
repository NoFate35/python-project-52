from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class UsersTest(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def test_fixtures(self):
        #проверка статуса по названию запрос из базы
        status = Status.objects.get(pk=1)
        self.assertEqual(status.name, "status1")
        #по общему количеству запрос из базы
        statuses = Status.objects.all()
        self.assertEqual(len(statuses), 3)

        #проверка пользователя по имени запрос из базы
        user = User.objects.get(pk=1)
        self.assertEqual(user.username, "rrr")
        #по общему количеству запрос из базы
        users = User.objects.all()
        self.assertEqual(len(users), 3)


    def test_statuses_list(self):
        #отображениие списка статусов по коду ответа
        response = self.client.get(reverse("statuses_list"))
        self.assertEqual(response.status_code, 200)
        # по общему количеству
        self.assertIn("statuses", response.context)
        statuses = response.context["statuses"]
        self.assertTrue(len(statuses) == 3)


    def test_status_bad_authentificate_create(self):
        #отобразить форму без аутентификации
        create_url = reverse("statuses_create")
        response = self.client.get(create_url, follow=True,)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос post без аутентификации
        response = self.client.post(create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
    
    def test_status_bad_unique_create(self):
        #аутентификация
        user = User.objects.filter(pk="2")[0]
        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': user.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')

        #отправка запроса на создание
        create_url = reverse("statuses_create")
        response = self.client.post(create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Статус успешно создан')

        #отправка запроса на создание такого же статуса
        create_url = reverse("statuses_create")
        response = self.client.post(create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Task status с таким Имя уже существует.')



    def test_status_create(self):
        #аутентификация
        user = User.objects.filter(pk="2")[0]
        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': user.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')

        #отображение формы
        create_url = reverse("statuses_create")
        response = self.client.get(create_url)
        self.assertEqual(response.status_code, 200)

        #отправка запроса на создание
        response = self.client.post(create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Статус успешно создан')

        #проверка создания в списке статусов
        list_url = reverse("statuses_list")
        response = self.client.get(list_url)
        self.assertContains(response, "status4")

        #по общему количеству
        statuses = response.context["statuses"]
        self.assertTrue(len(statuses) == 4)

    def test_status_update(self):
        status = Status.objects.filter(pk=2)[0]

        update_url = reverse("statuses_update", kwargs={'pk': status.id})

        response = self.client.get(update_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        response = self.client.post(update_url, follow=True, data={"name": status.name + "!"})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        
        user = User.objects.filter(pk="2")[0]
        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': user.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')

        response = self.client.get(update_url)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(update_url, follow=True, data={"name": status.name + "!"})
        self.assertContains(response, 'Статус успешно изменен')
        self.assertContains(response, 'Status2!')









    def test_bad_permission_middleware(self):
        user = User.objects.filter(first_name="Егор")[0]
        update_url = reverse("users_update", kwargs={'pk': user.id})
        response = self.client.post(update_url, follow=True, data={"first_name": "Bobik", "last_name": 'Sokkkkk', 'username': 'bob-S', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': 'rrr', 'password':'1234'})
        self.assertContains(response, 'Вы залогинены')

        user = User.objects.filter(first_name="пупсик")
        delete_url = reverse("users_delete", kwargs={'pk': user[0].id})
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, 'У вас нет прав для изменения другого пользователя.')







    def test_user_update(self):
        user = User.objects.filter(pk="2")[0]

        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': user.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')

        update_url = reverse("users_update", kwargs={'pk': user.id})
        response = self.client.get(update_url)

        self.assertEqual(response.status_code, 200)
        response = self.client.post(update_url, follow=True, data={"first_name": user.first_name, "last_name": user.last_name, 'username': 'egoska', 'password1':'123', 'password2':'123'})
        self.assertContains(response, 'Пользователь успешно изменен')
        self.assertContains(response, 'egoska')







    def test_user_bad_update(self):
        user = User.objects.filter(pk="2")[0]

        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': user.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')

        update_url = reverse("users_update", kwargs={'pk': user.id})
        response = self.client.post(update_url, follow=True, data={"first_name": user.first_name, "last_name": user.last_name, 'username': 'egoska', 'password1':'12', 'password2':'12'})
        self.assertContains(response, 'Введённый пароль слишком короткий. Он должен состоять из как минимум 3 символа.')







    def test_user_delete(self):
        user = User.objects.filter(pk="2")[0]

        login_url = reverse("login")
        response = self.client.post(login_url, follow=True, data={'username': user.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')

        delete_url = reverse("users_delete", kwargs={'pk': user.id})
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, 'Пользователь успешно удален')

        list_url = reverse("users_list")
        response = self.client.get(list_url)
        users = response.context["users"]
        self.assertTrue(len(users) == 2)

    