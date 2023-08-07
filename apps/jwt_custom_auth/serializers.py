from rest_framework import serializers

# by simple jwt library
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class ObtainTokenSerializer(serializers.Serializer):
    """
    Serializer class for obtaining authentication token.

    Attributes:
        email (serializers.CharField):
            A CharField representing the username of the user.
        password (serializers.CharField):
            A CharField representing the password of the user.
    """
    email = serializers.CharField()
    password = serializers.CharField()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom TokenObtainPairSerializer with additional custom claims.

    This serializer extends the TokenObtainPairSerializer provided by 'rest_framework_simplejwt'
    to include additional custom claims in the JWT token. Custom claims are extra pieces of
    information that can be included in the token payload to carry additional data about the user.

    Attributes:
        TokenObtainPairSerializer (class): The base class for obtaining token pairs in
            'rest_framework_simplejwt'.

    Methods:
        get_token(user):
            Create a JWT token for the specified user with custom claims.

    Note:
        To use this serializer, you must have the 'rest_framework_simplejwt' library installed
        in your Django project and added this serializer to the 'SIMPLE_JWT' configuration in
        your Django settings.py file.

    Example:
        To use this custom serializer, specify it in the 'token_serializer' setting of the
        'SIMPLE_JWT' configuration in your Django settings.py file:

        ```
        # settings.py

        SIMPLE_JWT = {
            'TOKEN_SERIALIZER': 'path.to.MyTokenObtainPairSerializer',
            ...
        }
        ```

        With the custom serializer specified, when you request a token using the
        'TokenObtainPairView', the returned token will include the additional custom claims
        defined in this serializer, such as the user's name.
    """
    @classmethod
    def get_token(cls, user):
        """
        Create a JWT token for the specified user with custom claims.

        This method overrides the 'get_token' method of the base TokenObtainPairSerializer
        to include custom claims in the JWT token. The custom claims are added to the token's
        payload to carry additional information about the user.

        Args:
            user (django.contrib.auth.models.User): The Django user object for which the token will be created.

        Returns:
            rest_framework_simplejwt.tokens.AccessToken: The JWT token with custom claims.

        Example:
            To create a JWT token with custom claims for a user, call this method with the user object:

            ```
            user = User.objects.get(pk=1)
            token = MyTokenObtainPairSerializer.get_token(user)
            # Use the token as needed
            ```
        """

        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.name
        # ...

        return token
