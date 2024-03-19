from .models import Item, Item_Category, Item_Status, Image, Auction_Product_List
from staff.serializers import ProfileSerializer
from staff.models import Profile
from rest_framework import serializers
import os
import dotenv

dotenv.load_dotenv()
MEDIA_DOMAIN = os.getenv('MEDIA_DOMAIN')


class ItemStatusSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    class Meta:
        model = Item_Status
        fields = ['id', 'status']

class AuctionProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction_Product_List
        fields = '__all__'
class ImageSerializer(serializers.ModelSerializer):
    full_image_url=serializers.SerializerMethodField()
    class Meta:
        model = Image
        fields = ['id', 'local_image', 'full_image_url']
        # fields = '__all__'
    def get_full_image_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.local_image)
        else:
            # You can define a default domain if the request context is not available
            return f"http://{MEDIA_DOMAIN}{obj.local_image.url}"

    def create(self, validated_data):
        print('validated_data')
        return Image.objects.create(**validated_data)

class ItemSerializer(serializers.ModelSerializer):
    # id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    # status = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    images = ImageSerializer(many=True, read_only=True)  # Assuming 'images' is the related_name
    add_staff = ProfileSerializer(read_only=True)  # Use the related name
    status = ItemStatusSerializer(read_only=True)
    status_id = serializers.PrimaryKeyRelatedField(queryset=Item_Status.objects.all(), source='status', write_only=True)
    category_id = serializers.CharField(source='category.id', read_only=True)
    add_staff_id = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all(), source='add_staff', write_only=True)
    # category = serializers.PrimaryKeyRelatedField(queryset=Item_Category.objects.all(), source='category_id')
    # status = serializers.PrimaryKeyRelatedField(queryset=Item_Status.objects.all(), source='status_id')
    class Meta:
        model = Item
        fields = '__all__'




class ItemCategorySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  # Ensure ID is treated as a string
    class Meta:
        model = Item_Category
        fields = '__all__'


class BoolSerializer(serializers.Serializer):
    image_has_saved = serializers.BooleanField()

class ItemFmDtDictSerializesr(serializers.Serializer):
    img_id = serializers.IntegerField()
