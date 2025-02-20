from rest_framework import serializers
from .models import Movie, Actor, Comment
from random import randint
from rest_framework import serializers

from .models import User

class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone',)

class RegisterSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ("id","is_user","is_admin","full_name","phone","password","confirm_password")

    def validate(self, data):
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords must match")

        return data


    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("confirm_password")

        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class VerifyOTPSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    verification_code = serializers.CharField(max_length=4)



class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = '__all__'

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('movie','user',)