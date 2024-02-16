from .models import Item, Item_Category, Item_Status, Image
from rest_framework import serializers

class ItemSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    # status = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    category_id = serializers.CharField(source='category.id', read_only=True)
    status_id = serializers.CharField(source='status.id', read_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=Item_Category.objects.all(), source='category_id')
    # status = serializers.PrimaryKeyRelatedField(queryset=Item_Status.objects.all(), source='status_id')
    class Meta:
        model = Item
        fields = '__all__'

    # def create(self, validated_data):
    #     validated_data['item_numer'] = get_next_item_number(validated_data.staff_id)


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

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['local_image']
        # fields = '__all__'

    def create(self, validated_data):
        print('validated_data')
        return Image.objects.create(**validated_data)

class BoolSerializer(serializers.Serializer):
    image_has_saved = serializers.BooleanField()

class ItemFmDtDictSerializesr(serializers.Serializer):
    img_id = serializers.IntegerField()
