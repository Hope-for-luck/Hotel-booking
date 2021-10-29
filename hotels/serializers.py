from rest_framework import serializers
from .models import Hotel, HotelReview, HotelLike, HotelRoom, HotelFavorites


class HotelListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'name', 'stars', 'status')


class HotelDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = "__all__"

    def to_representation(self, instance):
        representation = super(HotelDetailSerializer, self).to_representation(instance)
        representation['rooms'] = HotelRoomSerializer(
            HotelRoom.objects.filter(hotel=instance.id), many=True).data
        representation['reviews'] = HotelReviewSerializer(
            HotelReview.objects.filter(hotel=instance.id), many=True).data
        representation['total_likes'] = HotelLike.objects.filter(hotel=instance.id).count()
        return representation


class HotelCreateSerializer(serializers.ModelSerializer):
    class Meta(HotelDetailSerializer.Meta):
        pass

    def validate_rent(self, price):
        if price < 10:
            raise serializers.ValidationError("Аренда не может быть меньше десяти")
        return price

    def validate_stars(self, stars):
        if stars not in range(1, 6):
            raise serializers.ValidationError("Количество звёзд должно быть от 1 до 5")
        return stars


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

    def get_hotel_name(self, hotel_like):
        name = hotel_like.hotel.name
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


class HotelRoomSerializer(serializers.ModelSerializer):
    hotel_name = serializers.SerializerMethodField("get_hotel_name")
    # total_floors = serializers.SerializerMethodField("get_hotel_total_floors")

    def get_hotel_name(self, hotel_room):
        name = hotel_room.hotel.name
        return name

    # def get_hotel_total_floors(self, hotel_room):
    #     total_floors = hotel_room.hotel.total_floors
    #     return total_floors

    class Meta:
        model = HotelRoom
        exclude = ('created_at', )


class HotelFavoritesSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='username.name')
    hotel_name = serializers.SerializerMethodField("get_hotel_name")

    def get_hotel_name(self, hotel_favorites):
        name = hotel_favorites.hotel.name
        return name

    class Meta:
        model = HotelFavorites
        fields = "__all__"

    def validate_hotel(self, hotel):
        if self.Meta.model.objects.filter(hotel=hotel).exists():
            raise serializers.ValidationError("Вы уже добавили в избранное данный отель")
        return hotel

    def create(self, validated_data):
        request = self.context.get('request')
        favorite = HotelFavorites.objects.create(
            username=request.user,
            **validated_data
        )
        return favorite
