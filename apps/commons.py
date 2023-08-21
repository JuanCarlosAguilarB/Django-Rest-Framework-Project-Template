# Django
# from django.shortcuts import get_object_or_404
# from django.http import Http404

# Django Rest Framework
# from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
# from rest_framework.permissions import IsAdminUser
# from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class ListModelMixin:
    """
    Mixin for listing a queryset with pagination for GenericViewSet.
    """

    def list(self, request, *args, **kwargs):
        """
        Handles the listing of a queryset with pagination.
        """

        # Get the queryset based on the view's defined get_queryset method
        queryset = self.get_queryset()

        # Attempt to paginate the queryset
        page = self.paginate_queryset(queryset)

        # If pagination is applied, serialize and return paginated data
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # If no pagination is applied, serialize and return the entire queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class BasicPagination(PageNumberPagination):
    """
    Basic pagination class that extends PageNumberPagination.
    It allows setting the page size using the 'limit' query parameter.
    """
    page_size_query_param = 'limit'


class PaginationHandlerMixin(object):
    """
    Mixin to handle pagination of queryset results.
    """

    pagination_class = BasicPagination

    @property
    def paginator(self):
        """
        Returns an instance of the pagination class if defined.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Paginates the queryset using the defined pagination class.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                                                self.request, view=self)

    def get_paginated_response(self, data):
        """
        Returns a paginated response using the pagination class.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get_data_paginated(self, queryset=None, serializer_class=None, request=None):
        """
        Retrieves paginated data using the provided queryset, serializer class, and request.
        """
        if queryset is None:
            queryset = self.get_queryset()
        if serializer_class is None:
            serializer_class = self.get_serializer_class()
        if request is None:
            request = self.request

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(
            queryset, many=True, context={'request': request})
        return Response(serializer.data)
