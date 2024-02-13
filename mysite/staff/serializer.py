from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'