from apps.user.serializers import ListUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import views, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# from drf_yasg.utils import swagger_auto_schema

from .serializers import ObtainTokenSerializer
from .authentication import JWTAuthentication

from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

User = get_user_model()


class ObtainUserLoginMiddleware():
    """
    Middleware class for user login using email or phone number.

    This middleware class is responsible for authenticating users based on their email or phone number.
    It takes the user's email/phone number and password from the request data and attempts to authenticate
    the user using the 'User' model in the Django database.

    Attributes:
        permission_classes (list): A list of permission classes specifying the permissions required to use this middleware.
            By default, this class allows any user to use the middleware ('permissions.AllowAny').

        serializer_class (class): The serializer class used to validate and deserialize the login data.
            By default, it uses 'ObtainTokenSerializer' for token-based authentication.

    Methods:
        get_user():
            Authenticate the user using the provided email/phone number and password.

    Returns:
        User instance or bool: The authenticated user object if authentication is successful,
            otherwise False.
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = ObtainTokenSerializer

    def get_user(self):
        """
        Authenticate the user using the provided email/phone number and password.

        This method attempts to authenticate the user by validating the email/phone number and password
        provided in the request data using the 'ObtainTokenSerializer'. It queries the 'User' model in
        the Django database based on the email/phone number and checks the password for authentication.

        Returns:
            django.contrib.auth.models.User or bool: The authenticated user object if authentication
                is successful, otherwise False.
        """
        request = self.request
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_phone_number = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')

        user = User.objects.filter(email=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(
                phone=username_or_phone_number).first()

        if user is None or not user.check_password(password):
            return False

        return user


class ObtainTokenView(ObtainUserLoginMiddleware, views.APIView):
    """
    API View to obtain a JWT token for user authentication.

    This API view combines the functionality of the 'ObtainUserLoginMiddleware' to authenticate users
    based on their email or phone number and the 'JWTAuthentication' class to generate the JWT token
    for the authenticated user.

    Attributes:
        ObtainUserLoginMiddleware (class): The middleware class for user login using email or phone number.
            It handles user authentication based on the provided email/phone number and password.

    Methods:
        post(request, *args, **kwargs):
            Handle the HTTP POST request to obtain the JWT token for user authentication.

    Returns:
        rest_framework.response.Response: The response containing the JWT token upon successful authentication,
            or an error message if authentication fails.

    Example:
        To use this API view, make a POST request to the view's endpoint with valid email/phone number
        and password credentials:

        ```
        POST
        {
            "email": "john_doe@example.com",
            "password": "secretpassword"
        }
        ```
        If the credentials are valid, the server will respond with the JWT token:

        ```
        HTTP 200 OK
        {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }
        ```
        Otherwise, if the credentials are invalid, the server will respond with an error message:

        ```
        HTTP 400 Bad Request
        {
            "message": "Invalid credentials"
        }
        ```
    """

    def post(self, request, *args, **kwargs):
        """
        Handle the HTTP POST request to obtain the JWT token for user authentication.

        This method uses the 'ObtainUserLoginMiddleware' to authenticate the user based on the provided
        email/phone number and password. If authentication is successful, it generates the JWT token
        using the 'JWTAuthentication.create_jwt' method and returns it in the response.

        Args:
            request (rest_framework.request.Request): The request object representing the current request.

        Returns:
            rest_framework.response.Response: The response containing the JWT token upon successful authentication,
                or an error message if authentication fails.
        """

        user = self.get_user()

        if not user:
            return Response({'message': 'Invalid credentials'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Generate the JWT token
        jwt_token = JWTAuthentication.create_jwt(user)

        return Response({'token': jwt_token})


class TokenObtainExtraDetailsView(ObtainUserLoginMiddleware,
                                  TokenObtainPairView):
    """
    API View to obtain JWT tokens for user authentication with extra details and using simple jwt library.

    This API view combines the functionality of the 'ObtainUserLoginMiddleware' to authenticate users
    based on their email or phone number and the 'TokenObtainPairView' provided by 'rest_framework_simplejwt'
    to generate the JWT tokens for the authenticated user.

    Attributes:
        ObtainUserLoginMiddleware (class): The middleware class for user login using email or phone number.
            It handles user authentication based on the provided email/phone number and password.

        TokenObtainPairView (class): The view provided by 'rest_framework_simplejwt' to obtain JWT tokens
            for user authentication using username and password.

    Note:
        The 'ObtainUserLoginMiddleware' class should be placed before the 'TokenObtainPairView' class in the
        class inheritance list to ensure that user authentication is performed before token generation.

    Example:
        To use this API view, make a POST request to the view's endpoint with valid email/phone number
        and password credentials:

        ```
        POST /api/token-extra/
        {
            "email": "john_doe@example.com",
            "password": "secretpassword"
        }
        ```
        If the credentials are valid, the server will respond with the JWT tokens:

        ```
        HTTP 200 OK
        {
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "extra_info": "extra info"
        }
        ```
        The 'access' token can be used to access protected resources, and the 'refresh' token can be used
        to request a new access token once it expires.
    """

    def get_tokens_for_user(self, user):
        """
        Get JWT tokens (refresh and access tokens) for the specified user.

        This function generates JWT tokens for the specified user using the 'rest_framework_simplejwt'
        library. It creates a new RefreshToken and derives the corresponding AccessToken from it.

        Args:
            user (django.contrib.auth.models.User): The Django user object for which the tokens will be generated.

        Returns:
            dict: A dictionary containing the 'refresh' and 'access' tokens as strings.

        Example:
            To generate JWT tokens for a user, call this function with the user object:

            ```
            user = User.objects.get(pk=1)
            tokens = get_tokens_for_user(user)
            # Use the tokens as needed
            ```
        """
        # Generate a new RefreshToken for the user
        refresh = RefreshToken.for_user(user)

        # Return the refresh and access tokens as strings
        respose = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            # 'extra_info': 'This is extra info'
        }
        return respose

    def post(self, request, *args, **kwargs):
        """
        Handle the HTTP POST request to obtain the JWT tokens for user authentication.

        This method uses the 'ObtainUserLoginMiddleware' to authenticate the user based on the provided
        email/phone number and password. If authentication is successful, it generates the JWT tokens
        using the 'get_tokens_for_user' method and returns them in the response.

        Args:
            request (rest_framework.request.Request): The request object representing the current request.

        Returns:
            rest_framework.response.Response: The response containing the JWT tokens upon successful authentication,
                or an error message if authentication fails.
        """

        user = self.get_user()

        if not user:
            return Response({'message': 'Invalid credentials'},
                            status=status.HTTP_400_BAD_REQUEST)

        respose = self.get_tokens_for_user(user)
        respose['user'] = ListUserSerializer(user).data
        return Response(respose, status=status.HTTP_200_OK)
