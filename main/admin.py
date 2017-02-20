from django.contrib import admin
from .models import KnowledgeArea, Person


class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


class PersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'email', 'pk',)


admin.site.register(KnowledgeArea, KnowledgeAreaAdmin)
admin.site.register(Person, PersonAdmin)
