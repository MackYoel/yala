from django.core.management.base import BaseCommand
from main.models import Issue


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        issues = Issue.objects.filter(person__isnull=True)

        ind = 0
        for ind, i in enumerate(issues, 1):
            i.person = i.theme.person
            i.save()

        self.stdout.write('\n[+] {} updated issues'.format(ind))
