from typing import Dict

from django.test import TestCase

from api.models import Author, Advt


class AuthorModelTestCase(TestCase):
    """Класс тестов модели Author"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.author: Author = Author.objects.create(name="Test Author")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.author.delete()

    def test_verbose_name(self) -> None:
        """Тест валидности параметра verbose_name"""
        author: Author = AuthorModelTestCase.author
        field_verbose: Dict[str, str] = {
            "name": "Имя автора",
        }
        for field, expected_value in field_verbose.items():
            with self.subTest(field=field):
                self.assertEqual(
                    author._meta.get_field(field).verbose_name, expected_value
                )

    def test_name_max_length(self) -> None:
        """Тест параметра max_length у поля name"""
        author: Author = AuthorModelTestCase.author
        max_length: int = author._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)


class AdvtModelTestCase(TestCase):
    """Класс тестов модели Advt"""

    @classmethod
    def setUpClass(cls) -> None:
        cls.author: Author = Author.objects.create(name="Test Author")
        cls.ad: Advt = Advt.objects.create(
            title="New advertisement",
            author=cls.author,
            views=10,
            position=1,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.ad.delete()
        cls.author.delete()

    def test_verbose_name(self) -> None:
        """Тест валидности параметров verbose_name"""
        ad: Advt = AdvtModelTestCase.ad
        field_verboses: Dict[str, str] = {
            "title": "Заголовок",
            "author": "Автор",
            "views": "Кол-во просмотров",
            "position": "Позиция",
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(ad._meta.get_field(field).verbose_name, expected_value)

    def test_title_max_length(self) -> None:
        """Тест параметра max_length у поля title"""
        ad: Advt = AdvtModelTestCase.ad
        max_length: int = ad._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)
