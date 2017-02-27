from django.contrib import admin
from .models import KnowledgeArea, Person, Theme, Issue


class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'pk',)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ('name', 'person', 'knowledge_area', 'last_interaction', 'created_at')


class IssueAdmin(admin.ModelAdmin):
    list_display = ('name', 'theme', 'completed', 'doing', 'created_at')


admin.site.register(KnowledgeArea, KnowledgeAreaAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(Issue, IssueAdmin)
