from .models import Item, Item_Category, Item_Status
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    status_id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    category_id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        validated_data['item_numer'] = get_next_item_number(validated_data.staff_id)


class ItemStatusSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    class Meta:
        model = Item_Status
        fields = '__all__'

class ItemCategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    class Meta:
        model = Item_Category
        fields = '__all__'