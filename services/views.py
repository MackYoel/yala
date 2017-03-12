from main.models import KnowledgeArea, Theme
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from main.models import Issue
from .serializers import (
    KnowledgeAreaSerializer,
    ThemeSerializer,
    IssueSerializer
)


class KnowledgeAreaList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        user = request.user
        items = KnowledgeArea.objects.filter(person__pk=user.pk).order_by('id')
        serializer = KnowledgeAreaSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        request.data['person'] = request.user.pk
        serializer = KnowledgeAreaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class ThemeList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, area_pk):
        user = request.user
        themes = Theme.objects.filter(
            person__pk=user.pk,
            knowledge_area=area_pk).order_by('-last_interaction')[0:10]

        serializer = ThemeSerializer(themes, many=True)
        return Response(serializer.data)

    def post(self, request, area_pk):
        request.data['person'] = request.user.pk
        serializer = ThemeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class IssueList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, theme_pk):
        theme = get_object_or_404(Theme, pk=theme_pk)
        issues = Issue.objects.filter(theme=theme)
        serializer = IssueSerializer(issues, many=True)
        return Response(serializer.data)

    def post(self, request, theme_pk):
        request.data['person'] = request.user.pk
        serializer = IssueSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class IssueDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, theme_pk, pk):
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        _open = request.query_params.get('open')
        complete = request.query_params.get('complete')
        issue = get_object_or_404(Issue, pk=pk)

        if start is not None:
            if not issue.doing:
                issue.start_session()
        elif end is not None:
            if issue.doing:
                issue.end_session()
        elif _open is not None:
            if issue.completed:
                issue.open()
        elif complete is not None:
            if not issue.completed:
                issue.complete()
        else:
            serializer = IssueSerializer(issue, data=request.data)
            if serializer.is_valid():
                serializer.save()
                issue.theme.update_interaction()
                return Response(serializer.data, status=200)
            return Response(serializer.errors, status=400)

        issue.theme.update_interaction()
        serializer = IssueSerializer(issue, many=False)
        return Response(serializer.data, status=200)
