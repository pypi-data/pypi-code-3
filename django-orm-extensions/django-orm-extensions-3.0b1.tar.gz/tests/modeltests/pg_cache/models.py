# -*- coding: utf-8 -*-

from django.db import models
from django_orm.postgresql.manager import Manager

class TestModel(models.Model):
    name = models.CharField(max_length=200)
    objects = models.Manager()
    manager = Manager()

