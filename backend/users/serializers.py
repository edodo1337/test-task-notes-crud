from rest_framework import serializers
from rest_framework.serializers import ValidationError
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username")

    class Meta:
        model = Profile
        fields = ("pk", "full_name", "birth_date", "username")


class ProfileCreateSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    birth_date = serializers.DateField()
    username = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


class ProfileUpdateSerializer(serializers.Serializer):
    full_name = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    password = serializers.CharField(required=False)
    password_2 = serializers.CharField(required=False)

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password_2'):
            raise ValidationError("Passwords doesn't match")
        return super().validate(attrs)
