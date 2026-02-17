from django.test import TestCase
from django.urls import reverse
from task_manager.statuses.models import Status
from django.contrib.auth.models import User


class StatusesTest(TestCase):
    fixtures = ["statuses.json", "users.json"]

    def setUp(self):
        self.status1 = Status.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.statuses = Status.objects.all()
        self.status2 = Status.objects.get(pk=2)
        self.update_url = reverse("statuses_update", kwargs={'pk': self.status2.id})
        self.create_url = reverse("statuses_create")
        self.list_url = reverse("statuses_list")
        self.login_url = reverse("login")

    def test_fixtures(self):
        #проверка статуса по названию, запрос из базы
        self.assertEqual(self.status1.name, "status1")
        #по общему количеству, запрос из базы
        self.assertEqual(len(self.statuses), 3)
    
    def make_login(self):
        response = self.client.post(self.login_url, follow=True, data={'username': self.user2.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')


    def test_statuses_list(self):
        #отображениие списка статусов по коду ответа
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        # по общему количеству
        self.assertIn("statuses", response.context)
        statuses = response.context["statuses"]
        self.assertTrue(len(statuses) == 3)


    def test_status_bad_authentificate_create(self):
        #отобразить форму без аутентификации
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос post без аутентификации
        response = self.client.post(self.create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
    
    def test_status_bad_unique_create(self):
        #аутентификация
        self.make_login()

        #отправка запроса на создание    
        response = self.client.post(self.create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Статус успешно создан')

        #отправка запроса на создание такого же статуса
        response = self.client.post(self.create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Task status с таким Имя уже существует.')


    def test_status_good_create(self):
        #аутентификация
        self.make_login()

        #отображение формы
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

        #отправка запроса на создание
        response = self.client.post(self.create_url, follow=True, data={"name": "status4"})
        self.assertContains(response, 'Статус успешно создан')

        #проверка создания в списке статусов
        response = self.client.get(self.list_url)
        self.assertContains(response, "status4")

        #по общему количеству
        statuses = response.context["statuses"]
        self.assertTrue(len(statuses) == 4)

    def test_status_bad_authentificate_update(self):
        #отобразить форму без аутентификации
        response = self.client.get(self.update_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        
        #отправить post запрос на обновление без аутентификации
        response = self.client.post(self.update_url, follow=True, data={"name": self.status2.name + "!"})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')
    
    def test_status_bad_unique_update(self):
        #аутентификация
        self.make_login()

        #отправить post запрос на обновление с уже существующим именем статуса
        response = self.client.post(self.update_url, follow=True, data={"name": self.status2.name})
        self.assertContains(response, 'Task status с таким Имя уже существует.')


    def test_status_good_update(self):
        #аутентификация
        self.make_login()

        #отправка запроса формы обновления
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

        #отправка запроса post на обновление
        response = self.client.post(self.update_url, follow=True, data={"name": self.status2.name + "!"})
        self.assertContains(response, 'Статус успешно изменен')
        self.assertContains(response, 'status2!')
    

    def test_status_good_delete(self):
    
        self.make_login()

        delete_url = reverse("statuses_delete", kwargs={'pk': self.status2.id})

        #отображение страницы удаления
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        #post запрос на удаление
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, 'Статус успешно удален')

        #по общему количеству
        response = self.client.get(self.list_url)
        users = response.context["statuses"]
        self.assertTrue(len(users) == 2)


    def test_status_bound_bad_delete(self):

        self.make_login()

        delete_url = reverse("statuses_delete", kwargs={'pk': self.status1.id})

        #post запрос на удаление пользователя который задействован
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, 'Невозможно удалить статус, потому что он используется')