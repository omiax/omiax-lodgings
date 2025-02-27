from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
# from rest_framework.permissions import IsAdminUser
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

from lodge.models import Lodge, Room
from lodge.serializers import LodgeSerializer, RoomSerializer
#  LodgeImageSerializer


# class LodgeImageViewSet(viewsets.ModelViewSet):
#     permission_classes = (permissions.AllowAny, )
#     parser_classes = (MultiPartParser, FormParser,)
#     queryset = Lodge.objects.all()
#     serializer_class = LodgeImageSerializer


class LodgeViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.AllowAny, )
    queryset = Lodge.objects.all()
    serializer_class = LodgeSerializer

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


class RoomViewSet(viewsets.ModelViewSet):
    # queryset = Room.objects.all()
    # permission_classes = (permissions.AllowAny, )
    serializer_class = RoomSerializer

    @action(detail=True, methods=['get'])
    def lodge_rooms(self, request, pk=None):
        queryset = Room.objects.filter(lodge=pk)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def booked_rooms(self, request):
        booked_rooms = Room.objects.filter(occupied=True)
        serializer = self.get_serializer(booked_rooms, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        """Return List of rooms belonging to a lodge or user"""
        # queryset = Room.objects.filter(tenant=self.request.user)
        queryset = Room.objects.all()
        lodge_id = self.request.query_params.get('lodge', None)
        # queryset = self.queryset
        if lodge_id:
            queryset = queryset.filter(lodge__id=lodge_id)

        return queryset
