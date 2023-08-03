import datetime

from rest_framework import serializers

from user.models import User

MIN_USER_AGE = datetime.timedelta(days=5475)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'password', 'birthday', 'can_be_contacted', 'can_data_be_shared')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        birthday = attrs.get('birthday', datetime.datetime.now())

        if birthday.date() + MIN_USER_AGE > datetime.datetime.now().date():
            raise serializers.ValidationError({"birthday": f"birthday fields is invalid."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
