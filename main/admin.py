from django.contrib import admin
from .models import KnowledgeArea, Person, Theme, Issue, Session


class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'pk',)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'person', 'knowledge_area', 'last_interaction', 'created_at')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'completed', 'doing', 'created_at')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('issue', 'pk', 'starts_at', 'ends_at', 'active',
                    'closed_to_force')


admin.site.register(KnowledgeArea, KnowledgeAreaAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Issue, IssueAdmin)
admin.site.register(Session, SessionAdmin)
