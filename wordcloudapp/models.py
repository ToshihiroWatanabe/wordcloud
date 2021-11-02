from django.db import models


class Form(models.Model):
    url = models.CharField(max_length=100)
