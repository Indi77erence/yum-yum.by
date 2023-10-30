from django.db import models


class Category(models.Model):
    """Категории"""
    name = models.CharField('Категория', max_length=20, primary_key=True)
    description = models.CharField('Описание', max_length=1000, default='Описание')

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ['name']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Coupons(models.Model):
    """Акции и купоны"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Выберите категорию'
                                 )
    title = models.CharField('Название', max_length=30, primary_key=True)
    content = models.CharField('Содержание купона', max_length=1000, blank=True)
    photo = models.TextField('Изображение', blank=True)
    price = models.CharField('Цена', max_length=10)
    market_name = models.CharField('Маркетплейс', max_length=30)
    post_date = models.DateField('Дата', auto_now=True)

    class Meta:
        unique_together = ['title', 'content']
        verbose_name = 'Купон'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.title
