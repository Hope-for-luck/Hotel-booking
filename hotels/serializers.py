from rest_framework import serializers
from .models import Hotel, HotelReview, HotelLike


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        exclude = ('description', 'image', 'created_at')


class HotelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(
            HotelDetailSerializer, self).to_representation(instance)
        representation['reviews'] = HotelReviewSerializer(
            HotelReview.objects.filter(hotel=instance.id), many=True
        ).data
        representation['total_likes'] = HotelLike.objects.filter(
            hotel=instance.id).count()
        return representation


class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta(HotelDetailSerializer.Meta):
        pass

    def validate_rent(self, rent):
        if rent < 10:
            raise serializers.ValidationError("Аренда не может быть меньше десяти")
        return rent


class HotelReviewSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.name')
    hotel_name = serializers.SerializerMethodField("get_hotel_name")

    class Meta:
        model = HotelReview
        fields = "__all__"

    def get_hotel_name(self, hotel_review):
        name = hotel_review.hotel.name
        return name

    def validate_hotel(self, hotel):
        if self.Meta.model.objects.filter(hotel=hotel).exists():
            raise serializers.ValidationError("Вы уже оставляли отзыв на данный отель")
        return hotel

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5"
            )
        return rating

    def create(self, validated_data):
        request = self.context.get('request')
        review = HotelReview.objects.create(
            username=request.user,
            **validated_data
        )
        return review


class HotelLikesSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.name')
    hotel_name = serializers.SerializerMethodField("get_hotel_name")

    def get_hotel_name(self, hotel_review):
        name = hotel_review.hotel.name
        return name

    class Meta:
        model = HotelLike
        fields = "__all__"

    def validate_hotel(self, hotel):
        if self.Meta.model.objects.filter(hotel=hotel).exists():
            raise serializers.ValidationError("Вы уже лайкали данный отель")
        return hotel

    def create(self, validated_data):
        request = self.context.get('request')
        like = HotelLike.objects.create(
            username=request.user,
            **validated_data
        )
        return like
