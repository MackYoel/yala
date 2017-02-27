from rest_framework import serializers
from main.models import (
    KnowledgeArea,
    Person,
    Theme,
    Issue
)


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


class IssueSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    doing = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Issue
        fields = ('pk', 'theme', 'name', 'doing', 'completed', 'created_at')


class ThemeSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    issues = IssueSerializer(many=True, source='five_issues', read_only=True)

    class Meta:
        model = Theme
        fields = ('pk', 'name', 'person', 'knowledge_area', 'created_at', 'issues')
