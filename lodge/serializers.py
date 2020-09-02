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


class LodgeSerializer(serializers.HyperlinkedModelSerializer):
    # rooms = RoomIDSerializer(read_only=True, many=True)
    rooms_listing = serializers.HyperlinkedIdentityField(
        view_name='lodge:rooms-lodge-rooms', lookup_field='pk')

    lodge_listing = serializers.HyperlinkedIdentityField(
        view_name='lodge:lodge-detail', lookup_field='pk')

    image = serializers.ImageField(max_length=None,
                                   allow_empty_file=True,
                                   use_url=True,
                                   required=False)  #

    # tenants = UserSerializer(read_only=True, many=True, allow_null=True)

    class Meta:
        model = models.Lodge
        fields = [
            'id', 'name', 'address', 'state', 'water', 'electricity',
            'num_of_rooms', 'image', 'details', 'standard_price',
            'rooms_listing', 'lodge_listing'
            # 'tenants',
        ]
        # read_only_fields = ('id', )
