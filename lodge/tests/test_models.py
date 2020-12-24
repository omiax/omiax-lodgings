from django.test import TestCase
from lodge.models import Lodge, Room
from django.contrib.auth import get_user_model

User = get_user_model()


class TestModels(TestCase):
    def setUp(self):
        self.lodge1 = Lodge.objects.create(name="Lodge 1",
                                           address="Lodge Address",
                                           state="Akwa Ibom",
                                           num_of_rooms=3,
                                           standard_price=3000.00)
        self.rooms1 = Room.objects.filter(lodge=self.lodge1)
        self.user = User.objects.create(username='jacob',
                                        email='jacob@example.com',
                                        password='top_secret')

    def test_lodge_is_created(self):
        self.assertEquals(self.lodge1.standard_price, 3000.00)
        self.assertEquals(self.lodge1.num_of_rooms, 3)

    def test_room_is_created(self):
        self.assertTrue(self.rooms1.exists())
        self.assertEquals(len(self.rooms1), 3)

    def test_room_price_is_assigned(self):
        self.assertEquals(self.rooms1[0].room_price, 3000.00)

    def test_room_is_occupied_when_tenant_assigned(self):
        # update tenancy of room
        obj = self.rooms1[0]
        obj.tenant = self.user
        obj.save()

        self.assertEquals(self.rooms1[0].tenant, self.user)
        self.assertEquals(self.rooms1[0].occupied, True)

    def test_room_is_not_occupied_when_tenant_assigned(self):
        # update tenancy of room
        obj = self.rooms1[0]
        obj.tenant = None
        obj.save()

        self.assertEquals(self.rooms1[0].tenant, None)
        self.assertEquals(self.rooms1[0].occupied, False)
