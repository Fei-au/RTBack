from rest_framework import serializers
from .models import Profile
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']
class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    staff_id=serializers.IntegerField(source='id', read_only=True)
    class Meta:
        model = Profile
        fields = '__all__'

