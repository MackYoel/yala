from rest_framework import serializers
from main.models import KnowledgeArea, Person


class PersonSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)

    class Meta:
        model = Person
        fields = ('pk', 'first_name', 'email', 'picture')


class KnowledgeAreaSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = KnowledgeArea
        fields = ('pk', 'person', 'name', 'created_at')
