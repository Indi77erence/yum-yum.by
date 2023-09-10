from django.db import models


class Coupons(models.Model):
    title = models.CharField(max_length=30, primary_key=True)
    content = models.CharField(max_length=1000, blank=True)
    photo = models.TextField(blank=True)
    price = models.CharField(max_length=10)
    market_name = models.CharField(max_length=30)
    post_date = models.DateField(auto_now=True)

    class Meta:
        unique_together = ['title', 'content']
        verbose_name = 'Купоны'
        verbose_name_plural = 'Купоны'

    def __str__(self):
        return self.title
