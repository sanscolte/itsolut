from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models import Author, Advt


class AdvtDetailAPITestCase(TestCase):
    """Класс тестов для API AdvtDetailView"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.client: APIClient = APIClient()
        cls.user: User = User.objects.create_user(
            username="testuser", password="testpass"
        )
        cls.author: Author = Author.objects.create(name="Test Author")
        cls.ad: Advt = Advt.objects.create(
            title="Test Advertisement", author=cls.author, views=10, position=1
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()
        cls.author.delete()
        cls.ad.delete()

    def test_get_ad_detail_success(self) -> None:
        """Успешный тест получения деталей объявления"""
        self.client.post(
            reverse("api_auth:login"),
            {"username": "testuser", "password": "testpass"},
        )
        response: Response = self.client.get(
            reverse("api:ad-detail", kwargs={"pk": self.ad.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Test Advertisement")
        self.assertEqual(response.data["author"]["name"], "Test Author")
        self.assertEqual(response.data["views"], 10)
        self.assertEqual(response.data["position"], 1)

    def test_get_ad_detail_failed(self) -> None:
        """Ошибочный тест получения деталей объявления"""
        response: Response = self.client.get(
            reverse("api:ad-detail", kwargs={"pk": self.ad.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_parse_ads_success(self) -> None:
        """Успешный тест парсинга объявлений"""
        self.client.login(username="testuser", password="testpass")
        response: Response = self.client.get(reverse("api:ads-parse"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data), 7)

    def test_parse_ads_failed(self) -> None:
        """Ошибочный тест парсинга объявлений"""
        response: Response = self.client.get(reverse("api:ads-parse"))
        self.assertEqual(response.status_code, 403)


class RegistrationTestCase(TestCase):
    """Класс тестов для API RegisterView"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user: User = User.objects.create_user(
            username="testuser", password="testpass"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def test_registration_success(self) -> None:
        """Успешный тест регистрации пользователя"""
        response: Response = self.client.post(
            reverse("api_auth:register"),
            {"username": "newuser", "password": "newpass"},
        )

        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_registration_failed(self) -> None:
        """Ошибочный тест регистрации пользователя"""
        response: Response = self.client.post(
            reverse("api_auth:register"),
            {"username": "testuser", "password": "testpass"},
        )
        self.assertEqual(response.status_code, 400)


class LoginTestCase(TestCase):
    """Класс тестов для API LogiView"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.user: User = User.objects.create_user(
            username="testuser", password="testpass"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.user.delete()

    def test_login_success(self) -> None:
        """Успешный тест входа пользователя"""
        response: Response = self.client.post(
            reverse("api_auth:login"),
            {"username": "testuser", "password": "testpass"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Login successful")

    def test_login_failed(self) -> None:
        """Ошибочный тест входа пользователя"""
        response: Response = self.client.post(
            reverse("api_auth:login"),
            {"username": "newuser", "password": "newpass"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "Invalid credentials")

    def test_double_login(self) -> None:
        """Ошибочный тест попытки войти авторизованному пользователю"""
        self.client.post(
            reverse("api_auth:login"),
            {"username": "testuser", "password": "testpass"},
        )
        response: Response = self.client.post(
            reverse("api_auth:login"),
            {"username": "testuser", "password": "testpass"},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["message"], "You login already")
