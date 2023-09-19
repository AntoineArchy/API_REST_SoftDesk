import datetime

from rest_framework import serializers

from user.models import User

MIN_USER_AGE = datetime.timedelta(days=5475)


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle User.

    Attributs:
        url (str): Hyperlien vers l'API pour la ressource de l'utilisateur.
    """
    url = serializers.HyperlinkedIdentityField(view_name="api:user-detail")
    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'birthday', 'can_be_contacted', 'can_data_be_shared', 'is_active')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('is_active',)

    def validate(self, attrs):
        """
        Valide les attributs de l'utilisateur, notamment la date de naissance.

        Args:
            attrs (dict): Dictionnaire contenant les attributs de l'utilisateur.

        Returns:
            dict: Dictionnaire contenant les attributs validés de l'utilisateur.
        """
        birthday = attrs.get('birthday', datetime.datetime.now())

        if (birthday + MIN_USER_AGE) > datetime.datetime.now().date():
            raise serializers.ValidationError({"birthday": f"Sorry, you must be at least 15 to register."})
        return attrs

    def create(self, validated_data):
        """
        Crée un nouvel utilisateur.

        Args:
            validated_data (dict): Dictionnaire contenant les données validées de l'utilisateur.

        Returns:
            User: Instance de l'utilisateur créé.
        """
        user = User.objects.create_user(**validated_data)
        return user
