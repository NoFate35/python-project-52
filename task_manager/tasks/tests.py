from django.test import TestCase
from task_manager.tasks.models import Task
from django.contrib.auth.models import User
from django.urls import reverse


class TasksTest(TestCase):
    fixtures = ["tasks.json", "users.json", "statuses.json"]

    def setUp(self):
        self.list_url = reverse("tasks_list")
        self.task1 = Task.objects.get(name='task1')
        self.task2 = Task.objects.get(name='task2')
        self.tasks = Task.objects.all()
        self.create_url = reverse("tasks_create")
        self.user2 = User.objects.get(pk=2)
        self.login_url = reverse("login")
        self.update1_url = reverse("tasks_update", kwargs={'pk': self.task1.id})
        self.show1_url = reverse("tasks_show", kwargs={'pk': self.task1.id})
        self.delete2_url = reverse("tasks_delete", kwargs={'pk': self.task2.id})
    
    def test_fixtures(self):
        #проверка задачи по названию, запрос из базы
        self.assertEqual(self.task1.name, "task1")
        #по общему количеству, запрос из базы
        self.assertEqual(len(self.tasks), 2)


    def make_login(self):
        response = self.client.post(self.login_url, follow=True, data={'username': self.user2.username, 'password': '1234'})
        self.assertContains(response, 'Вы залогинены')
    
    def test_main_manu(self):
        #запрос главной страницы без логина
        response = self.client.get(reverse('home'))
        self.assertNotContains(response, 'Задачи')

        #логин
        self.make_login()
        #запрос главной страницы под логин пользователя
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Задачи')

    
    def test_tasks_list(self):
        #отображение списка пользователей
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Задачи')

        #по общему количеству
        self.assertIn("tasks", response.context)
        tasks = response.context["tasks"]
        self.assertTrue(len(tasks) == 2)


    def test_tasks_good_show(self):
        #логин под пользователем 2
        self.make_login()

        #просмотр задачи
        response = self.client.get(self.show1_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Просмотр задачи')
        self.assertContains(response, 'task1')
        self.assertContains(response, 'Изменить')
        self.assertContains(response, 'Удалить')


    def test_task_bad_authentificate_create_show_update_delete(self):
        #отобразить форму создания без аутентификации
        response = self.client.get(self.create_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос на создание post без аутентификации
        response = self.client.post(self.create_url, data={"name": "task3", "status": '2'})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отобразить страницу просмотра без аутентификации
        response = self.client.get(self.show1_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отобразить форму изменения без аутентификации
        response = self.client.get(self.update1_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос на изменение post без аутентификации
        response = self.client.post(self.update1_url, data={"name": "task2", "status": '1'})
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отобразить форму удаления без аутентификации
        response = self.client.get(self.delete2_url, follow=True)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')

        #отправить запрос на удаление post без аутентификации
        response = self.client.post(self.delete2_url)
        self.assertContains(response, 'Вы не авторизованы! Пожалуйста, выполните вход.')


    def test_status_good_create(self):
        #аутентификация
        self.make_login()

        #отображение формы
        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)

        #отправка запроса на создание
        response = self.client.post(self.create_url, data={"name": "task3", "status": '2'})
        self.assertContains(response, 'Задача успешно создана')

        #проверка создания в списке задач
        response = self.client.get(self.list_url)
        self.assertContains(response, "task3")

        #по общему количеству
        statuses = response.context["tasks"]
        self.assertTrue(len(statuses) == 3)

        #просмотр задачи
        response = self.client.get(reverse("tasks_show", kwargs={'pk': self.task3.id}))
        self.assertContains(response, 'task3')



    def test_task_bad_unique_create(self):

        #логин под пользователем 2
        self.make_login()

        #отправка запроса на создание
        response = self.client.post(self.create_url, data={"name": "task3", "status": '2'})
        self.assertContains(response, 'Задача успешно создана')

        #запрос на создание задачи с таким же именем
        response = self.client.post(self.create_url, data={"name": "task3", "status": '2'})
        self.assertContains(response, 'Task с таким Name уже существует.')


    def test_task_bad_unique_update(self):
        #аутентификация
        self.make_login()

        #отправить post запрос на обновление с уже существующим именем задачи
        response = self.client.post(self.update1_url, follow=True, data={"name": self.task2.name, 'status': self.task1.status})
        self.assertContains(response, 'Task status с таким Имя уже существует.')


    def test_status_good_update(self):
        #аутентификация под пользователем 2
        self.make_login()

        #отправка запроса формы обновления
        response = self.client.get(self.update1_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Изменить')

        #просмотр задачи
        response = self.client.get(self.show1_url)
        self.assertContains(response, 'task1')

        #отправка запроса post на обновление
        response = self.client.post(self.update1_url, follow=True, data={"name": 'task1update', 'status': self.task1.status})
        self.assertContains(response, 'task1update')

        #просмотр задачи
        response = self.client.get(self.show1_url)
        self.assertContains(response, 'task1update')

        #проверка обновления в списке задач
        response = self.client.get(self.list_url)
        self.assertContains(response, "task1update")

    def test_task_good_delete(self):
        #аутентификация под пользователем 2
        self.make_login()

        #отображение страницы удаления
        response = self.client.get(self.delete2_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Да, удалить')

        #post запрос на удаление
        response = self.client.post(self.delete2_url, follow=True)
        self.assertContains(response, 'Задача успешно удалена')

        #по общему количеству
        response = self.client.get(self.list_url)
        tasks = response.context["tasks"]
        self.assertTrue(len(tasks) == 1)


    def test_task_bad_author_delete(self):
        #аутентификация под пользователем 2
        self.make_login()

        #запрос на удаление задачи другого автора
        delete_url = reverse("tasks_delete", kwargs={'pk': self.task1.id})

        #post запрос на удаление задачи другого автора
        response = self.client.post(delete_url, follow=True)
        self.assertContains(response, 'Задачу может удалить только ее автор')

'''
    def test_task_filter_list(self):
        #отображение списка пользователей
        response = self.client.get(self.list_url, data={"status": "", "executor": '', 'label':''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Показать')
'''

