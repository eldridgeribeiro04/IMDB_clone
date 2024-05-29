from rest_framework import serializers
from watchlist_app.models import WatchList, StreamPlatform, Reviews


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Reviews
        # fields = "__all__"
        exclude = ("watchlist",)


class WatchListSerializer(serializers.ModelSerializer):
    
    # reviews = ReviewsSerializer(many=True, read_only=True)
    # len_name = serializers.SerializerMethodField()
    platform = serializers.CharField(source='platform.name')
    
    class Meta:
        model = WatchList
        # fields = ["id", "name", "description", "active"]
        fields = "__all__"
        
    # def get_len_name(self, obj):
    #     return len(obj.name)
        
    # def validate(self, data):
    #     if data['name'] == data['description']:
    #         raise serializers.ValidationError("Title and description cannot be the same")
    #     else:
    #         return data
    
    # def validate_name(self, value):
        
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name must be at least 2 characters")
    #     else:
    #         return value
        

# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
#     watchlist = WatchListSerializer(many=True, read_only=True)
    
#     class Meta:
#         model = StreamPlatform
#         fields = "__all__"

class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True, read_only=True)
    
    class Meta:
        model = StreamPlatform
        fields = "__all__"



# def name_lenght(value):
        
#         if len(value) < 2:
#             raise serializers.ValidationError("Name must be at least 2 characters")
#         else:
#             return value

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_lenght])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
    
#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
    
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description cannot be the same")
#         else:
#             return data
    
    # def validate_name(self, value):
        
    #     if len(value) < 2:
    #         raise serializers.ValidationError("Name must be at least 2 characters")
    #     else:
    #         return value
        
    