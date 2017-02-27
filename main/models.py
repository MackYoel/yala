from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


def str_obj(user):
    return user.email


User.__str__ = str_obj


class Person(User):
    picture = models.CharField(max_length=255, null=True, blank=True)
    fb_id = models.CharField(max_length=255, null=True, blank=True)


class KnowledgeArea(models.Model):
    person = models.ForeignKey(Person)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Theme(models.Model):
    person = models.ForeignKey(Person)
    knowledge_area = models.ForeignKey(KnowledgeArea)
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_interaction = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def five_issues(self):
        return self.issues.all().order_by('completed')

    def update_interaction(self):
        self.last_interaction = timezone.now()
        self.save()


class Issue(models.Model):
    theme = models.ForeignKey(Theme, related_name='issues', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    doing = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def start_session(self):
        session = Session(issue=self)
        session.save()
        self.doing = True
        self.save()

    def end_session(self):
        try:
            session = Session.objects.get(issue=self, active=True)
        except Session.DoesNotExist:
            self.doing = False
            self.save()
        except Session.MultipleObjectsReturned:
            sessions = Session.objects.filter(issue=self, active=True).order_by('-id')
            for s in sessions:
                s.active = False
                s.closed_to_force = True
                s.ends_at = timezone.now()
                s.save()
        else:
            session.ends_at = timezone.now()
            session.active = False
            session.save()
            self.doing = False
            self.save()

    def complete(self):
        self.end_session()
        self.completed = True
        self.save()

    def open(self):
        self.completed = False
        self.save()


class Session(models.Model):
    issue = models.ForeignKey(Issue)
    starts_at = models.DateTimeField(auto_now_add=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)
    closed_to_force = models.BooleanField(default=False)

    def __str__(self):
        return str(self.issue)
