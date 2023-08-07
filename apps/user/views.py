# Django
from django.shortcuts import get_object_or_404
from django.http import Http404

# Django Rest Framework
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

# apps
from apps.user.serializers import CreateUserSerializer, ListUserSerializer, ChangePasswordSerializer, DeleteAccount
from apps.user.models import User
from apps.commons import ListModelMixin


##
class CreateUser(CreateAPIView):
    """Api view for create an acount for one user"""

    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        """
        Create one user.
        """
        # in the serializers, we lets go to validate passwor2, for it we lets go to pass the context at serializxers
        serializer = CreateUserSerializer(
            data=request.data, context=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # we should delete password for security
        user_info = serializer.data
        user_info.pop("password")
        print(user_info)
        return Response(user_info, status=status.HTTP_201_CREATED)


class ChangePasswordView(UpdateAPIView):
    """Change password of an user"""

    # para buscar por username, see the next
    # https://github.com/encode/django-rest-framework/issues/6005
    lookup_field = 'username'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        # extraer el username del url
        username = self.kwargs['username']
        user = User.objects.filter(username=username)
        if not user:
            raise Http404("No MyModel matches the given query.")

        return user
    serializer_class = ChangePasswordSerializer


class DeleteUserAcount(RetrieveAPIView):
    """Delete account of one user"""

    # para buscar por username, see the next
    # https://github.com/encode/django-rest-framework/issues/6005
    lookup_field = 'username'
    # permission_classes = (IsAuthenticated,)

    def get_queryset(self):

        # extraer el username del url
        username = self.kwargs['username']
        print(self.kwargs, "..........................")
        user = User.objects.filter(username=username)
        if not user:
            raise Http404("No MyModel matches the given query.")

        return user

    serializer_class = DeleteAccount

    def retrieve(self, request, username, pk=None):
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        instance.status = False
        instance.save()
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)


class UserViewSet(ListModelMixin, viewsets.GenericViewSet, viewsets.ViewSet):
    """
    List of users with active acounts . 
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # los usuarios con status son los usuarios con cuentas activas
        return queryset.filter(status=True)

    # permission_classes = [IsAdminUser]
