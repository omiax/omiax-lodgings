from rest_framework import serializers

from lodge import models
# from user.serializers import UserSerializer


class RoomSerializer(serializers.ModelSerializer):
    room_listing = serializers.HyperlinkedIdentityField(
        view_name='lodge:rooms-detail', lookup_field='pk')

    class Meta:
        model = models.Room
        fields = [
            'id',
            'lodge',
            'tenant',
            'room_number',
            'floor',
            'occupied',
            'room_price',
            'room_mates',
            'room_listing',
        ]
        read_only_fields = ('id', 'lodge', 'occupied', 'room_number')


class RoomBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = ("room_mates", "rent_start_date", "rent_end_date",
                  "transaction_id", "terms_agreed")


class RoomIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Room
        fields = [
            'id',
            'room_number',
        ]
        read_only_fields = (
            'id',
            'room_number',
        )


class LodgeImageSerializer(serializers.ModelSerializer):
    pictures = serializers.ImageField(max_length=None,
                                      allow_empty_file=True,
                                      use_url=True,
                                      required=False)

    class Meta:
        model = models.LodgeImage
        fields = ('pictures',)


class LodgeSerializer(serializers.HyperlinkedModelSerializer):
    # rooms = RoomIDSerializer(read_only=True, many=True)
    rooms_listing = serializers.HyperlinkedIdentityField(
        view_name='lodge:rooms-lodge-rooms', lookup_field='pk')

    lodge_listing = serializers.HyperlinkedIdentityField(
        view_name='lodge:lodge-detail', lookup_field='pk')

    # tenants = UserSerializer(read_only=True, many=True, allow_null=True)
    lodge_images = LodgeImageSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = models.Lodge
        fields = [
            'id', 'name', 'address', 'state', 'water', 'electricity', 'fencing', 'tar_road',
            'num_of_flats', 'details', 'standard_price', 'caution_deposit', 'agreement',
            'lodge_images', 'rooms_listing', 'lodge_listing'
            # 'tenants',
        ]
        read_only_fields = ('id', )
