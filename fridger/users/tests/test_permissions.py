import pytest
from model_bakery import baker
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from fridger.users.models import Friend


@pytest.mark.django_db
class TestFriendsRequestPermissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_not_friend = baker.make("users.User")
        self.test_friend = baker.make("users.User")
        self.test_friend_2 = baker.make("users.User")

        friendship = baker.make("users.Friend", friend_1=self.test_friend, friend_2=self.test_friend_2)
        self.url = reverse("friend-accept", args=[friendship.id])

    def test_not_friend_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.test_not_friend)

        response = client.post(self.url)

        assert response.status_code == 404

    def test_friend_request_sender_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.test_friend)

        response = client.post(self.url)

        assert response.status_code == 403

    def test_friend_request_receiver_has_access(self):
        client = APIClient()
        client.force_authenticate(self.test_friend_2)

        response = client.post(self.url)

        assert response.status_code == 200


@pytest.mark.django_db
class TestFriendsDestroyPermissions:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.test_not_friend = baker.make("users.User")
        self.test_friend = baker.make("users.User")
        self.test_friend_2 = baker.make("users.User")

        friendship = baker.make("users.Friend", friend_1=self.test_friend, friend_2=self.test_friend_2)
        self.url = reverse("friend-detail", args=[friendship.id])

    def test_not_friend_has_no_access(self):
        client = APIClient()
        client.force_authenticate(self.test_not_friend)

        response = client.delete(self.url)

        assert Friend.objects.count() == 1
        assert response.status_code == 404

    def test_friend_destroy_has_access(self):
        client = APIClient()
        client.force_authenticate(self.test_friend)

        response = client.delete(self.url)

        assert Friend.objects.count() == 0
        assert response.status_code == 204
