from django.contrib.auth.models import User
from django.db import models


class Memory(models.Model):
    title = models.CharField('Title', max_length=150)
    comment = models.TextField('Comment')
    latitude = models.CharField('Latitude', max_length=10)
    longitude = models.CharField('Longitude', max_length=10)
    created_by_user = models.ForeignKey(User, verbose_name='Created by user', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Memory'
        verbose_name_plural = 'Memories'


