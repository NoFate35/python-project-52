from django.test import TestCase
from django.urls import reverse
from task_manager.labels.models import Label
from django.contrib.auth.models import User


class StatusesTest(TestCase):
    fixtures = ["labels.json", "users.json", "statuses.json"]

    def setUp(self):
        self.label1 = Label.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.labels = Label.objects.all()
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.update_url = reverse("labels_update", kwargs={'pk': self.label2.id})
        self.create_url = reverse("labels_create")
        self.list_url = reverse("labels_list")
        self.delete_url = reverse("labels_delete", kwargs={'pk': self.label3.id})
        self.login_url = reverse("login")

    def test_fixtures(self):
        #проверка метки по названию, запрос из базы
        self.assertEqual(self.label1.name, "label1")
        #по общему количеству, запрос из базы
        self.assertEqual(len(self.labels), 3)
    
    def make_login(self):
        response = self.client.post(self.login_url, follow=True, data={'username': self.user2.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')


    def test_labels_list(self):
        
        self.make_login()
        #отображениие списка меток по коду ответа
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

        # по общему количеству
        self.assertIn("labels", response.context)
        labels = response.context["labels"]
        self.assertTrue(len(labels) == 3)


    def test_label_bad_authentificate_create_update_list_delete(self):
        #отобразить форму создания без аутентификации
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос на создание post без аутентификации
        response = self.client.post(self.create_url, data={"name": "label4"}, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отобразить форму изменения без аутентификации
        response = self.client.get(self.update_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос на изменение post без аутентификации
        response = self.client.post(self.update_url, data={"name": "label4",}, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отобразить форму удаления без аутентификации
        response = self.client.get(self.delete_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос на удаление post без аутентификации
        response = self.client.post(self.delete_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

    
    
    def test_label_bad_unique_create(self):
        #аутентификация
        self.make_login()

        #отправка запроса на создание    
        response = self.client.post(self.create_url, follow=True, data={"name": "label4"})
        self.assertContains(response, 'Метка успешно создана')

        #отправка запроса на создание такого же статуса
        response = self.client.post(self.create_url, follow=True, data={"name": "label4"})
        self.assertContains(response, 'Task label с таким Имя уже существует.')


    def test_labels_good_create(self):
        #аутентификация
        self.make_login()

        #отображение формы
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

        #отправка запроса на создание
        response = self.client.post(self.create_url, follow=True, data={"name": "label4"})
        self.assertContains(response, 'Метка успешно создана')

        #проверка создания в списке статусов
        response = self.client.get(self.list_url)
        self.assertContains(response, "label4")

        #по общему количеству
        labels = response.context["labels"]
        self.assertTrue(len(labels) == 4)

    
    def test_label_bad_unique_update(self):
        #аутентификация
        self.make_login()

        #отправить post запрос на обновление с уже существующим именем статуса
        response = self.client.post(self.update_url, follow=True, data={"name": self.label1.name})
        self.assertContains(response, 'Task label с таким Имя уже существует.')


    def test_label_good_update(self):
        #аутентификация
        self.make_login()

        #отправка запроса формы обновления
        response = self.client.get(self.update_url)
        self.assertEqual(response.status_code, 200)

        #отправка запроса post на обновление
        response = self.client.post(self.update_url, follow=True, data={"name": self.label2.name + "!"})
        self.assertContains(response, 'Метка успешно изменена')
        self.assertContains(response, 'label2!')
    

    def test_label_good_delete(self):
    
        self.make_login()

        #отображение страницы удаления
        response = self.client.get(self.delete_url)
        self.assertEqual(response.status_code, 200)

        #post запрос на удаление
        response = self.client.post(self.delete_url, follow=True)
        self.assertContains(response, 'Метка успешно удалена')

        #по общему количеству
        response = self.client.get(self.list_url)
        labels = response.context["labels"]
        self.assertTrue(len(labels) == 2)


    def test_label_bound_bad_delete(self):

        self.make_login()

        create_task_url = reverse("tasks_create")

        #отправка запроса на создание задачи с label1 и label2
        response = self.client.post(create_task_url, data={"name": "task5", "status": '2', 'labels': ['1', '2']}, follow=True)
        self.assertContains(response, 'Задача успешно создана')

        delete1_url = reverse("labels_delete", kwargs={'pk': self.label1.id})
        delete2_url = reverse("labels_delete", kwargs={'pk': self.label1.id})

        #post запрос на удаление пользователя который задействован
        response = self.client.post(delete1_url, follow=True)
        self.assertContains(response, 'Невозможно удалить метку, потому что она уже используется')

        response = self.client.post(delete2_url, follow=True)
        self.assertContains(response, 'Невозможно удалить метку, потому что она уже используется')
