from rest_framework import serializers
from watchlist_app.models import WatchList,StreamPlatform, Review
from django.utils.timezone import now

def name_length(name):
    if (len(name) < 5):
        raise serializers.ValidationError("Name is too short")
    else:
        return name



class StreamPlatformSerializer(serializers.ModelSerializer):

    # url = serializers.HyperlinkedIdentityField(view_name="stream-detail")
    # watchlist = WatchListSerializer(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        # fields = ("url", "website", "about", "name", "watchlist")
        fields = "__all__"


            
class ReviewSerializer(serializers.ModelSerializer):

    reviewer = serializers.StringRelatedField(read_only=True)
    # watchlist = serializers.CharField(source='watchlist.name')

    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ("watchlist",)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

class WatchListSerializer(serializers.ModelSerializer):

    # stream = serializers.CharField(source='stream.name')
    # reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = WatchList
        fields = "__all__"
    
    def create(self, validated_data):
        return WatchList.objects.create(**validated_data)