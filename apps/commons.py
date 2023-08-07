# Django
from django.shortcuts import get_object_or_404
from django.http import Http404

# Django Rest Framework
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status, viewsets
from rest_framework.response import Response


class ListModelMixin:
    """
    List a queryset whit pagination for GenericViewSet.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
