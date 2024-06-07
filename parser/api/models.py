from django.db import models


class Author(models.Model):
    """Класс модели автора"""

    name = models.CharField(max_length=100, verbose_name="Имя автора")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Advt(models.Model):
    """Класс модели объявления (advertisement)"""

    title = models.CharField(max_length=100, verbose_name="Заголовок")
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    views = models.PositiveIntegerField(default=0, verbose_name="Кол-во просмотров")
    position = models.PositiveIntegerField(default=0, verbose_name="Позиция")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
