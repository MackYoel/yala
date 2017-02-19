from django.db import models
from django.contrib.auth.models import User


class Person(User):
    picture = models.CharField(max_length=255, null=True, blank=True)
    fb_id = models.CharField(max_length=255, null=True, blank=True)


class KnowledgeArea(models.Model):
    person = models.ForeignKey(Person)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Theme(models.Model):
    person = models.ForeignKey(Person)
    knowledge_area = models.ForeignKey(KnowledgeArea)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Issue(models.Model):
    theme = models.ForeignKey(Theme)
    name = models.CharField(max_length=50, unique=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
