from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    """
    JSON Web Token (JWT) Authentication class.

    This authentication class allows users to authenticate using JSON Web Tokens (JWT).
    JWT is a compact and URL-safe means of representing claims to be transferred between
    two parties. It is commonly used for stateless authentication in RESTful APIs.

    Attributes:
        User (Type): The Django user model class retrieved using `get_user_model()`.


    Methods:
        authenticate(request):
            Performs the authentication process using the provided JWT token in the request.

    Raises:
        AuthenticationFailed: If the provided token is invalid or expired, this exception is raised.
        ParseError: If there is an error parsing the token, this exception is raised.

    """
    def authenticate(self, request):
        """
        Authenticate the user using the provided JSON Web Token (JWT).

        This method extracts the JWT from the 'Authorization' header in the request and verifies its signature.
        If the token is valid, it decodes the token payload to retrieve the user identifier. It then queries the
        database to find the corresponding user and returns the authenticated user object along with the token
        payload.

        Args:
            request (rest_framework.request.Request):
            The request object representing the current request.

        Returns:
            tuple: A tuple containing the authenticated user object and the JWT token payload.

        Raises:
            AuthenticationFailed: If the provided token is invalid or expired, or if the user is not found,
                this exception is raised.
            ParseError: If there is an error parsing the token, this exception is raised.
        """
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(
            jwt_token)  # clean the token

        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(
                jwt_token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')
        except jwt.exceptions.DecodeError:
            raise ParseError()

        # Get the user from the database
        username_or_phone_number = payload.get('user_identifier')
        if username_or_phone_number is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(username=username_or_phone_number).first()
        if user is None:
            user = User.objects.filter(
                phone_number=username_or_phone_number).first()
            if user is None:
                raise AuthenticationFailed('User not found')

        # Return the user and token payload
        return user, payload

    def authenticate_header(self, request):
        """
        Get the authentication header string for JWT authentication.

        This method returns the authentication header string used for JWT authentication, which is 'Bearer'.
        This header string is included in the response when the client requests access to protected resources.

        Args:
            request (rest_framework.request.Request): The request object representing the current request.

        Returns:
            str: The authentication header string, which is 'Bearer'.
        """
        return 'Bearer'

    @classmethod
    def create_jwt(cls, user):
        """
        Create a JSON Web Token (JWT) for the specified user.

        This method creates a new JWT containing the user identifier, expiration time, issue time,
        email, and phone number as payload. The token is signed with the secret key specified in the
        Django settings using the 'HS256' algorithm.

        Args:
            user (django.contrib.auth.models.User): The Django user object for which the token will be created.

        Returns:
            str: The JWT token as a string.

        Note:
            The expiration time of the token is set to a specified number of hours from the current time,
            as defined in the 'JWT_CONF['TOKEN_LIFETIME_HOURS']' setting in the Django settings.py file.

        Example:
            To create a JWT token for a user, call this method with the user object:

            ```
            user = User.objects.get(pk=1)
            token = JWTAuthentication.create_jwt(user)
            # Use the token as needed
            ```
        """
        # Create the JWT payload
        payload = {
            'user_identifier': user.email,
            'exp': int((datetime.now() + timedelta(
                hours=settings.JWT_CONF['TOKEN_LIFETIME_HOURS'])).timestamp()),
            # set the expiration time for 5 hour from now
            'iat': datetime.now().timestamp(),
            'email': user.email,
            'phone': user.phone
        }

        # Encode the JWT with your secret key
        jwt_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

        return jwt_token

    @classmethod
    def get_the_token_from_header(cls, token):
        """
        Get the clean JWT token from the provided Authorization header.

        This method removes the 'Bearer' prefix and any extra spaces from the JWT token in the provided
        Authorization header, leaving only the clean JWT token.

        Args:
            token (str): The JWT token as provided in the Authorization header.

        Returns:
            str: The clean JWT token.

        Example:
            To extract the clean JWT token from an Authorization header, call this method with the header:

            ```
            authorization_header = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
            clean_token = JWTAuthentication.get_the_token_from_header(authorization_header)
            # Use the clean token as needed
            ```
        """
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token
